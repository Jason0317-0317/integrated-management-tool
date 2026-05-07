# 部署指南

## 本地開發環境

### 前置要求

- Python 3.8+
- pip 或 conda
- 現代網頁瀏覽器

### 快速開始

1. **克隆專案**
```bash
git clone https://github.com/Jason0317-0317/integrated-management-tool.git
cd integrated-management-tool
```

2. **建立虛擬環境 (推薦)**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **安裝依賴**
```bash
pip install -r requirements.txt
```

4. **啟動後端**
```bash
python backend.py
```
後端會在 `http://localhost:5000` 啟動

5. **在另一個終端啟動前端**
```bash
# 使用 Python HTTP 伺服器
python -m http.server 8000

# 或使用 Node.js http-server (如果已安裝)
npx http-server
```

6. **訪問應用**
打開瀏覽器訪問 `http://localhost:8000`

## 生產環境部署

### 使用 Gunicorn (推薦用於 Linux/macOS)

1. **安裝 Gunicorn**
```bash
pip install gunicorn
```

2. **啟動應用**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 backend:app
```

### 使用 Waitress (推薦用於 Windows)

1. **安裝 Waitress**
```bash
pip install waitress
```

2. **啟動應用**
```bash
waitress-serve --port=5000 backend:app
```

### Docker 部署

1. **建立 Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安裝依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用檔案
COPY . .

# 暴露埠
EXPOSE 5000

# 啟動應用
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "backend:app"]
```

2. **建立 .dockerignore**
```
__pycache__
*.pyc
.git
.gitignore
venv/
.env
```

3. **構建和運行**
```bash
# 構建映像
docker build -t integrated-tools:latest .

# 運行容器
docker run -p 5000:5000 integrated-tools:latest
```

### Heroku 部署

1. **建立 Procfile**
```
web: gunicorn -w 4 -b 0.0.0.0:$PORT backend:app
```

2. **建立 runtime.txt**
```
python-3.11.0
```

3. **部署**
```bash
# 安裝 Heroku CLI
# 訪問 https://devcenter.heroku.com/articles/heroku-cli

# 登入 Heroku
heroku login

# 建立應用
heroku create your-app-name

# 部署
git push heroku main
```

4. **更新前端 API_BASE**
在 `app.js` 中修改：
```javascript
const API_BASE = 'https://your-app-name.herokuapp.com/api';
```

### Railway 部署

1. **連接 GitHub**
- 訪問 [Railway.app](https://railway.app)
- 使用 GitHub 帳戶登入
- 連接您的儲存庫

2. **配置環境變數**
- 在 Railway 儀表板中設定 `FLASK_ENV=production`

3. **自動部署**
- Railway 會自動檢測 `requirements.txt` 並部署

4. **獲取 URL**
- Railway 會為您的應用生成一個 URL
- 更新前端 `app.js` 中的 `API_BASE`

### Render 部署

1. **連接 GitHub**
- 訪問 [Render.com](https://render.com)
- 使用 GitHub 帳戶登入
- 連接您的儲存庫

2. **建立 Web Service**
- 選擇 Python 環境
- 設定啟動命令：`gunicorn -w 4 -b 0.0.0.0:$PORT backend:app`

3. **部署**
- Render 會自動部署並提供 URL

## 前端靜態檔案部署

### 使用 Netlify

1. **連接 GitHub**
- 訪問 [Netlify](https://netlify.com)
- 使用 GitHub 帳戶登入
- 選擇儲存庫

2. **設定**
- Build command: (留空)
- Publish directory: `.` (或專案根目錄)

3. **環境變數**
在 Netlify 儀表板中設定 `API_BASE` 為您的後端 URL

### 使用 Vercel

1. **連接 GitHub**
- 訪問 [Vercel](https://vercel.com)
- 使用 GitHub 帳戶登入

2. **部署**
- Vercel 會自動檢測並部署靜態檔案

3. **環境變數**
在 Vercel 儀表板中設定 `API_BASE`

## 環境變數配置

建立 `.env` 檔案：

```env
# Flask 設定
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here

# API 設定
API_HOST=0.0.0.0
API_PORT=5000
API_WORKERS=4

# 檔案上傳
MAX_UPLOAD_SIZE=104857600  # 100MB

# CORS 設定
CORS_ORIGINS=*
```

在 `backend.py` 中載入環境變數：

```python
from dotenv import load_dotenv
import os

load_dotenv()

app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_UPLOAD_SIZE', 16777216))
```

## 安全性建議

### 生產環境檢查清單

- [ ] 設定 `FLASK_ENV=production`
- [ ] 設定強大的 `SECRET_KEY`
- [ ] 啟用 HTTPS
- [ ] 限制 CORS 來源
- [ ] 設定檔案上傳大小限制
- [ ] 添加速率限制
- [ ] 定期更新依賴套件
- [ ] 監控應用日誌
- [ ] 設定備份策略

### CORS 配置

在 `backend.py` 中自訂 CORS：

```python
from flask_cors import CORS

# 限制 CORS 來源
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.com"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})
```

### 速率限制

安裝 Flask-Limiter：

```bash
pip install Flask-Limiter
```

在 `backend.py` 中使用：

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/process-lesson-report', methods=['POST'])
@limiter.limit("10 per hour")
def process_lesson_report():
    # ...
```

## 監控和日誌

### 啟用日誌

在 `backend.py` 中配置日誌：

```python
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

@app.route('/api/health', methods=['GET'])
def health_check():
    logger.info('Health check requested')
    return jsonify({'status': 'ok'})
```

### 使用 Sentry 進行錯誤追蹤

1. **安裝 Sentry SDK**
```bash
pip install sentry-sdk
```

2. **集成到應用**
```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)
```

## 故障排除

### 常見問題

**Q: 前端無法連接後端**
- 檢查後端是否正在運行
- 確認 `app.js` 中的 `API_BASE` 正確
- 檢查防火牆設定
- 查看瀏覽器控制台的 CORS 錯誤

**Q: 檔案上傳失敗**
- 檢查檔案大小是否超過限制
- 確認檔案格式正確
- 查看後端日誌以了解詳細錯誤

**Q: 應用運行緩慢**
- 增加 Gunicorn workers 數量
- 檢查資料庫查詢效能
- 啟用快取
- 優化前端資源

## 備份和恢復

### 定期備份

```bash
# 備份整個專案
tar -czf backup-$(date +%Y%m%d).tar.gz .

# 上傳到雲端儲存 (例如 AWS S3)
aws s3 cp backup-*.tar.gz s3://your-bucket/backups/
```

### 恢復

```bash
# 從備份恢復
tar -xzf backup-20260507.tar.gz
```

## 效能優化

### 前端優化

- 啟用 gzip 壓縮
- 使用 CDN 分發靜態檔案
- 最小化 CSS 和 JavaScript
- 優化圖片

### 後端優化

- 使用資料庫索引
- 實現快取層 (Redis)
- 非同步處理長時間操作
- 使用連接池

## 更新和維護

### 定期更新依賴

```bash
# 檢查過時的套件
pip list --outdated

# 更新所有套件
pip install --upgrade -r requirements.txt

# 更新 requirements.txt
pip freeze > requirements.txt
```

### 版本控制

使用 Git 標籤標記版本：

```bash
git tag -a v2.0.0 -m "Release version 2.0.0"
git push origin v2.0.0
```

---

如有問題，請參考 README.md 或提交 Issue。
