"""Repeatable local Qwen3-ASR latency and character-error benchmark."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import math
import platform
import time
from pathlib import Path
from typing import Any


def character_error_rate(reference: str, hypothesis: str) -> float:
    """Return character error rate using Levenshtein distance."""
    if not reference:
        raise ValueError("reference must not be empty")

    previous = list(range(len(hypothesis) + 1))
    for ref_index, ref_char in enumerate(reference, start=1):
        current = [ref_index]
        for hyp_index, hyp_char in enumerate(hypothesis, start=1):
            current.append(
                min(
                    previous[hyp_index] + 1,
                    current[hyp_index - 1] + 1,
                    previous[hyp_index - 1] + (ref_char != hyp_char),
                )
            )
        previous = current
    return previous[-1] / len(reference)


def resample_audio_to_16khz(audio: Any, sample_rate: int) -> tuple[Any, int]:
    """Resample mono audio for the assistant's fixed 16 kHz ASR input contract."""
    if sample_rate <= 0:
        raise ValueError("sample_rate must be positive")
    if sample_rate == 16000:
        return audio, sample_rate

    from scipy.signal import resample_poly

    divisor = math.gcd(sample_rate, 16000)
    resampled = resample_poly(audio, 16000 // divisor, sample_rate // divisor)
    return resampled.astype("float32", copy=False), 16000


def run_benchmark(args: argparse.Namespace) -> dict[str, Any]:
    import soundfile as sf
    import torch
    from opencc import OpenCC
    from qwen_asr import Qwen3ASRModel

    audio_path = Path(args.audio).resolve()
    model_path = Path(args.model_path).resolve()
    audio, sample_rate = sf.read(audio_path, dtype="float32")
    if audio.ndim != 1:
        raise ValueError(f"expected mono audio, got {audio.shape}")
    source_sample_rate = sample_rate
    audio, sample_rate = resample_audio_to_16khz(audio, sample_rate)

    device = "cuda:0" if args.device == "auto" and torch.cuda.is_available() else args.device
    if device == "auto":
        device = "cpu"
    dtype = torch.bfloat16 if device.startswith("cuda") else torch.float32

    if device.startswith("cuda"):
        torch.cuda.set_device(device)
        torch.cuda.reset_peak_memory_stats()
    load_started = time.perf_counter()
    model = Qwen3ASRModel.from_pretrained(
        str(model_path),
        dtype=dtype,
        device_map=device,
        attn_implementation=args.attention_backend,
        trust_remote_code=True,
    )
    if device.startswith("cuda"):
        torch.cuda.synchronize(device)
    load_seconds = time.perf_counter() - load_started
    load_peak_mib = (
        torch.cuda.max_memory_allocated(device) / 1024**2
        if device.startswith("cuda")
        else None
    )
    load_reserved_peak_mib = (
        torch.cuda.max_memory_reserved(device) / 1024**2
        if device.startswith("cuda")
        else None
    )

    language = None if args.language.casefold() == "auto" else args.language
    traditional_converter = OpenCC("s2t")

    def transcribe() -> tuple[float, str]:
        started = time.perf_counter()
        result = model.transcribe(audio=(audio, sample_rate), language=language)
        if device.startswith("cuda"):
            torch.cuda.synchronize(device)
        transcript = traditional_converter.convert(result[0].text.strip()) if result else ""
        return time.perf_counter() - started, transcript

    if device.startswith("cuda"):
        torch.cuda.reset_peak_memory_stats()
    cold_seconds, cold_text = transcribe()
    warmup_seconds = [transcribe()[0] for _ in range(args.warmup)]

    if device.startswith("cuda"):
        torch.cuda.reset_peak_memory_stats()
    measured = []
    for index in range(args.iterations):
        seconds, transcript = transcribe()
        measured.append({"iteration": index + 1, "seconds": seconds, "transcript": transcript})

    inference_peak_mib = (
        torch.cuda.max_memory_allocated(device) / 1024**2
        if device.startswith("cuda")
        else None
    )
    inference_reserved_peak_mib = (
        torch.cuda.max_memory_reserved(device) / 1024**2
        if device.startswith("cuda")
        else None
    )
    reference = Path(args.reference).read_text(encoding="utf-8-sig").strip()
    final_transcript = measured[-1]["transcript"]
    return {
        "os": platform.platform(),
        "python": platform.python_version(),
        "torch": torch.__version__,
        "torch_cuda": torch.version.cuda,
        "qwen_asr": importlib.metadata.version("qwen-asr"),
        "transformers": importlib.metadata.version("transformers"),
        "opencc": importlib.metadata.version("opencc-python-reimplemented"),
        "gpu": torch.cuda.get_device_name(device) if device.startswith("cuda") else None,
        "device": device,
        "dtype": str(dtype),
        "attention_backend": args.attention_backend,
        "model_path": str(model_path),
        "audio_path": str(audio_path),
        "audio_sha256": hashlib.sha256(audio_path.read_bytes()).hexdigest(),
        "sample_rate": sample_rate,
        "source_sample_rate": source_sample_rate,
        "audio_seconds": len(audio) / sample_rate,
        "language": args.language,
        "reference": reference,
        "load_seconds": load_seconds,
        "load_peak_allocated_mib": load_peak_mib,
        "load_peak_reserved_mib": load_reserved_peak_mib,
        "cold_inference_seconds": cold_seconds,
        "cold_transcript": cold_text,
        "warmup_seconds": warmup_seconds,
        "iterations": measured,
        "warm_mean_seconds": sum(row["seconds"] for row in measured) / len(measured),
        "warm_mean_rtf": (
            sum(row["seconds"] for row in measured) / len(measured) / (len(audio) / sample_rate)
        ),
        "character_error_rate": character_error_rate(reference, final_transcript),
        "inference_peak_allocated_mib": inference_peak_mib,
        "inference_peak_reserved_mib": inference_reserved_peak_mib,
        "post_inference_reserved_mib": (
            torch.cuda.memory_reserved(device) / 1024**2
            if device.startswith("cuda")
            else None
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-path", default="models/Qwen3-ASR-0.6B")
    parser.add_argument("--audio", required=True)
    parser.add_argument("--reference", required=True)
    parser.add_argument("--language", default="Chinese", help="Use 'auto' to enable language detection")
    parser.add_argument("--device", default="auto")
    parser.add_argument("--attention-backend", choices=("sdpa", "flash_attention_2"), default="sdpa")
    parser.add_argument("--warmup", type=int, default=1)
    parser.add_argument("--iterations", type=int, default=3)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.warmup < 0 or args.iterations < 1:
        parser.error("--warmup must be nonnegative and --iterations must be at least 1")
    return args


def main() -> None:
    args = parse_args()
    result = run_benchmark(args)
    output = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()
