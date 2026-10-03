# 🚀 語音助理效能優化藍圖 (Performance Optimization Roadmap)

> [!NOTE]
> 本文件記錄了關於提升語音助理反應速度的深度分析與後續優化任務。目前的效能瓶頸主要在於 **GPU 模型推理**，而非程式語言本身。

---

## 🧠 為什麼不優先更換程式語言 (Python vs. Rust/Go)？

在目前的架構中，Python 僅作為「指揮官」角色，實際的運算（ASR 與 TTS）是由底層的 **C++/CUDA** 核心在 GPU 上執行。
*   **瓶頸點**：95% 的時間花在 GPU 的矩陣運算，而非 Python 的邏輯執行。
*   **更換語言的代價**：換成 Rust/Go 會失去 Python 豐富的 AI 生態系支援，且對 GPU 推理速度的提升微乎其微（僅能節省幾毫秒的指令傳遞時間）。

---

## 🛠️ 核心優化任務清單

### 1. 演算法級加速：Flash Attention
- [x] 提供 `--attention-backend`，可選擇 SDPA 或 Flash Attention 2，並傳入 Qwen ASR/TTS loader；預設使用 SDPA。
- [ ] 安裝相容的 `flash-attn` 並在 CUDA GPU 上量測速度、顯存與輸出品質；目前 CPU-only 環境未驗證。

### 2. 模型尺寸優化：模型量化 (Quantization)
- [ ] 評估 Qwen ASR/TTS loader 支援的 INT8/INT4 量化方式，量測顯存、速度與輸出品質後再決定整合方案。

### 3. 硬體級加速：TensorRT / ONNX 轉換
- [ ] 評估目前 Qwen ASR/TTS pipeline 是否支援 TensorRT/ONNX 匯出，並以實測確認收益及品質影響。

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
