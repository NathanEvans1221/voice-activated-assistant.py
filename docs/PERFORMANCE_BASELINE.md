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

專案 `.venv` 仍是 CPU-only PyTorch。為了量測實際 CUDA ASR，本次另建 TEMP 隔離環境，不修改專案 `.venv`；該環境使用 PyTorch 2.10.0+cu126、Qwen ASR 0.0.6、Transformers 4.57.6、OpenCC 0.1.7。

## 固定 ASR 輸入

基準音訊、參考句及來源註記放在 [`benchmarks/fixtures/`](../benchmarks/fixtures/)。音訊取自 Qwen3-ASR 官方中文範例，16 kHz、單聲道、4.204 秒，SHA-256 為 `46dbc998c9d1d48111267c40741dd3200f2e5bcf4075f8c4c97f4451160dce50`。參考句為「甚至出現交易幾乎停滯的情況。」；基準會以 OpenCC 簡轉繁，與正式 ASR Worker 的輸出處理一致。

執行工具：`benchmarks/asr_benchmark.py`。在有 CUDA、`qwen-asr`、`soundfile` 與 `opencc-python-reimplemented` 的 Python 環境中，從專案根目錄執行：

```powershell
python -m benchmarks.asr_benchmark `
  --audio benchmarks/fixtures/asr_zh.wav `
  --reference benchmarks/fixtures/asr_zh.txt `
  --language auto --iterations 3 --warmup 1 `
  --output "$env:TEMP/asr_cuda_sdpa_auto_rerun.json"
```

加上 `--language Chinese` 可比較明確語言提示。基準記錄模型載入時間、首次推論、暖機時間、重複推論平均、CER、模型程序的 allocated/reserved 顯存峰值、裝置及套件版本。不同電腦請使用新的輸出檔，勿覆寫本次存檔數據。

## ASR CUDA／SDPA 實測（2026-10-04）

兩次量測均使用 RTX 3070 Laptop GPU、CUDA 12.6、相同本機 Qwen3-ASR-0.6B 權重、SDPA 和上述固定音訊。推論文字均經 OpenCC 轉為繁體中文；兩種語言設定的 CER 均為 0。

| 語言設定 | 載入秒數 | 首次推論秒數 | 暖機後平均（3 次） | CER | 載入峰值 allocated/reserved | 推論峰值 allocated/reserved |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 自動偵測 | 2.177 | 1.124 | 0.599 | 0.000 | 1789/1798 MiB | 1548/1812 MiB |
| Chinese | 5.081 | 3.176 | 1.639 | 0.000 | 1789/1798 MiB | 1548/1812 MiB |

每輪時間受載入快取、GPU 背景負載與首次核心初始化影響；這是單一中文樣本，不能代表多口音、多語言或實際麥克風的辨識品質。完整原始數據分別保存於 [`asr_cuda_sdpa_auto.json`](performance-results/asr_cuda_sdpa_auto.json) 與 [`asr_cuda_sdpa_chinese.json`](performance-results/asr_cuda_sdpa_chinese.json)。

Qwen ASR 與 TTS 已分別成功載入 `cuda:0`，並完成單模型推論；同時載入時的資源與延遲仍待量測。

## TTS CUDA／SDPA 實測（2026-10-05）

Qwen TTS 使用獨立 TEMP 環境，避免官方 `qwen-tts` 固定 Transformers 4.57.3 與 ASR 套件版本衝突。模型實際載入 RTX 3070 Laptop GPU 的 `cuda:0`；套件為 `qwen-tts` 0.1.1、Transformers 4.57.3、PyTorch 2.10.0+cu126。測試文字是應用程式啟動招呼語，speaker 使用應用程式設定的 `vivian`。測試依正式 worker 的繁轉簡與標點切句流程分成三段。

| 指標 | 冷啟動 | 暖機後（2 次平均） |
| --- | ---: | ---: |
| 模型載入 | 6.829 秒 | — |
| 第一段音訊可用時間 | 21.208 秒 | 21.470 秒 |
| 完整三段生成時間 | 61.018 秒 | 62.677 秒 |
| 模型載入峰值 allocated/reserved | 2059/2184 MiB | — |
| 推論峰值 allocated/reserved | — | 2139/2198 MiB |

