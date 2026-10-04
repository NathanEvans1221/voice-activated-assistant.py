# Graph Report - voice-activated-assistant.py  (2026-10-04)

## Corpus Check
- 40 files · ~13,161 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 412 nodes · 699 edges · 38 communities (24 shown, 14 thin omitted)
- Extraction: 73% EXTRACTED · 27% INFERRED · 0% AMBIGUOUS · INFERRED: 187 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `315fae62`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- TTSJob
- ._speak_streaming
- RuleEngine
- ._audio_callback
- .process_frame
- TokenStreamer
- ASRWorker
- 安裝與疑難排解
- AI Agent 指南：GitHub Projects v2 工作流 / AI Agent Guide: GitHub Projects v2 Workflow
- test_vad.py
- __init__.py
- TODO.md - Voice Activated Assistant
- ._load_fallback_engine
- parse_args
- bash
- 🤖 Aider 安裝與操作指南 (Windows)
- permission
- Core Requirements (from PRD)
- 🔍 grepai 安裝與操作指南 (Windows)
- [Unreleased]
- .stop
- .frame_samples
- .is_running
- AGENTS.md
- .list_devices
- .start
- .stop
- .is_speaking
- voice-activated-assistant-py
- .load_vad
- .agent_task_state.md

## God Nodes (most connected - your core abstractions)
1. `TTSJob` - 40 edges
2. `TTSWorker` - 40 edges
3. `ASRWorker` - 34 edges
4. `RuleEngine` - 32 edges
5. `VADSegmenter` - 31 edges
6. `AudioInput` - 30 edges
7. `ASRResult` - 27 edges
8. `Orchestrator` - 27 edges
9. `bash` - 26 edges
10. `AudioConfig` - 25 edges

## Surprising Connections (you probably didn't know these)
- `AttentionBackendTests` --uses--> `TTSWorker`  [INFERRED]
  tests/test_attention_backend.py → src/tts_worker.py
- `main()` --rationale_for--> `主程式進入點          說明：         此函式是程式的執行起點，負責以下任務：         1. 解析命令列參數`  [EXTRACTED]
  main.py → src/main.py
- `test_stop_waits_for_inflight_recognition_and_suppresses_late_result()` --calls--> `ASRResult`  [EXTRACTED]
  tests/test_asr_worker_lifecycle.py → src/asr_worker.py
- `test_worker_restarts_after_stop_and_discards_queued_audio()` --calls--> `ASRResult`  [EXTRACTED]
  tests/test_asr_worker_lifecycle.py → src/asr_worker.py
- `AttentionBackendTests` --uses--> `ASRWorker`  [INFERRED]
  tests/test_attention_backend.py → src/asr_worker.py

## Import Cycles
- None detected.

## Communities (38 total, 14 thin omitted)

### Community 0 - "TTSJob"
Cohesion: 0.11
Nodes (53): Enum, Logger, ASRResult, 語音辨識結果資料類別 說明： 封裝語音辨識的結果，包含識別出的文字及其他相關資訊。 屬性： transcript: str，識別出的文字內容 -…, AudioConfig, AudioInput, 音訊輸入的組態資料類別 說明： 定義音訊擷取的所有相關參數，包含取樣率、聲道數、資料類型等。 使用 dataclass 提供型別安全且易於擴展的組態管理。…, 音訊輸入管理器 說明： 負責與系統音訊驅動互動，從麥克風即時擷取音訊資料。 使用 sounddevice 的串流 (Stream) 機制實現低延遲的音訊處理。… (+45 more)

### Community 1 - "._speak_streaming"
Cohesion: 0.11
Nodes (12): Event, 建構函式 - 建立 TTSWorker 實例          說明：             初始化 TTS Worker，設定模型路徑和回調函式。, 建構函式 - 建立 TTSWorker 實例 說明： 初始化 TTS Worker，設定模型路徑和回調函式。 參數： model_path:…, 取得說話事件物件 說明： 此 Event 會在開始說話時設為 True，說完後設為 False。 其他模組 (如 Orchestrator)…, 啟動 TTS Worker 執行緒 說明： 建立並啟動 worker 執行緒，開始處理任務佇列中的朗讀任務。 參數： 無 回傳： 無, 啟動 TTS Worker 執行緒          說明：             建立並啟動 worker 執行緒，開始處理任務佇列中的朗讀任務。, Worker 執行緒主迴圈 說明： 1. 從任務佇列取出朗讀任務 2. 將任務拆分為多個子句 (Streaming 基礎) 3.…, Worker 執行緒主迴圈          說明：             1. 從任務佇列取出朗讀任務             2. 將任務拆分為多 (+4 more)

