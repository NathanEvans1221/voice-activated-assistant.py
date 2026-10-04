import sys
import threading
import types
from unittest.mock import patch

from src.rule_engine import TTSJob
from src.tts_worker import TTSWorker


def test_windows_fallback_engine_is_initialized_in_calling_worker_thread():
    init_thread_ids = []

    class FakeEngine:
        def say(self, text):
            pass

        def runAndWait(self):
            pass

    def init_engine():
        init_thread_ids.append(threading.get_ident())
        return FakeEngine()

    fake_pyttsx3 = types.SimpleNamespace(init=init_engine)
    worker = TTSWorker()
    worker._load_fallback_engine()
    main_thread_id = threading.get_ident()

    with patch("platform.system", return_value="Windows"), patch.dict(
        sys.modules, {"pyttsx3": fake_pyttsx3}
    ):
        thread = threading.Thread(
            target=worker._speak_fallback,
            args=(TTSJob(rule_id="test", text="測試"),),
        )
        thread.start()
        thread.join(timeout=5)

    assert not thread.is_alive()
    assert init_thread_ids
    assert init_thread_ids[0] != main_thread_id