輸出 WAV 為 24 kHz、5.92 秒，peak amplitude 0.723、RMS 0.091，非靜音。再由 ASR 交叉轉寫 24 kHz WAV（基準會先重取樣至 16 kHz），得到 CER 0.15；差異包含標點與「啓／啟」字形，主要語句可辨識。生成檔與原始量測分別在 [`tts_cuda_sdpa_vivian.wav`](performance-results/tts_cuda_sdpa_vivian.wav)、[`tts_cuda_sdpa_vivian.json`](performance-results/tts_cuda_sdpa_vivian.json) 與 [`tts_asr_intelligibility.json`](performance-results/tts_asr_intelligibility.json)。未執行人工聆聽評分，因此未對自然度或音色主觀品質下結論。

Qwen TTS 載入與推論均走 CUDA/SDPA，但環境沒有 `flash-attn`，套件提示使用 PyTorch attention 路徑；SoX 命令列程式也未安裝。模型仍成功在記憶體中生成 WAV。約 62.7 秒產生 5.92 秒音訊，代表目前 TTS 是明顯延遲瓶頸；暖機沒有降低完整生成平均時間。

## Flash Attention 2 可行性檢查（2026-10-05）

ASR 與 TTS 的隔離 CUDA 環境均為 PyTorch 2.10.0+cu126，確認 CUDA 可用且裝置為 RTX 3070 Laptop GPU（compute capability 8.6）；兩個環境都沒有 `flash_attn` 套件。Windows 主機上也未找到 `nvcc` 或 MSVC `cl`，因此目前無法從原始碼建置，也沒有可載入的 Flash Attention 2 後端可供同機比較。專案目前的 CUDA 數據只代表 SDPA。

