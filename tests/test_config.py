import pytest

from src.main import parse_args


def test_yaml_defaults_and_explicit_cli_override(tmp_path):
    config = tmp_path / "config.yaml"
    config.write_text("vad:\n  silence_duration: 2.5\n  min_utterance_ms: 450\n"
                      "orchestrator:\n  asr_model_path: models/custom\n", encoding="utf-8")
    args = parse_args(["--config", str(config), "--silence-duration", "0.6"])
    assert args.silence_duration == 0.6
    assert args.min_utterance == 450
    assert args.asr_model_path == "models/custom"
    assert args.sample_rate == 16000


@pytest.mark.parametrize("content", ["[]", "vad: [1]", "vad:\n  typo: 1",
                                      "audio:\n  sample_rate: 8000",
                                      "vad:\n  silence_duration: -1",
                                      "vad:\n  silence_threshold: .nan",
                                      "orchestrator:\n  device: invalid"])
def test_invalid_config_fails_before_model_start(tmp_path, content):
    config = tmp_path / "bad.yaml"
    config.write_text(content, encoding="utf-8")
    with pytest.raises(SystemExit) as error:
        parse_args(["--config", str(config)])
    assert error.value.code == 2
