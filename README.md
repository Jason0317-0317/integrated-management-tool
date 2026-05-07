# 整合管理工具 (Integrated Management Tool)

## 簡介

這是一個整合型的 Streamlit 應用程式，將三個獨立的功能模組整合為一個統一的網頁應用。根據使用者身份的不同，提供「店長用」和「小編用」兩個主要功能入口。

## 功能模組

### 🏪 店長用

#### 1. 預約報表統計 (Lesson Report Automation)
- **功能**: 自動統計課程預約資訊，生成橫向統計表
- **特點**:
  - 支援多館別篩選 (中山館、高美館、義昌館、巨蛋館)
  - 支援日期區間篩選
  - 自動轉換老師名稱為正式姓名
  - 支援 Excel 和 CSV 格式上傳
  - 生成多個版本的統計表 (含合併團1-2人版本)
  - 下載 Excel 報表

#### 2. 業績報表轉換 (Sales Report Transformation)
- **功能**: 自動轉換交易報表為業績報表
- **特點**:
  - 自動計算單價和折數
  - 區分新購和續購
  - 自動計算業績獎金
  - 支援多種合約類型 (一對一、一對二、一對三、一對四)
  - 下載轉換後的 Excel 報表

### ✏️ 小編用

#### 業務獎金計算系統 (Editor Bonus Calculation)
- **功能**: 計算小編的業務獎金
- **特點**:
  - 體驗成交獎金 (依時間分級)
  - 補位獎金
  - 回流獎勵獎金 (STP-T)
  - 結構升級獎金
  - 品牌知名度獎金
  - 月轉換高手獎勵
  - 個人業績獎金
  - 實時計算和預覽
  - 下載結算報表 (Excel)

## 安裝與使用

### 本地運行

1. **克隆或下載專案**
   ```bash
   git clone <repository-url>
   cd integrated-tools
   ```

2. **安裝依賴**
   ```bash
   pip install -r requirements.txt
   ```

3. **運行應用**
   ```bash
   streamlit run app.py
   ```

4. **訪問應用**
   - 打開瀏覽器訪問 `http://localhost:8501`

### Streamlit Cloud 部署

1. **推送到 GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **在 Streamlit Cloud 部署**
   - 訪問 [Streamlit Cloud](https://streamlit.io/cloud)
   - 登入您的 GitHub 帳戶
   - 點擊「New app」
   - 選擇此儲存庫和 `app.py` 檔案
   - 點擊「Deploy」

3. **分享應用連結**
   - Streamlit Cloud 將生成一個公開 URL，您可以與他人分享

## 檔案結構

```
integrated-tools/
├── app.py                 # 主應用程式
├── requirements.txt       # Python 依賴
├── README.md             # 本檔案
└── .gitignore            # Git 忽略檔案 (可選)
```

## 技術棧

- **前端框架**: Streamlit
- **資料處理**: Pandas, NumPy
- **Excel 操作**: OpenPyXL, XlsxWriter
- **Python 版本**: 3.8+

## 依賴套件

| 套件 | 版本 | 用途 |
|------|------|------|
| streamlit | >=1.28.0 | Web 應用框架 |
| pandas | >=2.0.0 | 資料處理和分析 |
| openpyxl | >=3.10.0 | Excel 讀寫 |
| xlsxwriter | >=3.1.0 | Excel 格式化 |
| numpy | >=1.24.0 | 數值計算 |

## 使用說明

### 店長用 - 預約報表統計

1. 在側邊欄選擇「店長用」
2. 切換到「預約報表統計」標籤
3. 設定篩選條件 (館別、日期區間)
4. 上傳原始報表檔案 (Excel 或 CSV)
5. 系統自動處理並顯示統計結果
6. 下載 Excel 報表

### 店長用 - 業績報表轉換

1. 在側邊欄選擇「店長用」
2. 切換到「業績報表轉換」標籤
3. 上傳原始交易報表 (Excel)
4. 系統自動轉換並分類
5. 預覽新購和續購資料
6. 下載轉換後的 Excel 報表

### 小編用 - 業務獎金計算

1. 在側邊欄選擇「小編用」
2. 在側邊欄設定基本資訊 (館別、姓名、日期、身份)
3. 選擇個人業績獎金級別
4. 輸入各項數據 (體驗成交、補位、回流、升級、品牌推廣)
5. 系統實時計算總獎金
6. 點擊「產生並下載結算報表」下載 Excel 檔案

## 常見問題

### Q: 上傳的檔案格式有限制嗎？
A: 預約報表支援 Excel (.xlsx, .xls) 和 CSV 格式。業績報表和小編獎金計算僅支援 Excel 格式。

### Q: 如何修改老師名稱轉換規則？
A: 編輯 `app.py` 中的 `NAME_CONVERSION` 字典，添加或修改對應的名稱轉換規則。

### Q: 可以離線使用嗎？
A: 可以。在本地安裝依賴後，使用 `streamlit run app.py` 即可離線運行。

### Q: 如何自訂獎金計算規則？
A: 編輯 `app.py` 中的 `calculate_bonus()` 函數，修改相應的獎金計算邏輯。

## 貢獻

歡迎提交 Issue 和 Pull Request 來改進此應用。

## 授權

此專案採用 MIT 授權。詳見 LICENSE 檔案。

## 聯絡方式

如有問題或建議，請聯絡開發團隊。

---

**最後更新**: 2026-05-07
