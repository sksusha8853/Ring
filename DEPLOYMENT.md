# QR Contact App - Deployment Guide

## Deploy to Render.com (Recommended)

### Backend on Render

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Create Backend Service**
   - Go to [render.com](https://render.com)
   - Click "New +"
   - Select "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: qr-contact-backend
     - **Branch**: main
     - **Root Directory**: backend
     - **Runtime**: Python 3.11
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app`
   - Add Environment Variables:
     - `MONGODB_URL`: Your MongoDB connection string
     - `SECRET_KEY`: Random 32-character string
     - `APP_URL`: Your Render backend URL (e.g., https://qr-contact-backend.onrender.com)

3. **Add gunicorn to requirements.txt**
   ```bash
   echo "gunicorn==21.2.0" >> backend/requirements.txt
   ```

### Frontend on Render

1. **Create Frontend Service**
   - Click "New +"
   - Select "Static Site"
   - Connect repository
   - Configure:
     - **Name**: qr-contact-frontend
     - **Root Directory**: frontend
     - **Build Command**: (leave empty)
     - **Publish Directory**: frontend

2. **Update API URL**
   - In `frontend/script.js`, change:
     ```javascript
     const API_URL = 'https://qr-contact-backend.onrender.com';
     ```
   - Commit and push

## Deploy to Railway.app

### Setup

1. **Install Railway CLI**
   ```bash
   npm install -g railway
   ```

2. **Login**
   ```bash
   railway login
   ```

3. **Create Project**
   ```bash
   railway init
   ```

### Backend

1. **Create Procfile** in root:
   ```
   web: cd backend && gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT
   ```

2. **Add MongoDB Plugin**
   - In Railway dashboard, add MongoDB plugin
   - It will automatically set `MONGODB_URL`

3. **Add Environment Variables**
   - `SECRET_KEY`: Random string
   - `APP_URL`: Your Railway URL

4. **Deploy**
   ```bash
   railway up
   ```

### Frontend

1. **Deploy Separately**
   - Use Vercel (free, fast)
   - Or Netlify (free, easy)
   - Or keep on Railway

## Deploy to Vercel (Frontend Only)

1. **Push to GitHub**

2. **Create vercel.json** in frontend folder:
   ```json
   {
     "buildCommand": "echo 'Build complete'",
     "outputDirectory": ".",
     "routes": [
       {
         "src": "/(.*)",
         "dest": "index.html"
       }
     ]
   }
   ```

3. **Deploy**
   - Go to [vercel.com](https://vercel.com)
   - Import project
   - Build runs automatically
   - Add environment variables if needed

4. **Update API URL**
   - Add `NEXT_PUBLIC_API_URL` environment variable
   - Update `script.js` to use it

## Docker Deployment

### Create Dockerfile (Backend)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]
```

### Create docker-compose.yml

```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:7.0
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      MONGODB_URL: mongodb://admin:password@mongodb:27017/qr_contact_app?authSource=admin
      SECRET_KEY: your-secret-key-change-this
      APP_URL: http://localhost:8000
    depends_on:
      - mongodb

  frontend:
    image: nginx:alpine
    ports:
      - "8001:80"
    volumes:
      - ./frontend:/usr/share/nginx/html
    depends_on:
      - backend

volumes:
  mongo_data:
```

### Run with Docker

```bash
docker-compose up
```

## Self-Hosted (VPS/Dedicated Server)

### Setup on Ubuntu

1. **Install Dependencies**
   ```bash
   sudo apt-get update
   sudo apt-get install -y python3 python3-venv python3-pip nginx mongodb
   ```

2. **Clone Repository**
   ```bash
   git clone <your-repo> /var/www/qr-contact
   cd /var/www/qr-contact
   ```

3. **Setup Python**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   cd backend
   pip install -r requirements.txt
   cd ..
   ```

4. **Configure Nginx**
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       location /api {
           proxy_pass http://127.0.0.1:8000;
       }

       location / {
           root /var/www/qr-contact/frontend;
           try_files $uri $uri/ /index.html;
       }
   }
   ```

5. **Start Backend with Systemd**
   ```bash
   sudo nano /etc/systemd/system/qr-contact.service
   ```

   ```ini
   [Unit]
   Description=QR Contact App Backend
   After=network.target

   [Service]
   Type=notify
   User=www-data
   WorkingDirectory=/var/www/qr-contact
   ExecStart=/var/www/qr-contact/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.main:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start qr-contact
   sudo systemctl enable qr-contact
   ```

6. **Enable HTTPS with Let's Encrypt**
   ```bash
   sudo apt-get install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com
   ```

## Security Checklist

- [ ] Change `SECRET_KEY` to random string
- [ ] Enable HTTPS
- [ ] Set MongoDB authentication
- [ ] Whitelist MongoDB IP (if using Atlas)
- [ ] Set environment variables securely
- [ ] Disable CORS for production
- [ ] Enable rate limiting
- [ ] Setup backup strategy for MongoDB
- [ ] Monitor application logs
- [ ] Setup uptime monitoring

## Environment Variables for Production

```env
# Change all of these!
MONGODB_URL=mongodb+srv://user:password@cluster.mongodb.net/qr_contact_app
SECRET_KEY=generate-random-32-char-string
APP_URL=https://yourdomain.com

# Keep the same
DATABASE_NAME=qr_contact_app
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Monitoring

### Application Logs
- Render: Built-in logs in dashboard
- Railway: Built-in logs
- Self-hosted: `journalctl -u qr-contact -f`

### Database Monitoring
- MongoDB Atlas: Built-in dashboard
- Local: Use MongoDB Compass

### Uptime Monitoring
- Use services like UptimeRobot
- Monitor status page

## Scaling

### Add Caching
```python
from redis import Redis
cache = Redis(host='localhost', port=6379)
```

### Add Load Balancing
- Use Nginx as reverse proxy
- Deploy multiple backend instances

### CDN for Frontend
- Use Cloudflare or similar
- Cache static files

---

**Choose your platform and follow the steps above!**
