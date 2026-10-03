"""Load validated YAML defaults for the command-line entry point."""

from pathlib import Path
import math

import yaml


FIELDS = {
    "audio": {"sample_rate": "sample_rate", "frame_duration_ms": "frame_duration_ms",
              "channels": "channels", "device": "device"},
    "vad": {"silence_threshold": "silence_threshold", "silence_duration": "silence_duration",
            "min_utterance_ms": "min_utterance", "max_utterance_s": "max_utterance_s"},
    "orchestrator": {"resume_grace_s": "resume_grace_s", "rules_path": "rules",
                     "asr_model_path": "asr_model_path", "tts_model_path": "tts_model_path",
                     "device": "device_type", "tts_voice": "voice",
                     "attention_backend": "attention_backend"},
    "logging": {"debug": "debug", "level": "log_level"},
}


def load_defaults(path):
    try:
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ValueError(f"無法讀取設定檔 {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("設定檔必須是 YAML mapping")
    result = {}
    for section, values in data.items():
        if section not in FIELDS or not isinstance(values, dict):
            raise ValueError(f"未知或無效的設定區塊: {section}")
        for key, value in values.items():
            if key not in FIELDS[section]:
                raise ValueError(f"未知設定: {section}.{key}")
            result[FIELDS[section][key]] = value
    return result


def validate_options(args):
    for key in ("sample_rate", "frame_duration_ms", "min_utterance", "max_utterance_s",
                "silence_duration", "resume_grace_s", "silence_threshold"):
        value = getattr(args, key)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f"{key} 必須是有限數值")
        if value < 0 or (key not in ("resume_grace_s", "silence_threshold") and value == 0):
            raise ValueError(f"{key} 數值超出有效範圍")
    if args.sample_rate != 16000 or args.channels != 1:
        raise ValueError("目前 ASR 僅支援 16000 Hz、單聲道")
    if args.silence_threshold > 1:
        raise ValueError("silence_threshold 必須介於 0 與 1")
    if args.min_utterance > args.max_utterance_s * 1000:
        raise ValueError("最短語句不能長於最長語句")
    if not isinstance(args.debug, bool):
        raise ValueError("logging.debug 必須是布林值")
    if args.log_level not in ("DEBUG", "INFO"):
        raise ValueError("logging.level 目前支援 DEBUG 或 INFO")
    for key in ("rules", "asr_model_path", "tts_model_path"):
        if not isinstance(getattr(args, key), str) or not getattr(args, key).strip():
            raise ValueError(f"{key} 必須是非空字串")
    if args.device is not None and (type(args.device) is not int or args.device < 0):
        raise ValueError("audio.device 必須是非負整數或 null")
    for key in ("sample_rate", "frame_duration_ms", "min_utterance"):
        if type(getattr(args, key)) is not int:
            raise ValueError(f"{key} 必須是整數")
