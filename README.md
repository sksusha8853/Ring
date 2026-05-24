# QR Contact App - Setup & Deployment Guide

A full-stack web application for managing personal contact pages with QR codes.

## Features

✅ User Authentication (JWT + Bcrypt)
✅ Personal Contact Management
✅ QR Code Generation & Download
✅ Public Profile Pages (Mobile-Optimized)
✅ Visit Analytics
✅ Responsive Design
✅ Dark Mode Support

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: MongoDB
- **Authentication**: JWT (python-jose)
- **Password Hashing**: Bcrypt
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **QR Generation**: Python qrcode library

## Project Structure

```
Ring/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── config.py              # Configuration & environment variables
│   ├── database.py            # MongoDB connection
│   ├── auth.py                # Authentication & security
│   ├── models.py              # Pydantic models
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── index.html             # Auth & Dashboard page
│   ├── profile.html           # Public profile page
│   ├── style.css              # Global styles
│   ├── script.js              # Main app JavaScript
│   └── profile-script.js      # Public profile JavaScript
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore file
└── README.md                  # This file
```

## Prerequisites

- Python 3.8+
- MongoDB (local or cloud)
- Node.js/npm (for serving frontend, optional)
- Modern web browser

## Installation & Setup

### 1. Clone/Setup Repository

```bash
cd Ring
```

### 2. Setup Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your configuration
nano .env  # or use your preferred editor
```

**Important environment variables:**
- `MONGODB_URL`: Your MongoDB connection string (default: `mongodb://localhost:27017`)
- `DATABASE_NAME`: Database name (default: `qr_contact_app`)
- `SECRET_KEY`: Change this to a random string for production!
- `APP_URL`: Your application URL (e.g., `http://localhost:8000`)

### 5. Setup MongoDB

#### Option A: Local MongoDB

```bash
# macOS (using Homebrew)
brew services start mongodb-community

# Linux (Ubuntu)
sudo systemctl start mongod

# Windows (in PowerShell as Admin)
net start MongoDB
```

#### Option B: MongoDB Atlas (Cloud)

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free account
3. Create a cluster
4. Get your connection string
5. Update `MONGODB_URL` in `.env`:
   ```
   MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
   ```

### 6. Run the Backend

```bash
cd backend
python main.py
```

Or use Uvicorn directly with auto-reload:

```bash
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`

### 7. Serve the Frontend

#### Option A: Using Python's built-in server

```bash
cd frontend
python3 -m http.server 8001
```

Then open: `http://localhost:8001`

#### Option B: Using VS Code Live Server

1. Install Live Server extension in VS Code
2. Right-click on `index.html`
3. Select "Open with Live Server"

#### Option C: Using Node.js http-server

```bash
npm install -g http-server
cd frontend
http-server -p 8001
```

## API Documentation

### Authentication

#### Signup
```
POST /signup
Content-Type: application/json

{
  "username": "john_doe",
  "password": "password123",
  "phone": "+1234567890",
  "whatsapp": "+1234567890",
  "instructions": "Available 9AM-5PM"
}

Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "username": "john_doe",
    "phone": "+1234567890",
    "whatsapp": "+1234567890",
    "instructions": "Available 9AM-5PM",
    "profile_url": "http://localhost:8000/u/john_doe"
  }
}
```

#### Login
```
POST /login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "password123"
}
```

### Protected Routes (Require JWT Token)

#### Get Current User Profile
```
GET /me
Authorization: Bearer {access_token}

Response:
{
  "username": "john_doe",
  "phone": "+1234567890",
  "whatsapp": "+1234567890",
  "instructions": "Available 9AM-5PM",
  "profile_url": "http://localhost:8000/u/john_doe"
}
```

#### Update Profile
```
PUT /me
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "phone": "+0987654321",
  "whatsapp": "+0987654321",
  "instructions": "Call after 6PM"
}
```

#### Generate QR Code
```
GET /qr/{username}
Authorization: Bearer {access_token}

Response: PNG image file
```

#### Get Analytics
```
GET /analytics/visits
Authorization: Bearer {access_token}

Response:
{
  "username": "john_doe",
  "total_visits": 42,
  "visits_last_30_days": 15
}
```

### Public Routes (No Authentication)

#### Get Public Profile
```
GET /u/{username}

Response:
{
  "username": "john_doe",
  "phone": "+1234567890",
  "whatsapp": "+1234567890",
  "instructions": "Available 9AM-5PM",
  "updated_at": "2024-01-15T10:30:00"
}
```

#### Health Check
```
GET /health

Response:
{
  "status": "healthy",
  "app_name": "QR Contact App",
  "version": "1.0.0"
}
```

