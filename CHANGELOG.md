# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- 新增安裝與疑難排解指南，說明 Python 套件、本機模型權重、麥克風與 Mock 模式。
- 接通 `--config` YAML 載入，CLI 明確參數優先；新增設定檔結構與數值驗證及回歸測試。
- 將 Qwen ASR/TTS 設為互斥的 uv extras，避免其固定 Transformers 版本衝突。
- 限定 pytest 從 `tests/` 收集測試，避免執行模型探索腳本。
- 新增 `--attention-backend` 選項，可為 Qwen ASR/TTS 選擇 SDPA 或 Flash Attention 2；預設使用 SDPA。
- 記錄 Qwen 量化及 TensorRT/ONNX 的環境限制與可行性評估方向。
- 建立 `PRD.md`：定義語音互動助理的核心規格，包含 ASR/TTS 多執行緒、VAD 停頓偵測及記憶體管理邏輯。

### Changed
- 將 VAD 預設靜音等待由 1.5 秒縮短為 0.8 秒，停頓後更快送出語音辨識。
- 修正 Windows `pyttsx3` 備援引擎的執行緒歸屬，改由 TTS Worker 執行緒初始化，避免朗讀卡住後持續丟棄麥克風音訊。
- 精簡 README 快速開始，分清 ASR 套件安裝、本機模型路徑、真實麥克風啟動與測試指令。
- 修正 ASR Worker 停止與重啟期間的執行緒生命週期競態；停止會等待執行中辨識、丟棄排隊音訊與停止後結果，並新增 2 項回歸測試。
- 修正 VAD 長語句緩衝無上限與 callback 重入死鎖，保留短停頓並依樣本數強制切段；新增連續 30 次語句與超長框架回歸測試。
- 直接查證 RTX 3070 Laptop GPU，修正將 CPU 版 PyTorch 誤認為無 GPU 的環境紀錄；補做 Graphify 程式圖譜重建。
- 優化 `PRD.md` 標題與前言描述，使其符合專業文件規範。
- 重新編寫 `README.md`，包含豐富的專案簡介與 Mermaid 核心流程圖。
- 在 `README.md` 新增「開發進度」區塊並連結至 `TODO.md`。
- 在 `README.md` 新增 WSL 環境限制說明，建議使用 Windows 原生環境執行。
- 整合 Qwen3-ASR (0.6B) 模型，實現高性能本地端語音識別。
- 整合 Qwen3-TTS (0.6B) 模型，支援本地端語音合成與直接音訊播放。
- 使用 `uv` 修復 Python 虛擬環境，補齊 `numpy`, `torch`, `qwen-tts`, `qwen-asr` 等依賴套件。
- 修正 Qwen3 ASR/TTS 模型載入與推論介面，優化 VAD 判定邏輯，達成秒級響應。





