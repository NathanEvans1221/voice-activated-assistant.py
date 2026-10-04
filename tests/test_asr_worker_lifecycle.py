import threading
import time

import numpy as np

from src.asr_worker import ASRResult, ASRWorker


def test_stop_waits_for_inflight_recognition_and_suppresses_late_result():
    recognition_started = threading.Event()
    release_recognition = threading.Event()
    stop_finished = threading.Event()
    results = []
    worker = ASRWorker(on_result=results.append)

    def blocked_recognition(_audio):
        recognition_started.set()
        assert release_recognition.wait(5)
        return ASRResult(transcript="late result")

    worker._recognize = blocked_recognition
    worker.start()
    assert worker.process(np.zeros(160, dtype=np.float32))
    assert recognition_started.wait(1)

    stopper = threading.Thread(target=lambda: (worker.stop(), stop_finished.set()))
    stopper.start()
    try:
        # stop() must not forget the worker while model inference is still active.
        assert not stop_finished.wait(2.2)
    finally:
        release_recognition.set()
        stopper.join(timeout=2)

    assert stop_finished.is_set()
    assert results == []
    assert worker._worker_thread is None


def test_worker_restarts_after_stop_and_discards_queued_audio():
    recognition_started = threading.Event()
    release_recognition = threading.Event()
    new_result_received = threading.Event()
    results = []

    def on_result(result):
        results.append(result.transcript)
        if result.transcript == "new":
            new_result_received.set()

    worker = ASRWorker(on_result=on_result)

    def controlled_recognition(audio):
        if audio[0] == 1:
            recognition_started.set()
            assert release_recognition.wait(5)
            return ASRResult(transcript="stopped")
        return ASRResult(transcript="new")

    worker._recognize = controlled_recognition
    worker.start()
    worker.process(np.array([1], dtype=np.float32))
    assert recognition_started.wait(1)
    worker.process(np.array([2], dtype=np.float32))

    stopper = threading.Thread(target=worker.stop)
    stopper.start()
    deadline = time.monotonic() + 1
    while worker._is_running and time.monotonic() < deadline:
        time.sleep(0.01)
    assert not worker._is_running
    release_recognition.set()
    stopper.join(timeout=2)
    assert not stopper.is_alive()

    worker.start()
    assert worker.process(np.array([3], dtype=np.float32))
    assert new_result_received.wait(1)
    worker.stop()

    assert results == ["new"]
