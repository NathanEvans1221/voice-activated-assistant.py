# Graph Report - voice-activated-assistant.py  (2026-10-04)

## Corpus Check
- 38 files · ~12,576 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 398 nodes · 680 edges · 28 communities (23 shown, 5 thin omitted)
- Extraction: 72% EXTRACTED · 28% INFERRED · 0% AMBIGUOUS · INFERRED: 187 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `cb5c965a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- AudioInput
- TTSJob
- rule_engine.py
- ._audio_callback
- VADSegmenter
- TokenStreamer
- ASRWorker
- 安裝與疑難排解
- AI Agent 指南：GitHub Projects v2 工作流 / AI Agent Guide: GitHub Projects v2 Workflow
- __init__.py
- TODO.md - Voice Activated Assistant
- src/main.py
- bash
- 🤖 Aider 安裝與操作指南 (Windows)
- permission
- Core Requirements (from PRD)
- 🔍 grepai 安裝與操作指南 (Windows)
- [Unreleased]
- AGENTS.md
- voice-activated-assistant-py
- .agent_task_state.md

## God Nodes (most connected - your core abstractions)
1. `TTSJob` - 40 edges
2. `TTSWorker` - 39 edges
3. `ASRWorker` - 34 edges
4. `VADSegmenter` - 31 edges
5. `AudioInput` - 30 edges
6. `RuleEngine` - 28 edges
7. `ASRResult` - 27 edges
8. `Orchestrator` - 27 edges
9. `bash` - 26 edges
10. `AudioConfig` - 25 edges

## Surprising Connections (you probably didn't know these)
- `AttentionBackendTests` --uses--> `TTSWorker`  [INFERRED]
  tests/test_attention_backend.py → src/tts_worker.py
- `AttentionBackendTests` --uses--> `ASRWorker`  [INFERRED]
  tests/test_attention_backend.py → src/asr_worker.py
- `test_yaml_defaults_and_explicit_cli_override()` --calls--> `parse_args()`  [EXTRACTED]
  tests/test_config.py → src/main.py
- `main()` --calls--> `parse_args()`  [EXTRACTED]
  main.py → src/main.py
- `main()` --rationale_for--> `主程式進入點          說明：         此函式是程式的執行起點，負責以下任務：         1. 解析命令列參數`  [EXTRACTED]
  main.py → src/main.py

## Import Cycles
- None detected.

## Communities (28 total, 5 thin omitted)

### Community 0 - "AudioInput"
Cohesion: 0.08
Nodes (41): Enum, AudioConfig, AudioInput, 列出所有可用的音訊裝置 說明： 查詢並顯示系統中所有可用的音訊輸入和輸出裝置。 此函式用於帮助使用者選擇正確的音訊裝置索引。 參數： 無 回傳： 無…, 啟動音訊串流，開始從麥克風擷取音訊 說明： 建立 sounddevice InputStream 並開始錄音。此函式會： 1. 檢查是否有可用的音訊輸入裝置…, 停止音訊串流 說明： 優雅地停止音訊串流並釋放資源。 此函式會： 1. 檢查是否正在執行 2. 停止串流 3. 關閉串流物件 4. 重設執行狀態 參數： 無…, 音訊輸入的組態資料類別 說明： 定義音訊擷取的所有相關參數，包含取樣率、聲道數、資料類型等。 使用 dataclass 提供型別安全且易於擴展的組態管理。…, 檢查音訊串流是否正在執行 參數： 無 回傳： bool: - True: 正在擷取音訊 - False: 已停止 (+33 more)

### Community 1 - "TTSJob"
Cohesion: 0.08
Nodes (24): Event, TTS 任務資料類別 說明： 封裝要送給 TTS Worker 的任務資料。 由 RuleEngine 根據匹配的規則生成。 屬性： rule_id:…, TTSJob, 建構函式 - 建立 TTSWorker 實例          說明：             初始化 TTS Worker，設定模型路徑和回調函式。, 建構函式 - 建立 TTSWorker 實例 說明： 初始化 TTS Worker，設定模型路徑和回調函式。 參數： model_path:…, 檢查是否正在說話          回傳：             bool: True = 正在朗讀, 檢查是否正在說話 回傳： bool: True = 正在朗讀, 取得說話事件物件          說明：             此 Event 會在開始說話時設為 True，說完後設為 False。 (+16 more)

### Community 2 - "rule_engine.py"
Cohesion: 0.18
Nodes (7): 載入規則檔 說明： 從 JSON 檔案讀取規則定義，並轉換為 Rule 物件列表。 載入後會按照 priority 欄位排序。 參數： path:…, 檢查是否需要熱重載 說明： 檢查規則檔是否被修改過，若是則自動重新載入。 這使得使用者可以在程式運行時修改規則而無需重啟。 參數： 無 回傳： bool: -…, 匹配規則 說明： 根據輸入的文字匹配對應的規則。 匹配流程： 1. 先檢查熱重載 2. 將文字加入歷史記錄 3. 遍歷所有規則，檢查關鍵字匹配 4.…, 規則資料類別 說明： 封裝單一規則的所有屬性，包含關鍵字、匹配模式、優先級、冷卻時間等。 屬性： id: str，規則的唯一識別碼 - 用於日誌和追蹤 -…, 檢查關鍵字是否匹配 說明： 根據規則的 match_mode 欄位，選擇合適的匹配方式： - "contains": 檢查關鍵字是否包含在文字中 -…, 生成回應文字 說明： 根據規則的回應類型生成要朗讀的文字： - "speak_text": 回傳 text_template - "speak_kv": 將…, Rule

### Community 3 - "._audio_callback"
Cohesion: 0.33
Nodes (4): CallbackFlags, ndarray, 建構函式 - 建立 AudioInput 實例 說明： 初始化音訊輸入管理器，設定組態和回調函式。 注意：此時尚未啟動音訊串流，必須呼叫 start()…, 音訊資料回調 - sounddevice 每次收到新音訊時呼叫 說明： 此函式由 sounddevice 內部執行緒呼叫，每次有新的音訊區塊時觸發。…

### Community 5 - "VADSegmenter"
Cohesion: 0.11
Nodes (19): ndarray, 語音活動檢測與語句分段器 說明： 負責從連續的音訊流中偵測語音並組合成完整語句。 工作流程： 1. 接收每個音訊框架 (frame) 2.…, 建構函式 - 建立 VADSegmenter 實例 說明： 初始化 VAD 模組，設定組態和回調函式。 參數： config:…, 載入 VAD 模型 說明： 嘗試載入 Silero VAD 模型。 若載入失敗 (缺少依賴套件)，會自動切換到 Simple VAD 模式。 流程： 1.…, 處理單個音訊框架 說明： 這是 VAD 模組的核心函式，每次收到新的音訊資料時呼叫。 職責： 1. 判斷是否為語音 2. 更新緩衝區和狀態 3.…, 簡單能量閾值 VAD 說明： 使用簡單的能量計算來判斷是否為語音。 計算音訊的 RMS (Root Mean Square) 能量， 若超過閾值則視為語音。…, Silero VAD 語音活動檢測 說明： 使用 Silero AI 的預訓練 VAD 模型進行語音偵測。 這是一個深度學習模型，比簡單能量法更精確。 原理：…, 完成語句處理 說明： 當偵測到語句結束時呼叫此函式。 職責： 1. 檢查語句長度是否符合要求 2. 合併緩衝區中的所有片段 3. 建立 Utterance… (+11 more)

### Community 7 - "ASRWorker"
Cohesion: 0.08
Nodes (24): ASRResult, ASRWorker, ndarray, 建構函式 - 建立 ASRWorker 實例          說明：             初始化 ASR Worker，設定模型路徑和回調函式。, 建構函式 - 建立 ASRWorker 實例 說明： 初始化 ASR Worker，設定模型路徑和回調函式。 參數： model_path:…, 啟動 ASR Worker 執行緒          說明：             建立並啟動 worker 執行緒，開始處理任務佇列中的音訊任務。, 啟動 ASR Worker 執行緒 說明： 建立並啟動 worker 執行緒，開始處理任務佇列中的音訊任務。 參數： 無 回傳： 無 設計考量： -…, 停止 ASR Worker          說明：             優雅地停止 worker 執行緒：             1. 設定停止 (+16 more)

### Community 8 - "安裝與疑難排解"
Cohesion: 0.18
Nodes (11): ASR 模型載入失敗, Mock 模式, `No module named 'qwen_asr'`, `No module named 'qwen_tts'`, Python 套件和模型權重是兩回事, `uv sync` 顯示警告, 修改語音規則, 安裝與疑難排解 (+3 more)

### Community 9 - "AI Agent 指南：GitHub Projects v2 工作流 / AI Agent Guide: GitHub Projects v2 Workflow"
Cohesion: 0.07
Nodes (27): 1. 適用情境 / When to Use, 2.1 確認 gh CLI 與授權, 2.2 確認 Token Scopes, 2.3 確認目標 owner 與 repo, 2. 必要前置 / Prerequisites, 3.1 解析來源文件, 3.2 建立 Issues（每大類 1 個 parent）, 3.3 建立 Projects v2 Board (+19 more)

### Community 18 - "TODO.md - Voice Activated Assistant"
Cohesion: 0.05
Nodes (40): 1.1 初始化專案, 1.2 建立專案結構, 1.3 Logging 設定, 2.1 音訊輸入模組, 2.2 VAD 語音偵測, 3.1 ASR Worker, 3.2 Utterance 處理, 4.1 規則系統 (+32 more)

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

## Knowledge Gaps
- **130 isolated node(s):** `$schema`, `read`, `glob`, `grep`, `list` (+125 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `TTSWorker` connect `TTSJob` to `AudioInput`, `ASRWorker`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Why does `ASRWorker` connect `ASRWorker` to `AudioInput`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Why does `VADSegmenter` connect `VADSegmenter` to `AudioInput`, `ASRWorker`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Are the 28 inferred relationships involving `TTSJob` (e.g. with `Orchestrator` and `OrchestratorConfig`) actually correct?**
  _`TTSJob` has 28 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `TTSWorker` (e.g. with `Orchestrator` and `OrchestratorConfig`) actually correct?**
  _`TTSWorker` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `ASRWorker` (e.g. with `Orchestrator` and `OrchestratorConfig`) actually correct?**
  _`ASRWorker` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `VADSegmenter` (e.g. with `Orchestrator` and `OrchestratorConfig`) actually correct?**
  _`VADSegmenter` has 17 INFERRED edges - model-reasoned connections that need verification._