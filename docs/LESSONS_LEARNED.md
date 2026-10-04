# 維護經驗

本文件記錄已由使用者實際驗證、可供後續維護者重用的問題根因與修正。新增經驗時保留症狀、證據、根因、修正和驗證結果；不要把尚未驗證的猜測寫成結論。

## Windows 麥克風有辨識結果，但後續 TTS 沒有聲音

### 症狀

- 麥克風輸入可被 VAD 偵測，ASR 有文字，規則也成功觸發。
- 啟動時只聽得到第一段「正在熱身」；後續招呼語與規則回覆沒有聲音。
- 日誌仍顯示 `pyttsx3` 的 `runAndWait()` 已完成，沒有錯誤。

### 除錯證據與根因

1. 依序檢查音訊輸入、VAD、ASR、規則、TTS 日誌。看到 VAD/ASR 文字及規則觸發後，可先排除麥克風和辨識鏈路。
2. `runAndWait()` 返回只代表程式呼叫結束，不能證明實際喇叭有輸出。
3. 使用者環境安裝 `pyttsx3 2.99`。其 Windows SAPI5 有「第一次朗讀有聲，後續呼叫正常返回但靜音」的已知問題：[上游 issue #419](https://github.com/nateshmbhat/pyttsx3/issues/419)。
4. 早期暖身階段的 TTS 卡住另有執行緒歸屬問題：SAPI 引擎在主執行緒建立、在 TTS Worker 使用。引擎應在實際使用它的 Worker 執行緒初始化。

### 修正與驗證

- `pyproject.toml` 將 `pyttsx3` 限制為 `>=2.90,<2.99`，`uv.lock` 鎖定 `2.98`；更新套件環境需執行：

  ```powershell
  uv sync --extra asr
  .\.venv\Scripts\python.exe -c "from importlib.metadata import version; print(version('pyttsx3'))"
  ```

  版本應為 `2.98`。這只同步 Python 套件，不會下載本機 Qwen 模型權重。
- Windows 備援引擎在 TTS Worker 執行緒初始化，優先選擇已安裝的中文 SAPI 語音（此電腦為 Microsoft Hanhan zh-TW）。
- 系統 TTS 備援保留繁體原文；OpenCC 簡繁轉換只用於 Qwen TTS。
- 使用者同步至 `2.98` 後，確認麥克風辨識、規則回覆與語音輸出皆正常。單元測試覆蓋 Worker 執行緒初始化和中文語音選擇；實際喇叭輸出仍須在 Windows 實機確認。

### 避免回歸

- 不要只根據 `[TTS] 播放完成` 判定有聲音；讓使用者確認暖身、啟動招呼和後續規則回覆都聽得到。
- 升級 `pyttsx3` 前，先在 Windows 對同一引擎連續呼叫多次 `say()`／`runAndWait()`，確認每一段都有聲音。
- 保留 `tests/test_tts_fallback.py`、`tests/test_config.py`、`tests/test_vad.py`，並以 lockfile 和 `uv lock --check` 管理依賴版本。
- VAD 的 `silence_duration` 是辨識前的停頓等待時間；它不會修復 TTS 靜音。專案預設為 0.8 秒，兩類問題要分開診斷。
