# 春不老薪資計算系統

整合管理工具 - 結合預約報表統計、業績報表轉換和業務獎金計算的完整解決方案。

## 技術棧

- **前端**: HTML5 + CSS3 + Vanilla JavaScript
- **後端**: Python Flask + CORS
- **資料處理**: Pandas, NumPy, OpenPyXL
- **部署**: 可部署到任何支援 Python 的伺服器

## 專案結構

```
integrated-management-tool/
├── index.html          # 前端主頁面
├── styles.css          # 前端樣式
├── app.js              # 前端邏輯
├── backend.py          # Python Flask 後端
├── requirements.txt    # Python 依賴
└── README.md          # 本文件
```

## 安裝與運行

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 啟動後端服務

```bash
python backend.py
```

後端會在 `http://localhost:5000` 啟動

### 3. 啟動前端

在瀏覽器中打開 `index.html` 或使用簡單的 HTTP 伺服器：

```bash
# 使用 Python 內建伺服器
python -m http.server 8000

# 或使用 Node.js http-server
npx http-server
```

然後訪問 `http://localhost:8000`

## 功能說明

### 店長用

#### 1. 預約報表統計
- 支援多館別篩選 (全部、中山館、高美館、義昌館、巨蛋館)
- 靈活的日期區間選擇
- 自動名稱轉換 (20+ 位老師的簡稱轉換)
- 支援 Excel 和 CSV 格式
- 自動課程分類統計
- 生成橫向統計表和原始明細對照表
- 支援下載 Excel 報表

#### 2. 業績報表轉換
- 自動計算單價、折數、未稅金額
- 智能分類新購和續購
- 自動計算業績獎金 (2%、1.5%、1%)
- 支援多種合約類型
- 生成分類統計表
- 支援下載轉換後的 Excel 報表

### 小編用

#### 業務獎金計算系統

完整的獎金計算工具，包含以下獎金類型：

| 獎金類型 | 說明 | 計算方式 |
|---------|------|--------|
| 個人業績獎金 | 根據業績級別發放 | 12萬元 (2000元)、24萬元 (4000元)、30萬元 (6000元) |
| 體驗成交獎金 | 根據成交時間分級 | 當天 (80元)、48小時 (60元)、7天內 (50元) |
| 補位獎金 | 補開課程獎勵 | 每次 30 元 |
| 回流獎勵獎金 | 會員回流獎勵 | 10堂 (100元)、20堂 (200元)、30堂 (300元)、40堂 (500元) |
| 結構升級獎金 | 課程升級獎勵 | 1對2變1對3 (100元)、團課變期班 (150元)、包班成立 (300元) |
| 品牌知名度獎金 | 推廣獎勵 | 正職基準 5 人、兼職基準 2 人；超過基準每 5 人加 200 元 |
| 月高手獎勵 | 轉換筆數獎勵 | 30筆 (2000元)、50筆 (5000元) |

## API 端點

### 健康檢查
- `GET /api/health` - 檢查後端服務狀態

### 預約報表處理
- `POST /api/process-lesson-report` - 處理預約報表
  - 參數: `file`, `branch`, `start_date`, `end_date`
  - 返回: 統計結果 JSON

### 業績報表處理
- `POST /api/process-sales-report` - 處理業績報表
  - 參數: `file`
  - 返回: 新購和續購資料 JSON

### 獎金報表下載
- `POST /api/download-bonus-report` - 下載獎金結算報表
  - 參數: JSON 格式的獎金資料
  - 返回: Excel 檔案

## 部署指南

### 本地部署

1. 克隆或下載專案
2. 安裝依賴: `pip install -r requirements.txt`
3. 啟動後端: `python backend.py`
4. 啟動前端: 使用 HTTP 伺服器或直接打開 HTML 檔案

### 伺服器部署 (Heroku/Railway/Render)

1. 建立 `Procfile`:
```
web: python backend.py
```

2. 部署到您選擇的平台

3. 更新前端中的 `API_BASE` 為您的伺服器 URL

### Docker 部署

建立 `Dockerfile`:
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "backend.py"]
```

構建和運行:
```bash
docker build -t integrated-tools .
docker run -p 5000:5000 integrated-tools
```

## 開發注意事項

### CORS 設定

前端和後端運行在不同的埠上時，需要啟用 CORS。已在 `backend.py` 中配置：

```python
from flask_cors import CORS
CORS(app)
```

### 檔案上傳限制

預設檔案上傳大小限制為 16MB。如需修改，在 `backend.py` 中添加：

```python
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
```

### 環境變數

可以使用 `.env` 檔案設定環境變數：

```
FLASK_ENV=production
FLASK_DEBUG=False
API_PORT=5000
```

## 故障排除

### 前端無法連接後端

1. 確保後端已啟動: `python backend.py`
2. 檢查 `app.js` 中的 `API_BASE` 是否正確
3. 檢查瀏覽器控制台是否有 CORS 錯誤

### 檔案上傳失敗

1. 確認檔案格式正確 (Excel 或 CSV)
2. 檢查檔案是否包含必要的欄位
3. 查看後端日誌以了解詳細錯誤

### 獎金計算不正確

1. 確認輸入的數據是否正確
2. 檢查員工身份設定 (正職/兼職)
3. 驗證各項獎金的計算邏輯

## 貢獻指南

歡迎提交 Issue 和 Pull Request！

## 授權

MIT License

## 聯絡方式

如有問題或建議，請提交 Issue 或聯絡開發團隊。

---

**版本**: 2.0.0  
**最後更新**: 2026-05-07  
**技術**: HTML + CSS + JavaScript + Python Flask