## MongoDB Schema

### Users Collection
```javascript
{
  "_id": ObjectId,
  "username": "john_doe",           // unique, indexed
  "password_hash": "bcrypt_hash",   // never stored in plain text
  "phone": "+1234567890",
  "whatsapp": "+1234567890",
  "instructions": "Available 9AM-5PM",
  "created_at": ISODate("2024-01-15T10:30:00Z"),
  "updated_at": ISODate("2024-01-15T10:30:00Z")
}
```

### Visits Collection (Analytics)
```javascript
{
  "_id": ObjectId,
  "username": "john_doe",
  "ip_address": "192.168.1.1",
  "user_agent": "Mozilla/5.0...",
  "timestamp": ISODate("2024-01-15T10:30:00Z")
}
```

## Testing the App

### 1. Create an Account
- Go to http://localhost:8001
- Click "Sign Up"
- Fill in your details
- Click "Sign Up"

### 2. Verify Authentication
- You should see your dashboard
- Your profile URL is displayed (e.g., `http://localhost:8000/u/your_username`)

### 3. Generate QR Code
- Click "Generate QR Code" button
- Download the QR code

### 4. Test Public Profile
- Open a new incognito window
- Visit your profile URL: `http://localhost:8001/profile.html?u=your_username`
- Or scan the QR code with a phone camera
- Update the profile-script.js to handle URL parameters if needed

### 5. Test Call/WhatsApp Buttons
- On public profile, click "Call Now" - should open phone dialer
- Click "WhatsApp" - should open WhatsApp web/app

## Deployment Guide

### Option 1: Deploy to Render

#### Backend Deployment
1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. Create new "Web Service"
4. Connect your GitHub repository
5. Set environment variables
6. Build command: `pip install -r requirements.txt`
7. Start command: `uvicorn backend.main:app --host 0.0.0.0`

#### Frontend Deployment
1. Create new "Static Site"
2. Connect GitHub
3. Build command: (leave empty)
4. Publish directory: `frontend`

### Option 2: Deploy to Railway

1. Push code to GitHub
2. Go to [railway.app](https://railway.app)
3. Connect GitHub account
4. Create new project
5. Select repository
6. Add MongoDB plugin
7. Set environment variables
8. Deploy!

### Option 3: Deploy to Vercel (Frontend Only)

1. Frontend to Vercel
2. Backend to separate service (Render, Railway, etc.)

### Important: Update APP_URL

In production, update `APP_URL` in `.env`:
```
APP_URL=https://your-domain.com
```

### Security Checklist

- [ ] Change `SECRET_KEY` to a random 32-character string
- [ ] Use HTTPS in production
- [ ] Set `CORS_ORIGINS` to your frontend domain
- [ ] Enable MongoDB authentication
- [ ] Use environment variables for all secrets
- [ ] Set strong passwords for MongoDB
- [ ] Enable CORS only for your domain

## Troubleshooting

### MongoDB Connection Error
```
Error: Failed to connect to MongoDB
```
- Ensure MongoDB is running: `brew services status mongodb-community`
- Check `MONGODB_URL` in `.env`
- For Atlas, check whitelist IP in MongoDB dashboard

### CORS Error
```
Access to XMLHttpRequest blocked by CORS policy
```
- Update `APP_URL` in `.env` to match your frontend URL
- In production, update CORS settings in `main.py`

### QR Code Not Generating
- Ensure `Pillow` is installed: `pip install Pillow`
- Check file permissions

### Token Expired
- The JWT token expires after 30 minutes
- User will be logged out and redirected to login
- This is configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`

## Performance Tips

1. **MongoDB Indexing**: Already configured for username and timestamps
2. **Caching**: Add Redis for session caching (future enhancement)
3. **CDN**: Serve frontend assets via CDN
4. **Database**: Use MongoDB Atlas for better performance
5. **Backend**: Use Gunicorn in production instead of Uvicorn

```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.main:app
```

## Future Enhancements

- [ ] Two-factor authentication
- [ ] Profile customization (colors, themes)
- [ ] Email verification
- [ ] Password reset functionality
- [ ] API rate limiting
- [ ] Image uploads for profiles
- [ ] Integration with analytics dashboards
- [ ] Mobile app (React Native)
- [ ] Email notifications
- [ ] Social media integration

## Support & Issues

For bugs and feature requests, create an issue on GitHub.

## License

MIT License - Feel free to use this project commercially or personally.

---

Built with ❤️ using FastAPI, MongoDB, and Vanilla JavaScript
