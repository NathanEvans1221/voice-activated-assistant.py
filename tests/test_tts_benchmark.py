import unittest

import numpy as np

from benchmarks.tts_benchmark import _sentences, summarize_audio


class TtsAudioSummaryTests(unittest.TestCase):
    def test_reports_duration_peak_and_rms_for_audio(self):
        result = summarize_audio(np.array([0.0, 0.0, 1.0, -1.0]), sample_rate=2)
        self.assertEqual(result["duration_seconds"], 2.0)
        self.assertEqual(result["peak_amplitude"], 1.0)
        self.assertAlmostEqual(result["rms_amplitude"], 2**-0.5)
        self.assertTrue(result["has_audio"])

    def test_reports_silence_as_empty_audio(self):
        result = summarize_audio(np.zeros(8), sample_rate=4)
        self.assertFalse(result["has_audio"])

    def test_rejects_empty_audio_and_invalid_sample_rate(self):
        with self.assertRaises(ValueError):
            summarize_audio(np.array([]), sample_rate=16000)
        with self.assertRaises(ValueError):
            summarize_audio(np.ones(4), sample_rate=0)

    def test_splits_greeting_like_the_assistant_worker(self):
        self.assertEqual(
            _sentences("系统已启动，你好！我有什么可以帮你的吗？"),
            ["系统已启动，", "你好！", "我有什么可以帮你的吗？"],
        )


if __name__ == "__main__":
    unittest.main()
