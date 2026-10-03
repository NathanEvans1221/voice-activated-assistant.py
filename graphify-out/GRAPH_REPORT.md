# Graph Report - voice-activated-assistant.py  (2026-10-04)

## Corpus Check
- 34 files · ~12,373 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 390 nodes · 652 edges · 42 communities (24 shown, 18 thin omitted)
- Extraction: 71% EXTRACTED · 29% INFERRED · 0% AMBIGUOUS · INFERRED: 188 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `aced5b7b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- TTSJob
- ._speak_streaming
- .__init__
- ._audio_callback
- Orchestrator
- .process_frame
- TokenStreamer
- ._recognize
- 🎙️ 語音互動助理 (Voice-Activated Assistant)
- AI Agent 指南：GitHub Projects v2 工作流 / AI Agent Guide: GitHub Projects v2 Workflow
- .load_vad
- __init__.py
- TODO.md - Voice Activated Assistant
- .frame_samples
- src/main.py
- bash
- 🤖 Aider 安裝與操作指南 (Windows)
- permission
- Core Requirements (from PRD)
- 🔍 grepai 安裝與操作指南 (Windows)
- [Unreleased]
- .__init__
- .start
- .stop
- AGENTS.md
- .is_running
- .list_devices
- .start
- .stop
- .get_history
- .is_speaking
- voice-activated-assistant-py
- .match
- .stop
- .agent_task_state.md

## God Nodes (most connected - your core abstractions)
1. `TTSJob` - 39 edges
2. `TTSWorker` - 37 edges
3. `ASRWorker` - 31 edges
4. `AudioInput` - 30 edges
5. `VADSegmenter` - 29 edges
6. `RuleEngine` - 28 edges
7. `Orchestrator` - 27 edges
8. `bash` - 26 edges
9. `AudioConfig` - 25 edges
10. `ASRResult` - 24 edges

## Surprising Connections (you probably didn't know these)
- `AttentionBackendTests` --uses--> `ASRWorker`  [INFERRED]
  tests/test_attention_backend.py → src/asr_worker.py
- `test_yaml_defaults_and_explicit_cli_override()` --calls--> `parse_args()`  [EXTRACTED]
  tests/test_config.py → src/main.py
- `TTSJob` --uses--> `建構函式 - 建立 TTSWorker 實例          說明：             初始化 TTS Worker，設定模型路徑和回調函式。`  [INFERRED]
  src/rule_engine.py → src/tts_worker.py
- `TTSJob` --uses--> `啟動 TTS Worker 執行緒          說明：             建立並啟動 worker 執行緒，開始處理任務佇列中的朗讀任務。`  [INFERRED]
  src/rule_engine.py → src/tts_worker.py
- `TTSJob` --uses--> `停止 TTS Worker          說明：             優雅地停止 worker 執行緒。          參數：`  [INFERRED]
  src/rule_engine.py → src/tts_worker.py

## Import Cycles
- None detected.

## Communities (42 total, 18 thin omitted)

### Community 0 - "TTSJob"
Cohesion: 0.13
Nodes (44): Enum, ASRResult, ASRWorker, 語音辨識結果資料類別 說明： 封裝語音辨識的結果，包含識別出的文字及其他相關資訊。 屬性： transcript: str，識別出的文字內容 -…, 語音辨識工作者 說明： 負責將音訊資料轉換為文字的 worker 模組。 使用執行緒和佇列實現非同步處理： - 主執行緒透過 process()…, AudioConfig, AudioInput, 音訊輸入的組態資料類別 說明： 定義音訊擷取的所有相關參數，包含取樣率、聲道數、資料類型等。 使用 dataclass 提供型別安全且易於擴展的組態管理。… (+36 more)

### Community 1 - "._speak_streaming"
Cohesion: 0.12
Nodes (11): Event, 建構函式 - 建立 TTSWorker 實例          說明：             初始化 TTS Worker，設定模型路徑和回調函式。, 建構函式 - 建立 TTSWorker 實例 說明： 初始化 TTS Worker，設定模型路徑和回調函式。 參數： model_path:…, 取得說話事件物件 說明： 此 Event 會在開始說話時設為 True，說完後設為 False。 其他模組 (如 Orchestrator)…, 啟動 TTS Worker 執行緒          說明：             建立並啟動 worker 執行緒，開始處理任務佇列中的朗讀任務。, 啟動 TTS Worker 執行緒 說明： 建立並啟動 worker 執行緒，開始處理任務佇列中的朗讀任務。 參數： 無 回傳： 無, Worker 執行緒主迴圈          說明：             1. 從任務佇列取出朗讀任務             2. 將任務拆分為多, Worker 執行緒主迴圈 說明： 1. 從任務佇列取出朗讀任務 2. 將任務拆分為多個子句 (Streaming 基礎) 3.… (+3 more)

### Community 3 - "._audio_callback"
Cohesion: 0.33
Nodes (4): CallbackFlags, ndarray, 建構函式 - 建立 AudioInput 實例 說明： 初始化音訊輸入管理器，設定組態和回調函式。 注意：此時尚未啟動音訊串流，必須呼叫 start()…, 音訊資料回調 - sounddevice 每次收到新音訊時呼叫 說明： 此函式由 sounddevice 內部執行緒呼叫，每次有新的音訊區塊時觸發。…

### Community 4 - "Orchestrator"
Cohesion: 0.12
Nodes (12): Orchestrator, 語音助理的核心協調器 說明： Orchestrator 是整個語音助理的心臟，負責： 1. 管理所有子模組的生命週期 (初始化、起動、停止) 2.…, 取得目前系統狀態 (執行緒安全) 說明： 使用 Lock 保護 _state 變數，確保在多執行緒環境下 讀取狀態不會取得不一致的結果。 參數： 無 回傳：…, 設定系統狀態 (執行緒安全) 說明： 使用 Lock 保護 _state 變數，確保在多執行緒環境下 設定狀態不會產生競爭條件。 參數： new_state:…, 啟動 Orchestrator 和所有子模組 說明： 此函式負責起動所有子模組並將系統狀態設為 LISTENING。 執行順序： 1. 載入規則檔…, AI 模型熱身 透過執行一次隱藏推論來初始化 CUDA 快取與相關運算資源, 停止 Orchestrator 和所有子模組 說明： 此函式負責優雅地停止所有子模組： 1. 停止 AudioInput (停止擷取音訊) 2. 停止 ASR…, 音訊框架回調 - 處理每個新的音訊資料塊 說明： 此函式由 AudioInput 在收到新的音訊框架時呼叫。 它會： 1. 檢查 TTS 是否正在說話… (+4 more)

### Community 5 - ".process_frame"
Cohesion: 0.19
Nodes (7): ndarray, 處理單個音訊框架 說明： 這是 VAD 模組的核心函式，每次收到新的音訊資料時呼叫。 職責： 1. 判斷是否為語音 2. 更新緩衝區和狀態 3.…, 簡單能量閾值 VAD 說明： 使用簡單的能量計算來判斷是否為語音。 計算音訊的 RMS (Root Mean Square) 能量， 若超過閾值則視為語音。…, Silero VAD 語音活動檢測 說明： 使用 Silero AI 的預訓練 VAD 模型進行語音偵測。 這是一個深度學習模型，比簡單能量法更精確。 原理：…, 完成語句處理 說明： 當偵測到語句結束時呼叫此函式。 職責： 1. 檢查語句長度是否符合要求 2. 合併緩衝區中的所有片段 3. 建立 Utterance…, 重設內部狀態 說明： 清空緩衝區並重設所有計時器和狀態變數。 用於語句完成後或需要重新開始時。 參數： 無, 公開的重設函式 說明： 提供給外部呼叫的重設接口。 會先取得鎖再重設，確保執行緒安全。 參數： 無

### Community 7 - "._recognize"
Cohesion: 0.20
Nodes (7): ndarray, 提交音訊進行辨識          說明：             將音訊資料加入任務佇列，等待 worker 執行緒處理。             這, 提交音訊進行辨識 說明： 將音訊資料加入任務佇列，等待 worker 執行緒處理。 這是非同步操作，函式會立即返回。 參數： audio:…, Worker 執行緒主迴圈          說明：             在獨立執行緒中運行的主要工作迴圈：             1. 從輸入佇, Worker 執行緒主迴圈 說明： 在獨立執行緒中運行的主要工作迴圈： 1. 從輸入佇列取出音訊任務 2. 若收到 None，則結束迴圈 3. 呼叫…, 執行實際的語音辨識          說明：             這是核心的辨識函式，目前為預留實作：             - 若模型未載入，回, 執行實際的語音辨識 說明： 這是核心的辨識函式，目前為預留實作： - 若模型未載入，回傳錯誤訊息 - 若已載入模型，應調用模型進行推論 參數： audio:…

### Community 8 - "🎙️ 語音互動助理 (Voice-Activated Assistant)"
Cohesion: 0.06
Nodes (30): 1. 演算法級加速：Flash Attention, 2. 模型尺寸優化：模型量化 (Quantization), 3. 硬體級加速：TensorRT / ONNX 轉換, 📅 未來發展方向, 🛠️ 核心優化任務清單, 🧠 為什麼不優先更換程式語言 (Python vs. Rust/Go)？, 🚀 語音助理效能優化藍圖 (Performance Optimization Roadmap), 🚀 進行中與已完成優化 (+22 more)

### Community 9 - "AI Agent 指南：GitHub Projects v2 工作流 / AI Agent Guide: GitHub Projects v2 Workflow"
Cohesion: 0.07
Nodes (27): 1. 適用情境 / When to Use, 2.1 確認 gh CLI 與授權, 2.2 確認 Token Scopes, 2.3 確認目標 owner 與 repo, 2. 必要前置 / Prerequisites, 3.1 解析來源文件, 3.2 建立 Issues（每大類 1 個 parent）, 3.3 建立 Projects v2 Board (+19 more)

### Community 18 - "TODO.md - Voice Activated Assistant"
Cohesion: 0.07
Nodes (27): 1.1 初始化專案, 1.2 建立專案結構, 1.3 Logging 設定, 2.1 音訊輸入模組, 2.2 VAD 語音偵測, 3.1 ASR Worker, 3.2 Utterance 處理, 4.1 規則系統 (+19 more)

### Community 20 - "src/main.py"
Cohesion: 0.15
Nodes (16): Logger, main(), parametrize, load_defaults(), Load validated YAML defaults for the command-line entry point., validate_options(), get_logger(), Logging configuration module (+8 more)

### Community 21 - "bash"
Cohesion: 0.08
Nodes (26): cat *, cp *, dd *, del *, echo *, format *, git add *, git branch * (+18 more)

### Community 22 - "🤖 Aider 安裝與操作指南 (Windows)"
Cohesion: 0.12
Nodes (16): 1. 📥 安裝 Aider, 2. 🔑 設定 API Key (以 OpenAI 或 Anthropic 為例), 3. 🚀 開始結對程式設計 (Pair Programming), 4. 💬 常用指令與操作邏輯, 5. 🤝 AI 代理人如何與 Aider 協作？, 6. 💡 Aider 為什麼對寫程式超級有幫助？, 🤖 Aider 安裝與操作指南 (Windows), 🗺️ Codebase 索引與專案地圖 (Repo Map) (+8 more)

### Community 23 - "permission"
Cohesion: 0.12
Nodes (16): permission, cargo, date, dir, echo, edit, glob, grep (+8 more)

### Community 24 - "Core Requirements (from PRD)"
Cohesion: 0.15
Nodes (12): 1. Audio Pipeline, 2. ASR (Automatic Speech Recognition), 3. Rule Engine, 4. TTS (Text-to-Speech), 5. State Machine, 6. Memory & Privacy, Core Requirements (from PRD), Draft: Voice Activated Assistant Plan (+4 more)

### Community 25 - "🔍 grepai 安裝與操作指南 (Windows)"
Cohesion: 0.25
Nodes (7): 1. 📥 安裝 grepai, 2. 🤖 準備本地模型 (Ollama), 3. ⚙️ 初始化你的專案, 4. 👁️ 啟動「索引監聽」 Daemon, 5. 🔍 執行自然語言語意搜尋, 🔍 grepai 安裝與操作指南 (Windows), 💡 核心工作流總結

### Community 26 - "[Unreleased]"
Cohesion: 0.40
Nodes (4): Added, Changed, Changelog, [Unreleased]

### Community 39 - ".match"
Cohesion: 0.20
Nodes (7): 載入規則檔 說明： 從 JSON 檔案讀取規則定義，並轉換為 Rule 物件列表。 載入後會按照 priority 欄位排序。 參數： path:…, 檢查是否需要熱重載 說明： 檢查規則檔是否被修改過，若是則自動重新載入。 這使得使用者可以在程式運行時修改規則而無需重啟。 參數： 無 回傳： bool: -…, 匹配規則 說明： 根據輸入的文字匹配對應的規則。 匹配流程： 1. 先檢查熱重載 2. 將文字加入歷史記錄 3. 遍歷所有規則，檢查關鍵字匹配 4.…, 規則資料類別 說明： 封裝單一規則的所有屬性，包含關鍵字、匹配模式、優先級、冷卻時間等。 屬性： id: str，規則的唯一識別碼 - 用於日誌和追蹤 -…, 檢查關鍵字是否匹配 說明： 根據規則的 match_mode 欄位，選擇合適的匹配方式： - "contains": 檢查關鍵字是否包含在文字中 -…, 生成回應文字 說明： 根據規則的回應類型生成要朗讀的文字： - "speak_text": 回傳 text_template - "speak_kv": 將…, Rule

## Knowledge Gaps
- **135 isolated node(s):** `$schema`, `read`, `glob`, `grep`, `list` (+130 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ASRWorker` connect `TTSJob` to `Orchestrator`, `._recognize`, `.__init__`, `.start`, `.stop`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Why does `TTSWorker` connect `TTSJob` to `.stop`, `._speak_streaming`, `Orchestrator`, `.is_speaking`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Why does `Orchestrator` connect `Orchestrator` to `TTSJob`, `src/main.py`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Are the 29 inferred relationships involving `TTSJob` (e.g. with `Orchestrator` and `OrchestratorConfig`) actually correct?**
  _`TTSJob` has 29 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `TTSWorker` (e.g. with `Orchestrator` and `OrchestratorConfig`) actually correct?**
  _`TTSWorker` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `ASRWorker` (e.g. with `Orchestrator` and `OrchestratorConfig`) actually correct?**
  _`ASRWorker` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `AudioInput` (e.g. with `主程式進入點          說明：         此函式是程式的執行起點，負責以下任務：         1. 解析命令列參數` and `Orchestrator`) actually correct?**
  _`AudioInput` has 18 INFERRED edges - model-reasoned connections that need verification._