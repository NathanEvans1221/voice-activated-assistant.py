# 安裝與疑難排解

## Python 套件和模型權重是兩回事

- `uv sync --extra asr` 安裝 Qwen ASR 的 Python 執行套件及其依賴；不會重新下載本機模型權重。
- 專案預設從 `models/Qwen3-ASR-0.6B` 載入 ASR 模型。此資料夾由使用者自行準備，模型檔不納入版控。
- 執行啟動命令時，請先切到專案根目錄，因為模型與設定路徑是相對於目前工作目錄。

如果模型已在該資料夾且內容完整，就不必再下載。若尚未準備模型，請從 [Qwen3-ASR-0.6B 模型頁](https://huggingface.co/Qwen/Qwen3-ASR-0.6B)下載檔案，放入上述資料夾。

安裝 ASR 和測試依賴：

```powershell
uv sync --extra asr --extra dev
```

如要確認目前專案虛擬環境能載入套件：

```powershell
.\.venv\Scripts\python.exe -c "import qwen_asr; print('qwen_asr OK')"
```

## 麥克風沒有辨識結果

1. 啟動時不要加 `--mock-mode` 或 `--test`。
2. 執行 `.\.venv\Scripts\python.exe src\main.py --list-devices`，選擇輸入聲道大於 0 的裝置。
3. 用 `--device <裝置編號>` 指定麥克風；省略此參數則使用系統預設輸入。
4. 說完一句後停頓。預設需約 0.8 秒靜音，VAD 才會結束語句並送去辨識；可用 `--silence-duration` 調整。
5. 啟動日誌應看到 `[ASR] 模型載入成功`。只看到「語音助理已就緒」不代表 ASR 模型已成功載入。

## 常見錯誤

### `No module named 'qwen_asr'`

目前執行程式的 Python 環境缺少 ASR 套件。請在專案根目錄執行 `uv sync --extra asr`，並用同一個環境啟動程式。

### ASR 模型載入失敗

確認 `models/Qwen3-ASR-0.6B` 存在且含有完整模型檔，或在 `config/config.yaml` 的 `orchestrator.asr_model_path` 指向實際模型目錄。也可用 `--config` 指定其他 YAML 設定檔。

### `No module named 'qwen_tts'`

這代表 Qwen TTS 套件未安裝。Windows 上程式會嘗試使用 `pyttsx3`，並優先選擇已安裝的中文 SAPI 語音作為備援；這不會造成 ASR 無法辨識。若仍聽不到語音，請確認 Windows 已安裝中文語音，且系統預設播放裝置及音量正常。Qwen ASR 與 TTS extras 有相依版本衝突，請勿在同一環境同時安裝兩者。

若只有第一次備援朗讀有聲，請在專案根目錄執行 `uv sync --extra asr --extra dev`，將環境同步至 lockfile 指定的 `pyttsx3` 相容版本。

### `uv sync` 顯示警告

- `Failed to hardlink`：uv 會改用複製檔案，通常只影響安裝速度。
- `tool.uv.dev-dependencies` 已淘汰：這是專案設定欄位的提醒，不等於安裝失敗。
- 若出現套件無法移除或安裝紀錄缺失，先確認命令結束碼及上述 `qwen_asr` 匯入檢查；仍失敗時保留完整輸出供診斷。

## Mock 模式

`--mock-mode` 會停用麥克風。加上 `--test "天氣"` 時，程式把指定文字直接送入規則流程，並不測試麥克風或真實 ASR。此模式仍會嘗試載入 ASR/TTS worker；它不是免模型啟動模式。

## 修改語音規則

在 `config/rules.json` 修改關鍵字與回應，例如：

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

## 更多設定

`src/main.py --help` 可列出命令列選項。進階推論與效能評估方向記錄在 [TODO](TODO.md)。