### Community 2 - "RuleEngine"
Cohesion: 0.10
Nodes (16): 規則引擎 說明： 負責管理所有規則的生命週期和匹配邏輯。 核心功能： 1. 從 JSON 檔案載入規則 2. 根據輸入文字匹配對應規則 3. 支援熱重載…, 建構函式 - 建立 RuleEngine 實例 說明： 初始化規則引擎，設定規則檔路徑。 參數： rules_path: Optional[str]，規則…, 載入規則檔 說明： 從 JSON 檔案讀取規則定義，並轉換為 Rule 物件列表。 載入後會按照 priority 欄位排序。 參數： path:…, 檢查是否需要熱重載 說明： 檢查規則檔是否被修改過，若是則自動重新載入。 這使得使用者可以在程式運行時修改規則而無需重啟。 參數： 無 回傳： bool: -…, 匹配規則 說明： 根據輸入的文字匹配對應的規則。 匹配流程： 1. 先檢查熱重載 2. 將文字加入歷史記錄 3. 遍歷所有規則，檢查關鍵字匹配 4.…, 規則資料類別 說明： 封裝單一規則的所有屬性，包含關鍵字、匹配模式、優先級、冷卻時間等。 屬性： id: str，規則的唯一識別碼 - 用於日誌和追蹤 -…, 檢查關鍵字是否匹配 說明： 根據規則的 match_mode 欄位，選擇合適的匹配方式： - "contains": 檢查關鍵字是否包含在文字中 -…, 生成回應文字 說明： 根據規則的回應類型生成要朗讀的文字： - "speak_text": 回傳 text_template - "speak_kv": 將… (+8 more)

### Community 3 - "._audio_callback"
Cohesion: 0.33
Nodes (4): CallbackFlags, ndarray, 建構函式 - 建立 AudioInput 實例 說明： 初始化音訊輸入管理器，設定組態和回調函式。 注意：此時尚未啟動音訊串流，必須呼叫 start()…, 音訊資料回調 - sounddevice 每次收到新音訊時呼叫 說明： 此函式由 sounddevice 內部執行緒呼叫，每次有新的音訊區塊時觸發。…

### Community 5 - ".process_frame"
Cohesion: 0.19
Nodes (7): ndarray, 處理單個音訊框架 說明： 這是 VAD 模組的核心函式，每次收到新的音訊資料時呼叫。 職責： 1. 判斷是否為語音 2. 更新緩衝區和狀態 3.…, 簡單能量閾值 VAD 說明： 使用簡單的能量計算來判斷是否為語音。 計算音訊的 RMS (Root Mean Square) 能量， 若超過閾值則視為語音。…, Silero VAD 語音活動檢測 說明： 使用 Silero AI 的預訓練 VAD 模型進行語音偵測。 這是一個深度學習模型，比簡單能量法更精確。 原理：…, 完成語句處理 說明： 當偵測到語句結束時呼叫此函式。 職責： 1. 檢查語句長度是否符合要求 2. 合併緩衝區中的所有片段 3. 建立 Utterance…, 重設內部狀態 說明： 清空緩衝區並重設所有計時器和狀態變數。 用於語句完成後或需要重新開始時。 參數： 無, 公開的重設函式 說明： 提供給外部呼叫的重設接口。 會先取得鎖再重設，確保執行緒安全。 參數： 無

