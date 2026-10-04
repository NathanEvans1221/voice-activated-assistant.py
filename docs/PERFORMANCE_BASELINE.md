# 推論效能基準

本文件保存量測環境與結果。只有使用可重複的輸入、相同模型及相同硬體取得的數據，才用來判定效能是否改善。

## 環境盤點

盤點日期：2026-10-04。以下為本機專案 `.venv` 與已下載模型的狀態：

| 項目 | 觀察值 |
| --- | --- |
| OS | Windows，Python 回報 `Windows-10-10.0.26300-SP0` |
| Python | 3.11.9 x64 |
| GPU | NVIDIA GeForce RTX 3070 Laptop GPU，8192 MiB |
| NVIDIA 驅動 | 560.94；`nvidia-smi` 顯示 CUDA 相容版本 12.6 |
| GPU 顯存觀察 | 查詢當下約使用 1780 MiB；包含桌面及背景程式，並非模型峰值 |
| PyTorch | 2.10.0（CPU build）；`torch.version.cuda` 為 `None`，`torch.cuda.is_available()` 為 `False` |
| Transformers | 4.57.6 |
| Qwen ASR 套件 | `qwen-asr` 0.0.6 |
| Qwen TTS 套件 | 未安裝；程式會使用 Windows TTS 備援 |
| bitsandbytes | 未安裝 |
| pyttsx3 | 2.98 |
| Silero VAD | 6.2.1 |
| 本機模型 | `Qwen3-ASR-0.6B` 與 `Qwen3-TTS-12Hz-0.6B-CustomVoice` 目錄存在 |
| ASR 模型設定 | `config.json` 宣告 Transformers 4.57.6 |
| TTS 模型設定 | `config.json` 宣告 Transformers 4.57.3 |

目前 ASR 可在 CPU 環境執行，但本盤點沒有固定的語音測試集和參考轉寫，因此尚無可重現的 ASR 品質／延遲基準。TTS 套件缺漏，所以也沒有 Qwen TTS 的冷啟動、暖機、首音、總生成時間、顯存峰值或音質數據。

## 目前可下的結論

- GPU 硬體存在，但目前專案虛擬環境的 PyTorch 不含 CUDA；只安裝 Flash Attention 或量化套件不會啟用 GPU 推論。
- 本次 `nvidia-smi` 顯示的顯存用量是單一時間點的整機觀察值，不能當成 ASR/TTS 模型的峰值用量。
- ASR/TTS 模型設定記錄了不同的 Transformers 版本；TTS 套件目前未安裝，雙引擎相容性及同時載入需求尚未驗證。
- 不應以目前資料宣稱 Flash Attention、量化、ONNX 或 TensorRT 有速度或顯存改善。

## 待補的可重複量測

- [ ] 建立並保存固定中文語音測試集及人工確認的參考轉寫。
- [ ] 在 CUDA PyTorch 與 Qwen 套件可用的隔離環境，量 ASR 冷啟動／暖機延遲、辨識品質與顯存峰值。
- [ ] 在 Qwen TTS 可用環境，使用固定文字及 speaker 量首音延遲、總生成時間、顯存峰值與輸出品質。
- [ ] 比較 ASR/TTS 個別與同時載入時的峰值顯存和延遲。
- [ ] 每次比較記錄環境版本、模型目錄／revision、命令、輸入及原始結果。

## 重現環境資訊

在專案根目錄執行：

```powershell
.\.venv\Scripts\python.exe -c "import platform, torch; print(platform.platform()); print(platform.python_version()); print(torch.__version__, torch.version.cuda, torch.cuda.is_available())"
nvidia-smi --query-gpu=name,memory.total,memory.used,driver_version --format=csv,noheader
```
