# 🎙️ 語音互動助理 (Voice-Activated Assistant)

這是一個基於 Python 開發的高效能、隱私優先的本地端語音代理系統。透過整合最新的 Qwen3 ASR 與 TTS 技術，實現流暢的語音指令識別與自動化回應。

---

> [!WARNING]
> **WSL 環境限制**：由於 WSL 預設無法存取 Windows 端的麥克風硬體，請務必在 **Windows 原生環境**（PowerShell/CMD）中執行本程式。如需在 WSL 中使用，請參考「常見問題」章節。

---


## ✨ 核心特性

- **🚀 極速本地推論**：使用 Qwen3-ASR 與 Qwen3-TTS，支援串流輸出，具備極低首包延遲。
- **🗣️ 純淨自然發音**：內建 OpenCC 簡繁轉換機制，避免 TTS 模型朗讀繁體中文時產生混淆（如自動切換為粵語口音），確保發音皆為標準的國語/普通話。同時排除帶有強烈方言口音的角色，保障溝通無礙。
- **🤫 隱私與安全**：語音轉文字 (ASR) 結果僅暫存於記憶體 (RAM)，程式結束後自動釋放，不留任何磁碟紀錄。
- **🧠 智慧停頓偵測 (VAD)**：預設連續靜音 0.8 秒後結束語句，可用 `--silence-duration` 調整。
- **🚦 狀態機協調**：當 TTS 播放時自動暫停 ASR 監聽，完美解決「自己聽到自己講話」的自我回饋問題。
- **🛠️ JSON 驅動規則**：透過簡單的 JSON 設定檔定義關鍵字、優先序與多樣化的回覆模式。

---

## 🏗️ 技術架構

系統採用多執行緒非同步設計，確保音訊採集與 AI 推論互不干擾：

> 📦 **預覽須知**：本圖使用 Mermaid 語法繪製。若在 VS Code 中看不到圖示，
> 請安裝擴充套件 [Markdown Preview Mermaid Support](https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid)
> （搜尋 `bierner.markdown-mermaid`）後，重新開啟 Markdown Preview 即可正常顯示。

```mermaid
flowchart TD
    A[🎤 麥克風收音] --> B{VAD 語音偵測}
    B -- 有人聲 --> C[將音訊存入緩衝]
    B -- 靜音達 1s --> D[Finalize Utterance]
    D --> E[Qwen3-ASR 推論]
    E --> F[取得 Transcript 文字]
    F --> G{關鍵字規則引擎}
    G -- 命中規則 --> H[產生 TTS Job]
    H --> I[Qwen3-TTS 語音合成]
    I --> J[🔊 揚聲器播放]
    
    subgraph 互斥機制
    J -- 播放中 --> K[暫停 ASR 收音/判斷]
    end
```

---

## 🛠️ 技術棧

- **語言**: Python 3.11.9+
- **ASR**: Qwen3-ASR (程式預設本機路徑為 0.6B)
- **TTS**: Qwen3-TTS
- **VAD**: Silero VAD
- **併發**: Threading + Python Queue

---

## � 開發進度與計畫

專案採階段性開發，目前已完成核心架構的設計與初步實作。詳細的任務追蹤請參閱：

- [📝 專案待辦事項](docs/project_tasks.md)：包含各階段 (Phase 1-8) 的實作清單與驗收標準。
- [⚡ 效能優化待辦](docs/TODO.md)：記錄注意力後端、量化與推論引擎評估。
- [📄 產品需求文件](docs/PRD.md)：系統範圍與演算法規格。

## 🚀 快速開始

### 1. 安裝依賴

啟動時讀取 `config/config.yaml`，或用 `--config 路徑` 指定檔案。設定優先序為 CLI 明確參數 > YAML > 程式預設值；檔案中的相對路徑以工作目錄為基準。附帶 YAML 的停頓時間為 1.5 秒，可用 `--silence-duration 0.8` 覆寫。錯誤設定會在模型啟動前終止。

```powershell
# 使用 uv（推薦，ASR 與 TTS 引擎擇一）
uv sync --extra asr  # Qwen3-ASR
# 或
uv sync --extra tts  # Qwen3-TTS

# 使用 pip 時，requirements.txt 僅安裝核心依賴；模型套件擇一安裝
pip install -r requirements.txt
pip install qwen-asr  # 或改為 pip install qwen-tts
```

Qwen ASR/TTS 目前固定了不同 Transformers 版本，請勿同時安裝兩個模型套件。

### 2. 準備 ASR 模型

程式預設從 `models/Qwen3-ASR-0.6B` 載入模型。請先將模型放在該路徑，或修改程式設定；`uv sync` 會安裝專案依賴。

```powershell
# 預設讀取 models/Qwen3-ASR-0.6B
python src/main.py --rules config/rules.json
```

若要手動預先下載：
```powershell
# 使用 transformers 庫下載模型
python -c "from transformers import AutoModelForSpeech2Seq; m = AutoModelForSpeech2Seq.from_pretrained('Qwen/Qwen3-ASR-0.6B', torch_dtype='float32', device_map='cpu')"
```

