"""Repeatable local Qwen3-TTS latency and output-signal benchmark."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import re
import time
from pathlib import Path
from typing import Any

import numpy as np


def summarize_audio(audio: np.ndarray, sample_rate: int) -> dict[str, float | bool]:
    """Summarize basic signal health for a generated audio waveform."""
    samples = np.asarray(audio, dtype=np.float64)
    if sample_rate <= 0:
        raise ValueError("sample_rate must be positive")
    if samples.size == 0:
        raise ValueError("audio must contain at least one sample")

    peak = float(np.max(np.abs(samples)))
    return {
        "duration_seconds": samples.shape[0] / sample_rate,
        "peak_amplitude": peak,
        "rms_amplitude": float(np.sqrt(np.mean(np.square(samples)))),
        "has_audio": peak > 1e-4,
    }


def _sentences(text: str) -> list[str]:
    parts = re.findall(r"([^，。！？,;.!?]+[，。！？,;.!?]*)", text)
    return [part.strip() for part in parts if part.strip()] or [text]


def run_benchmark(args: argparse.Namespace) -> dict[str, Any]:
    import soundfile as sf
    import torch
    from opencc import OpenCC
    from qwen_tts import Qwen3TTSModel

    model_path = Path(args.model_path).resolve()
    original_text = Path(args.text_file).read_text(encoding="utf-8-sig").strip()
    simplified_text = OpenCC("t2s").convert(original_text)
    sentences = _sentences(simplified_text)

    device = "cuda:0" if args.device == "auto" and torch.cuda.is_available() else args.device
    if device == "auto":
        device = "cpu"
    dtype = torch.bfloat16 if device.startswith("cuda") else torch.float32
    if device.startswith("cuda"):
        torch.cuda.set_device(device)
        torch.cuda.reset_peak_memory_stats()

    load_started = time.perf_counter()
    model = Qwen3TTSModel.from_pretrained(
        str(model_path),
        device_map=device,
        dtype=dtype,
        attn_implementation=args.attention_backend,
        trust_remote_code=True,
    )
    if device.startswith("cuda"):
        torch.cuda.synchronize(device)
    load_seconds = time.perf_counter() - load_started
    load_peak_allocated_mib = (
        torch.cuda.max_memory_allocated(device) / 1024**2 if device.startswith("cuda") else None
    )
    load_peak_reserved_mib = (
        torch.cuda.max_memory_reserved(device) / 1024**2 if device.startswith("cuda") else None
    )

    def generate_utterance() -> tuple[float, float, np.ndarray, int]:
        started = time.perf_counter()
        first_audio_seconds = 0.0
        chunks = []
        sample_rate = 0
        for index, sentence in enumerate(sentences):
            with torch.inference_mode():
                waves, sample_rate = model.generate_custom_voice(
                    text=sentence,
                    speaker=args.speaker,
                    language=args.language,
                    do_sample=False,
                    max_new_tokens=args.max_new_tokens,
                )
            if device.startswith("cuda"):
                torch.cuda.synchronize(device)
            if not waves:
                raise RuntimeError(f"TTS returned no audio for segment {index + 1}")
            chunk = np.asarray(waves[0], dtype=np.float32).reshape(-1)
            if chunk.size == 0:
                raise RuntimeError(f"TTS returned empty audio for segment {index + 1}")
            chunks.append(chunk)
            if index == 0:
                first_audio_seconds = time.perf_counter() - started
        return time.perf_counter() - started, first_audio_seconds, np.concatenate(chunks), sample_rate

    cold_total_seconds, cold_first_audio_seconds, cold_audio, sample_rate = generate_utterance()
    warmup_seconds = [generate_utterance()[0] for _ in range(args.warmup)]
    if device.startswith("cuda"):
        torch.cuda.reset_peak_memory_stats()

    measured = []
    final_audio = cold_audio
    final_sample_rate = sample_rate
    for index in range(args.iterations):
        total_seconds, first_audio_seconds, final_audio, final_sample_rate = generate_utterance()
        measured.append({
            "iteration": index + 1,
            "first_audio_seconds": first_audio_seconds,
            "total_generation_seconds": total_seconds,
        })

    inference_peak_allocated_mib = (
        torch.cuda.max_memory_allocated(device) / 1024**2 if device.startswith("cuda") else None
    )
    inference_peak_reserved_mib = (
        torch.cuda.max_memory_reserved(device) / 1024**2 if device.startswith("cuda") else None
    )
    output_wav = Path(args.output_wav)
    output_wav.parent.mkdir(parents=True, exist_ok=True)
    sf.write(output_wav, final_audio, final_sample_rate)

    mean_first_audio = sum(row["first_audio_seconds"] for row in measured) / len(measured)
    mean_total = sum(row["total_generation_seconds"] for row in measured) / len(measured)
    return {
        "os": platform.platform(),
        "python": platform.python_version(),
        "torch": torch.__version__,
        "torch_cuda": torch.version.cuda,
        "qwen_tts": importlib.metadata.version("qwen-tts"),
        "transformers": importlib.metadata.version("transformers"),
        "gpu": torch.cuda.get_device_name(device) if device.startswith("cuda") else None,
        "device": device,
        "dtype": str(dtype),
        "attention_backend": args.attention_backend,
        "model_path": str(model_path),
        "model_config_transformers_version": _model_transformers_version(model_path),
        "text": original_text,
        "model_input_text": simplified_text,
        "sentences": sentences,
        "speaker": args.speaker,
        "language": args.language,
        "load_seconds": load_seconds,
        "load_peak_allocated_mib": load_peak_allocated_mib,
        "load_peak_reserved_mib": load_peak_reserved_mib,
        "cold_first_audio_seconds": cold_first_audio_seconds,
        "cold_total_generation_seconds": cold_total_seconds,
        "warmup_seconds": warmup_seconds,
        "iterations": measured,
        "warm_mean_first_audio_seconds": mean_first_audio,
        "warm_mean_total_generation_seconds": mean_total,
        "output_wav": str(output_wav.resolve()),
        "output_sample_rate": final_sample_rate,
        "output_audio_sha256": hashlib.sha256(output_wav.read_bytes()).hexdigest(),
        "output_audio": summarize_audio(final_audio, final_sample_rate),
        "inference_peak_allocated_mib": inference_peak_allocated_mib,
        "inference_peak_reserved_mib": inference_peak_reserved_mib,
    }


def _model_transformers_version(model_path: Path) -> str | None:
    config_path = model_path / "config.json"
    if not config_path.exists():
        return None
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return config.get("transformers_version")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-path", default="models/Qwen3-TTS-12Hz-0.6B-CustomVoice")
    parser.add_argument("--text-file", required=True)
    parser.add_argument("--speaker", default="vivian")
    parser.add_argument("--language", default="Chinese")
    parser.add_argument("--device", default="auto")
    parser.add_argument("--attention-backend", choices=("sdpa", "flash_attention_2"), default="sdpa")
    parser.add_argument("--max-new-tokens", type=int, default=512)
    parser.add_argument("--warmup", type=int, default=1)
    parser.add_argument("--iterations", type=int, default=3)
    parser.add_argument("--output-wav", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    args = parser.parse_args()
    if args.warmup < 0 or args.iterations < 1 or args.max_new_tokens < 1:
        parser.error("warmup must be nonnegative; iterations and max_new_tokens must be positive")
    return args


def main() -> None:
    args = parse_args()
    result = run_benchmark(args)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
