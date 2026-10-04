import hashlib
import unittest
import wave
from pathlib import Path

import numpy as np

from benchmarks.asr_benchmark import character_error_rate, resample_audio_to_16khz

FIXTURES = Path(__file__).parents[1] / "benchmarks" / "fixtures"


class CharacterErrorRateTests(unittest.TestCase):
    def test_exact_chinese_transcript_has_zero_error(self):
        self.assertEqual(character_error_rate("甚至出現交易幾乎停滯的情況。", "甚至出現交易幾乎停滯的情況。"), 0.0)

    def test_counts_insertions_deletions_and_substitutions(self):
        self.assertEqual(character_error_rate("甲乙丙", "甲丁"), 2 / 3)

    def test_empty_reference_is_rejected(self):
        with self.assertRaises(ValueError):
            character_error_rate("", "辨識文字")

    def test_resamples_24khz_tts_audio_to_16khz(self):
        audio = np.zeros(24000, dtype=np.float32)
        resampled, sample_rate = resample_audio_to_16khz(audio, 24000)
        self.assertEqual(sample_rate, 16000)
        self.assertEqual(len(resampled), 16000)

    def test_keeps_16khz_audio_and_rejects_invalid_rate(self):
        audio = np.zeros(16000, dtype=np.float32)
        resampled, sample_rate = resample_audio_to_16khz(audio, 16000)
        self.assertIs(resampled, audio)
        self.assertEqual(sample_rate, 16000)
        with self.assertRaises(ValueError):
            resample_audio_to_16khz(audio, 0)

    def test_reference_audio_fixture_is_fixed_and_16khz_mono(self):
        audio_path = FIXTURES / "asr_zh.wav"
        self.assertEqual(
            hashlib.sha256(audio_path.read_bytes()).hexdigest(),
            "46dbc998c9d1d48111267c40741dd3200f2e5bcf4075f8c4c97f4451160dce50",
        )
        with wave.open(str(audio_path), "rb") as audio:
            self.assertEqual(audio.getframerate(), 16000)
            self.assertEqual(audio.getnchannels(), 1)
        self.assertEqual(
            (FIXTURES / "asr_zh.txt").read_text(encoding="utf-8-sig").strip(),
            "甚至出現交易幾乎停滯的情況。",
        )


if __name__ == "__main__":
    unittest.main()
