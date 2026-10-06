# 🚀 語音助理效能優化藍圖 (Performance Optimization Roadmap)

> [!NOTE]
> 本文件記錄了關於提升語音助理反應速度的深度分析與後續優化任務。目前的效能瓶頸主要在於 **GPU 模型推理**，而非程式語言本身。

## GitHub Issue 追蹤

- 本優化工作由 GitHub CLI（`gh`）建立：[Issue #1：規劃並驗證語音助理效能與服務化優化](https://github.com/chiisen/voice-activated-assistant.py/issues/1)。
- Issue #1 與本文件同步追蹤效能基準、Attention、量化、ONNX／TensorRT、ASR／TTS 部署、WebSocket、LLM 與儀表板工作。
- Issue 保持開啟，直到下方未完成項目實際完成或記錄不採用的理由；完成後再關閉 issue，避免 GitHub 與 TODO 狀態不一致。
- [x] 環境盤點記錄於 [docs/PERFORMANCE_BASELINE.md](PERFORMANCE_BASELINE.md)；本機 RTX 3070 存在，但目前 `.venv` 使用 CPU-only PyTorch。
- [x] 保存固定 ASR 音訊／參考句及 TTS 招呼語；完成 CUDA/SDPA ASR、TTS 單模型載入與推論基準，包含 CER、首音、完整生成、顯存及 TTS 輸出 WAV；詳見 `docs/PERFORMANCE_BASELINE.md` 與 `docs/performance-results/`。
- [ ] 比較 ASR/TTS 個別與同時載入的顯存／延遲，並評估相同環境與獨立環境部署方案；TTS 聽感自然度仍待人工評分。

---

## 🧠 為什麼不優先更換程式語言 (Python vs. Rust/Go)？

在目前的架構中，Python 僅作為「指揮官」角色，實際的運算（ASR 與 TTS）是由底層的 **C++/CUDA** 核心在 GPU 上執行。
*   **瓶頸點**：95% 的時間花在 GPU 的矩陣運算，而非 Python 的邏輯執行。
*   **更換語言的代價**：換成 Rust/Go 會失去 Python 豐富的 AI 生態系支援，且對 GPU 推理速度的提升微乎其微（僅能節省幾毫秒的指令傳遞時間）。

---

## 🛠️ 核心優化任務清單

### 1. 演算法級加速：Flash Attention
- [x] 提供 `--attention-backend`，可選擇 SDPA 或 Flash Attention 2，並傳入 Qwen ASR/TTS loader；預設使用 SDPA。
- [ ] 比較 CUDA SDPA 與 Flash Attention 2 的速度、顯存與輸出品質。目前兩套 CUDA 測試環境均無 `flash_attn`；Windows 主機缺少 `nvcc`／MSVC `cl`，且官方將 Windows 編譯列為仍需更多測試。先取得可信且版本匹配的 wheel，或改用 Linux/WSL CUDA 環境；詳見 `docs/PERFORMANCE_BASELINE.md`。

### 2. 模型尺寸優化：模型量化 (Quantization)
- [x] 在隔離 CUDA 環境完成 ASR INT8 單樣本探測：CER 0.000、暖機平均 8.635 秒，較 BF16 基準 0.599 秒慢約 14.4 倍；峰值顯存降低。結果與限制見 `docs/PERFORMANCE_BASELINE.md` 及 `docs/performance-results/asr_cuda_bnb_int8_auto.json`。
- [ ] 評估 ASR INT4、TTS INT8/INT4 與更多固定樣本；目前 ASR INT8 的速度回退，不整合為正式預設。專案 `.venv` 仍是 CPU-only，bitsandbytes 只安裝在 TEMP CUDA 環境。

### 3. 硬體級加速：TensorRT / ONNX 轉換
- [ ] Qwen3-ASR 可評估社群 ONNX 匯出工具，但需另建推論 adapter 並比較準確度與效能；目前官方 pipeline 沒有直接匯出整合。
- [ ] Qwen3-TTS tokenizer 有 ONNX 元件，不等同完整語音生成流程可匯出；先確認端到端支援再投入 TensorRT。
- [ ] 本機為 CPU-only PyTorch，TensorRT/CUDA 效能尚無法量測；不預設固定倍數收益。

---

## 🚀 進行中與已完成優化

- [x] **語句級串流播放 (Sentence Streaming)**：已實作「邊生成邊播放」機制，大幅降低首聲反應時間。
- [x] **ASR 繁體轉寫整合**：已整合 OpenCC，確保辨識結果能正確匹配繁體規則檔案。
- [x] **VAD 靈敏度調整**：已降低門限值並縮短靜音判定時間，提升監聽效能。
- [x] **隨機語音啟動**：新增 `--voice random` 功能。

---

## 📅 未來發展方向
- [ ] **WebSocket 服務化**：將 ASR/TTS 模組拆分為獨立服務，支援遠端裝置連接。
- [ ] **大語言模型整合**：將固定的規則引擎升級為 LLM（如 Qwen-Chat），實現真正的自然語言對話。
- [ ] **UI 介面開發**：建立一個視覺化儀表板，顯示即時波形與辨識狀態。

### 雙引擎部署待決策
- ASR 與 TTS 套件固定不同 Transformers 版本，需使用獨立 Python 子程序/環境並定義本機 RPC。
- RTX 3070 Laptop GPU 為 8 GB；需先量測各模型單獨及同時載入的峰值顯存，再選部署策略。
- 選項：兩模型同時常駐 GPU（延遲低、顯存競用）、GPU 分時載入（省顯存、載入延遲）、ASR CPU + TTS GPU（省 GPU 顯存、ASR 較慢）。
- 官方 ASR `qwen-asr-serve` 入口依賴 vLLM；TTS 官方封裝沒有同型 RPC 服務端，兩者不能直接拼成同一服務。
- 暫不決定 WebSocket 訊息協定、遠端存取方式與 GPU 排程；待硬體量測及服務介面設計確認後執行。