### Community 7 - "ASRWorker"
Cohesion: 0.06
Nodes (23): ASRWorker, ndarray, 建構函式 - 建立 ASRWorker 實例          說明：             初始化 ASR Worker，設定模型路徑和回調函式。, 建構函式 - 建立 ASRWorker 實例 說明： 初始化 ASR Worker，設定模型路徑和回調函式。 參數： model_path:…, 啟動 ASR Worker 執行緒          說明：             建立並啟動 worker 執行緒，開始處理任務佇列中的音訊任務。, 啟動 ASR Worker 執行緒 說明： 建立並啟動 worker 執行緒，開始處理任務佇列中的音訊任務。 參數： 無 回傳： 無 設計考量： -…, 停止 ASR Worker          說明：             優雅地停止 worker 執行緒：             1. 設定停止, 停止 ASR Worker 說明： 優雅地停止 worker 執行緒： 1. 設定停止標記 2. 傳送 None 到佇列，觸發 worker 結束 3.… (+15 more)

### Community 8 - "安裝與疑難排解"
Cohesion: 0.06
Nodes (30): Windows 麥克風有辨識結果，但後續 TTS 沒有聲音, 修正與驗證, 症狀, 維護經驗, 避免回歸, 除錯證據與根因, 1. 演算法級加速：Flash Attention, 2. 模型尺寸優化：模型量化 (Quantization) (+22 more)

### Community 9 - "AI Agent 指南：GitHub Projects v2 工作流 / AI Agent Guide: GitHub Projects v2 Workflow"
Cohesion: 0.07
Nodes (27): 1. 適用情境 / When to Use, 2.1 確認 gh CLI 與授權, 2.2 確認 Token Scopes, 2.3 確認目標 owner 與 repo, 2. 必要前置 / Prerequisites, 3.1 解析來源文件, 3.2 建立 Issues（每大類 1 個 parent）, 3.3 建立 Projects v2 Board (+19 more)

### Community 12 - "test_vad.py"
Cohesion: 0.52
Nodes (6): make_vad(), test_callback_can_reset_without_deadlock(), test_continuous_speech_is_emitted_without_waiting_for_silence(), test_oversized_frame_splits_without_losing_samples(), test_short_pause_is_preserved_in_audio(), test_too_short_speech_is_discarded_and_next_sentence_starts_clean()

### Community 18 - "TODO.md - Voice Activated Assistant"
Cohesion: 0.07
Nodes (27): 1.1 初始化專案, 1.2 建立專案結構, 1.3 Logging 設定, 2.1 音訊輸入模組, 2.2 VAD 語音偵測, 3.1 ASR Worker, 3.2 Utterance 處理, 4.1 規則系統 (+19 more)

### Community 20 - "parse_args"
Cohesion: 0.23
Nodes (9): main(), load_defaults(), Load validated YAML defaults for the command-line entry point., validate_options(), parse_args(), 解析命令列參數 說明： 此函式使用 argparse 模組解析命令列參數，讓使用者可以自訂程式行為， 包括設定配置檔路徑、除錯模式、音訊裝置選擇等。 參數：…, parametrize, test_invalid_config_fails_before_model_start() (+1 more)

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

## Knowledge Gaps
- **134 isolated node(s):** `$schema`, `read`, `glob`, `grep`, `list` (+129 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `TTSWorker` connect `TTSJob` to `._speak_streaming`, `RuleEngine`, `.is_speaking`, `ASRWorker`, `._load_fallback_engine`, `.stop`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **Why does `ASRWorker` connect `ASRWorker` to `TTSJob`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Why does `VADSegmenter` connect `TTSJob` to `test_vad.py`, `.process_frame`, `.load_vad`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Are the 28 inferred relationships involving `TTSJob` (e.g. with `Orchestrator` and `OrchestratorConfig`) actually correct?**
  _`TTSJob` has 28 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `TTSWorker` (e.g. with `Orchestrator` and `OrchestratorConfig`) actually correct?**
  _`TTSWorker` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `ASRWorker` (e.g. with `Orchestrator` and `OrchestratorConfig`) actually correct?**
  _`ASRWorker` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `RuleEngine` (e.g. with `Orchestrator` and `OrchestratorConfig`) actually correct?**
  _`RuleEngine` has 17 INFERRED edges - model-reasoned connections that need verification._