FlashAttention 官方 README 將 Linux 列為安裝需求，並說明 Windows 可能可用但編譯仍需更多測試（[官方安裝說明](https://github.com/Dao-AILab/flash-attention/blob/main/README.md)）。本次沒有安裝未驗證來源的 Windows wheel，也沒有宣稱已比較兩種後端。可重現比較需先取得與 Python、PyTorch、CUDA 完全匹配且可信的 Windows wheel，或在 Linux/WSL CUDA 環境建置；之後必須以相同模型、音訊／文字量測延遲、顯存與輸出品質。現階段維持 SDPA 預設。

## ASR INT8 初步量測（2026-10-05）

在 ASR TEMP CUDA 環境安裝 `bitsandbytes` 0.50.2，以 `BitsAndBytesConfig(load_in_8bit=True)` 載入 Qwen3-ASR-0.6B；PyTorch 2.10.0+cu126、Transformers 4.57.6、RTX 3070 Laptop GPU。使用相同 4.204 秒固定音訊、自動語言偵測、SDPA、1 次暖機與 3 次量測。原始結果見 [`asr_cuda_bnb_int8_auto.json`](performance-results/asr_cuda_bnb_int8_auto.json)。

| 指標 | BF16 SDPA 基準 | INT8 | INT4 NF4 |
| --- | ---: | ---: | ---: |
| 模型載入 | 2.177 秒 | 6.236 秒 | 8.431 秒 |
| 首次推論 | 1.124 秒 | 10.087 秒 | 4.619 秒 |
| 暖機平均 | 0.599 秒 | 8.635 秒（慢 14.4 倍） | 2.804 秒（慢 4.7 倍） |
| CER | 0.000 | 0.000 | 0.000 |
| 載入峰值 allocated / reserved | 1789 / 1798 MiB | 1237 / 1266 MiB | 945 / 1048 MiB |
| 推論峰值 allocated / reserved | 1548 / 1812 MiB | 988 / 1272 MiB | 696 / 1062 MiB |

INT8 與 NF4 4-bit 都降低顯存，但此單一樣本上的暖機延遲分別慢 14.4 倍及 4.7 倍，不適用目前的即時辨識需求，因此不整合為正式預設。INT8 執行時 bitsandbytes 反覆提示將 BF16 輸入轉為 FP16；這是觀察到的行為，尚未單獨驗證它是否為全部延遲差異的原因。結果只涵蓋一段樣本，不能代表整體準確率。兩次 ASR 量測均使用臨時 runner，正式 benchmark 尚無量化 CLI 選項。NF4 原始數據見 [`asr_cuda_bnb_int4_auto.json`](performance-results/asr_cuda_bnb_int4_auto.json)。

## TTS NF4 初步量測（2026-10-08）

以新建的 TEMP CUDA 環境執行 Qwen TTS 0.1.1、Transformers 4.57.3、bitsandbytes 0.50.2、PyTorch 2.10.0+cu126 與 RTX 3070 Laptop GPU。輸入為與 BF16 基準相同的啟動招呼語，SDPA、BF16 計算、NF4 4-bit double quantization，並明確保留 `talker.codec_head` 為 BF16。原始資料與音檔見 [`tts_cuda_bnb_int4_nf4_vivian.json`](performance-results/tts_cuda_bnb_int4_nf4_vivian.json) 及 [`tts_cuda_bnb_int4_nf4_vivian.wav`](performance-results/tts_cuda_bnb_int4_nf4_vivian.wav)。

| 指標 | BF16 SDPA 基準 | NF4 4-bit（單次） |
| --- | ---: | ---: |
| 模型載入 | 6.829 秒 | 16.729 秒 |
| 首段音訊 | 21.208 秒（冷）／21.470 秒（暖機平均） | 28.034 秒 |
| 完整生成 | 61.018 秒（冷）／62.677 秒（暖機平均） | 79.718 秒 |
| 推論峰值 allocated / reserved | 2139 / 2198 MiB | 1266 / 1352 MiB |

此 NF4 單次測量相較 BF16 暖機平均約慢 27%，推論峰值 allocated 約低 41%；輸出音訊為 6.4 秒且有非零音訊。這只是一次冷生成，輸出尚未完成 ASR CER 交叉檢查或人工聽感評分，不足以判定品質或支援範圍。直接啟用 BNB NF4 時，Transformers 嘗試 deepcopy 自動尋找 tied weights，遭遇 `TypeError: cannot pickle 'dict_keys' object`；設定保留 `talker.codec_head` 後才成功。量測使用臨時 runner，正式 benchmark 尚無量化 CLI 選項；TTS INT8 與多樣本評估仍未完成。

重跑 TTS 基準時，使用裝有 CUDA PyTorch、Qwen TTS 0.1.1、Transformers 4.57.3 與 OpenCC 的隔離環境：

```powershell
python -m benchmarks.tts_benchmark `
  --text-file benchmarks/fixtures/tts_zh.txt `
  --speaker vivian --language Chinese --iterations 2 --warmup 1 `
  --output-wav "$env:TEMP/tts_cuda_sdpa_vivian_rerun.wav" `
  --output-json "$env:TEMP/tts_cuda_sdpa_vivian_rerun.json"
```

該命令使用預設 `models/Qwen3-TTS-12Hz-0.6B-CustomVoice`；環境建立方式與 Qwen 套件版本需求見 [Issue #1](https://github.com/chiisen/voice-activated-assistant.py/issues/1)。

## 目前可下的結論

- GPU 硬體存在，但目前專案虛擬環境的 PyTorch 不含 CUDA；只安裝 Flash Attention 或量化套件不會啟用 GPU 推論。
- 本次 `nvidia-smi` 顯示的顯存用量是單一時間點的整機觀察值，不能當成 ASR/TTS 模型的峰值用量。
- ASR/TTS 套件固定不同 Transformers 版本，因此分別在隔離環境測量；專案 `.venv` 尚未安裝 TTS extra，雙引擎相容性及同時載入需求尚未驗證。
- 目前只觀察到單樣本 ASR/TTS 量化降低顯存但降低速度；樣本和量測次數不足，不應外推為整體品質、速度或部署改善。
- Flash Attention 尚未比較；ONNX/TensorRT 尚未做端到端匯出和量測。

## 待補的可重複量測

- [x] 建立並保存一組固定中文語音測試輸入及參考轉寫；樣本來源與雜湊見 `benchmarks/fixtures/README.md`。後續需擴充樣本集。
- [x] 在 CUDA PyTorch 與 Qwen ASR 隔離環境，量 ASR 模型載入、首次／暖機延遲、CER 與顯存峰值。
- [x] 在 CUDA Qwen TTS 環境，使用固定文字及 `vivian` speaker 量模型載入、冷／暖機首音與完整生成時間、顯存峰值；保存 WAV 並以 ASR CER 驗證可懂度。人工聆聽的自然度評分未做。
- [ ] 比較 ASR/TTS 個別與同時載入時的峰值顯存和延遲。
- [ ] 每次比較記錄環境版本、模型目錄／revision、命令、輸入及原始結果。

## 重現環境資訊

在專案根目錄執行：

```powershell
.\.venv\Scripts\python.exe -c "import platform, torch; print(platform.platform()); print(platform.python_version()); print(torch.__version__, torch.version.cuda, torch.cuda.is_available())"
nvidia-smi --query-gpu=name,memory.total,memory.used,driver_version --format=csv,noheader
```
