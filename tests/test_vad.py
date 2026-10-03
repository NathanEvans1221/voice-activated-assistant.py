import threading

import numpy as np

from src.vad_segmenter import VADConfig, VADSegmenter


def make_vad(callback):
    return VADSegmenter(VADConfig(min_utterance_ms=100, max_utterance_s=1,
                                  min_silence_duration=0.2), callback)


def test_continuous_speech_is_emitted_without_waiting_for_silence():
    output = []
    vad = make_vad(output.append)
    frame = np.full(1600, 0.2, dtype=np.float32)
    for _ in range(30):
        vad.process_frame(frame)
    assert len(output) == 3
    assert all(len(item.audio) == 16000 for item in output)
    assert not vad._buffer


def test_short_pause_is_preserved_in_audio():
    output = []
    vad = make_vad(output.append)
    voice = np.full(1600, 0.2, dtype=np.float32)
    silence = np.zeros(1600, dtype=np.float32)
    for frame in (voice, silence, voice, silence, silence):
        vad.process_frame(frame)
    assert len(output) == 1
    np.testing.assert_array_equal(output[0].audio[1600:3200], silence)
    assert len(output[0].audio) == 8000


def test_callback_can_reset_without_deadlock():
    completed = threading.Event()
    vad = make_vad(lambda _: (vad.reset(), completed.set()))

    def feed():
        vad.process_frame(np.ones(1600, dtype=np.float32))
        vad.process_frame(np.zeros(3200, dtype=np.float32))

    thread = threading.Thread(target=feed, daemon=True)
    thread.start()
    assert completed.wait(2), "VAD callback deadlocked while resetting"
    thread.join(timeout=1)


def test_oversized_frame_splits_without_losing_samples():
    output = []
    vad = make_vad(output.append)
    audio = np.linspace(0.1, 0.5, 48000, dtype=np.float32)
    vad.process_frame(audio)
    assert len(output) == 3
    np.testing.assert_array_equal(np.concatenate([item.audio for item in output]), audio)


def test_too_short_speech_is_discarded_and_next_sentence_starts_clean():
    output = []
    vad = make_vad(output.append)
    vad.process_frame(np.ones(800, dtype=np.float32))
    vad.process_frame(np.zeros(3200, dtype=np.float32))
    assert output == []
    for _ in range(30):
        vad.process_frame(np.ones(1600, dtype=np.float32))
        vad.process_frame(np.zeros(3200, dtype=np.float32))
    assert len(output) == 30
    assert not vad._buffer
