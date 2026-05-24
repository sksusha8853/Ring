# QR Contact App - Quick Start Guide

Get the app running in 5 minutes!

## Prerequisites

- Python 3.8+ installed
- MongoDB running locally (or use MongoDB Atlas)

## Windows Users

1. Open Command Prompt in the Ring folder
2. Run: `setup.bat`
3. Then run: `run.bat`

## macOS/Linux Users

1. Open Terminal in the Ring folder
2. Run: `bash setup.sh`
3. Then run: `bash run.sh`

## Manual Setup (All Platforms)

If you prefer manual setup:

### Step 1: Create Virtual Environment
```bash
python3 -m venv venv

# Activate it
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### Step 2: Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 3: Setup MongoDB

**Option A - Local MongoDB:**
```bash
# macOS
brew services start mongodb-community

# Linux (Ubuntu)
sudo systemctl start mongod

# Windows (in PowerShell as Admin)
net start MongoDB
```

**Option B - MongoDB Atlas (Cloud):**
1. Create account at https://mongodb.com/cloud/atlas
2. Create a cluster
3. Get connection string
4. Update `.env` file with your URL

### Step 4: Configure .env

```bash
# Copy example
cp .env.example .env

# Edit .env (change MONGODB_URL if needed, change SECRET_KEY)
```

### Step 5: Start Services

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
python3 -m http.server 8001
```

## Access the App

1. Open browser: **http://localhost:8001**
2. Sign up for an account
3. You'll see your dashboard with QR code
4. Visit your profile: **http://localhost:8000/u/your_username**

## Testing QR Code

1. From dashboard, generate QR code
2. Download the PNG
3. Scan with phone to see public profile
4. Click "Call Now" or "WhatsApp" buttons

## Troubleshooting

### MongoDB connection error?
```
Error: Failed to connect to MongoDB
```
- Make sure MongoDB is running
- Check MONGODB_URL in .env

### Port already in use?
```
Port 8000 is already in use
```
- Change port: `python main.py --port 8001`

### Import errors?
```
ModuleNotFoundError: No module named...
```
- Make sure virtual environment is activated
- Run: `pip install -r requirements.txt`

## Next Steps

1. **Create an account** and explore the dashboard
2. **Update your profile** with correct phone/WhatsApp
3. **Share your profile link** or QR code
4. **Check analytics** to see profile views

## Important Notes

- Change `SECRET_KEY` in `.env` before deploying!
- QR code URL is: `http://localhost:8000/qr/{username}`
- Profile visits are tracked in MongoDB
- All passwords are hashed with bcrypt

## API Documentation

API docs available at: **http://localhost:8000/docs**

Quick endpoints:
- POST `/signup` - Create account
- POST `/login` - Login
- GET `/me` - Get your profile
- PUT `/me` - Update profile
- GET `/u/{username}` - View public profile
- GET `/qr/{username}` - Download QR code

## Deploy to Production

See [DEPLOYMENT.md](DEPLOYMENT.md) for details on deploying to:
- Render.com
- Railway.app
- Heroku
- Your own server

---

**Need help?** Check README.md for detailed documentation.
