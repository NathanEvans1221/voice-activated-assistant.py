# 語音互動助理

以 Python 建立的本機語音助理：從麥克風接收語音，使用 Qwen3-ASR 轉成文字，再依 JSON 規則產生回應。

模型權重放在本機的 `models/`，不納入版控。若模型已下載完成，不需要重新下載；啟動時仍須在 Python 環境安裝 ASR 執行套件。

## 快速開始（Windows PowerShell）

請在專案根目錄執行：

```powershell
# 安裝 ASR 執行依賴及開發測試依賴
uv sync --extra asr --extra dev

# 列出麥克風，確認要使用的裝置編號
.\.venv\Scripts\python.exe src\main.py --list-devices

# 使用預設麥克風啟動
.\.venv\Scripts\python.exe src\main.py --rules config\rules.json
```

如需指定麥克風，將下方的 `1` 換成清單中的輸入裝置編號：

```powershell
.\.venv\Scripts\python.exe src\main.py --rules config\rules.json --device 1
```

說完一句後停頓約 0.8 秒，程式就會送出整句辨識。按 `Ctrl+C` 停止。

## 執行測試

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## 文件

- [安裝、模型、麥克風與常見問題](docs/TROUBLESHOOTING.md)：說明套件與本機模型的差異、ASR/TTS 設定及排錯方式。
- [產品需求文件](docs/PRD.md)
- [專案待辦](docs/project_tasks.md)
- [效能與推論評估](docs/TODO.md)

> `--mock-mode --test "天氣"` 是文字模擬，不會讀取麥克風；詳情請看疑難排解文件。