或直接從 Hugging Face 下載：
- [Qwen3-ASR-0.6B](https://huggingface.co/Qwen/Qwen3-ASR-0.6B)（較小，推薦）
- [Qwen3-ASR-1.7B](https://huggingface.co/Qwen/Qwen3-ASR-1.7B)（較大，但準確率更高）

### 2. 列出音訊設備

```powershell
python src/main.py --list-devices
```

### 3. 執行語音助理

```powershell
# 基本執行
python src/main.py --rules config/rules.json

# 指定音訊設備
python src/main.py --rules config/rules.json --device 0

# 指定運算裝置 (CPU 或 GPU)
python src/main.py --device-type cuda  # 強制 GPU
python src/main.py --device-type cpu   # 強制 CPU
python src/main.py --attention-backend flash_attention_2  # 需相容 CUDA、PyTorch 與 flash-attn 安裝

# 切換語音人聲 (預設 vivian)
python src/main.py --voice random      # 啟動時隨機抽取一個聲音
python src/main.py --voice serena      # 切換為塞雷娜 (女聲)
python src/main.py --voice ryan        # 切換為瑞恩 (男聲)
python src/main.py --voice uncle_fu    # 切換為傅大叔 (特色聲)
# 註：為確保發音標準，已主動隱藏帶有四川與北京口音的方言角色。

# Mock 測試模式（不需要麥克風）
python src/main.py --mock-mode --test "天氣"
```

---

## ⚡ 推論引擎與加速指南 (進階)

我們建議進階使用者或擁有高速 GPU 的開發者安裝 **vLLM** 引擎。這能將語音推論的速度推向極致，解決預設 `transformers` 框架中的迴圈效能瓶頸。

### 為什麼不使用 `.bin` 格式 (CTranslate2 / faster-whisper) 加速？

在早期的計畫或是 Whisper 的使用生態中，通常會透過將模型轉換成 `.bin` 格式，交由 `faster-whisper` (底層依賴於 **CTranslate2 (CT2)**) 來進行極速推理。
* **CTranslate2 (CT2)**：這是一個專為標準 Transformer 架構設計的高效 C++ 推理引擎，特色是就算使用 CPU 也能跑得飛快。
* **無法使用的原因**：我們專案目前採用的是最新世代的 **Qwen3-ASR** 模型。這是一個「具備語音理解能力的大型語言模型變體 (Multimodal LLM)」，其架構不僅龐大，且包含許多特殊的結構 (需要 `trust_remote_code=True` 才能載入)。由於其**不是傳統的 Transformer 結構**，因此 **CTranslate2 目前尚未支援 Qwen3-ASR**。這就是為什麼我們無法像處理標準 Whisper 模型那樣，簡單把它轉成 `.bin` 格式。

### 推論後端狀態

目前程式以 Transformers 相容的 Qwen 封裝執行，尚未整合 vLLM。vLLM 是否支援本專案所用 ASR/TTS pipeline，需依模型與當前版本另外驗證；以下不視為已可使用的專案功能。
1.  vLLM 是大型語言模型推論引擎，但本專案尚未接入，效能收益需實測。
2.  **🌌 PagedAttention 技術**：有效管理 KV Cache 記憶體，降低 OOM 風險。
3.  是否適用 Qwen3-ASR/TTS 應以各模型官方支援範圍為準。
4.  在本專案完成整合與基準測試前，不宣稱已有 vLLM 串流或加速能力。

### 安裝 vLLM

請在虛擬環境 (如 `.venv`) 中執行以下安裝指令：

```powershell
uv pip install vllm
# 或使用標準 pip
# pip install vllm
```

*(註：Windows 上安裝 vLLM 可能需要準備 C++ 建置工具與 CUDA Toolkit，若不熟悉編譯流程，可繼續使用免編譯的預設 Transformers 引擎。)*

---

## 🔧 常見問題

### Q1: WSL 環境無法使用麥克風

**問題**：在 WSL 中執行時顯示 `PortAudioError: Error querying device -1`

**原因**：WSL 預設無法直接存取 Windows 主機的麥克風

**解決方案**：

1. **推薦**：在 Windows 原生環境執行（PowerShell/CMD）
   ```powershell
   cd D:\github\chiisen\voice-activated-assistant.py
   python src\main.py --rules config\rules.json
   ```

2. **或設定 WSL 音訊**（進階）：
   ```bash
   # 在 WSL 中安裝
   sudo apt install libasound2-plugins pulseaudio
   ```

### Q2: `ModuleNotFoundError: No module named 'numpy'`

**解決方案**：
```powershell
# 安裝依賴
pip install -r requirements.txt
# 或
uv sync
```

### Q3: `uv sync` 錯誤 - 存取被拒

**問題**：Windows 檔案權限錯誤

**解決方案**：
```powershell
# 刪除舊的虛擬環境
Remove-Item -Recurse -Force .venv

# 重新安裝
uv sync
```

### Q4: TTS 無法發聲

**檢查**：
1. 確認系統音量已開啟
2. Windows 可用 `pyttsx3`（內建 Edge TTS）
3. Linux 可用 `espeak-ng`（已安裝）

---

## 📖 使用說明

### 指令列選項

| 選項 | 說明 |
|------|------|
| `--rules <path>` | 規則檔路徑（預設：config/rules.json） |
| `--list-devices` | 列出可用音訊設備 |
| `--device <n>` | 指定音訊設備編號 |
| `--mock-mode` | Mock 模式，不需要麥克風 |
| `--test <文字>` | 測試特定關鍵字（自動啟用 mock 模式） |
| `--debug` | 啟用偵錯模式 |

### 規則檔格式

編輯 `config/rules.json` 來新增/修改關鍵字回應：

```json
{
  "rules": [
    {
      "id": "greeting",
      "keywords": ["你好", "hello"],
      "match_mode": "contains",
      "priority": 1,
      "cooldown_s": 2.0,
      "response": {
        "type": "speak_text",
        "text_template": "你好，我是語音助理"
      }
    }
  ]
}
```

---

<!-- [😸SAM] -->
