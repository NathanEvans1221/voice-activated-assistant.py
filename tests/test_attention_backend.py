import sys
import types
import unittest
from unittest.mock import patch

from src.asr_worker import ASRWorker
from src.tts_worker import TTSWorker


class AttentionBackendTests(unittest.TestCase):
    def test_asr_passes_selected_attention_backend(self):
        captured = {}

        class FakeModel:
            @classmethod
            def from_pretrained(cls, path, **kwargs):
                captured.update(path=path, **kwargs)
                return cls()

        fake_module = types.SimpleNamespace(Qwen3ASRModel=FakeModel)
        with patch.dict(sys.modules, {"qwen_asr": fake_module}):
            worker = ASRWorker(attention_backend="flash_attention_2")
            worker.load_model()

        self.assertEqual(captured["attn_implementation"], "flash_attention_2")
        self.assertTrue(worker._model_loaded)

    def test_tts_passes_selected_attention_backend(self):
        captured = {}

        class FakeModel:
            @classmethod
            def from_pretrained(cls, path, **kwargs):
                captured.update(path=path, **kwargs)
                return cls()

            @property
            def model(self):
                return self

            def parameters(self):
                import torch

                return iter([torch.nn.Parameter(torch.zeros(1))])

        fake_module = types.SimpleNamespace(Qwen3TTSModel=FakeModel)
        with patch.dict(sys.modules, {"qwen_tts": fake_module}):
            worker = TTSWorker(model_path="fake-model", attention_backend="flash_attention_2")
            worker.load_model()

        self.assertEqual(captured["attn_implementation"], "flash_attention_2")
        self.assertIsNotNone(worker._engine)


if __name__ == "__main__":
    unittest.main()
