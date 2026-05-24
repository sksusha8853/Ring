# QR Contact App - Project Overview

A complete, production-ready QR Contact Management application built with FastAPI and MongoDB.

## What This Does

- Users create accounts with their contact information
- Each user gets a unique profile page accessible via QR code
- Public profile page displays instructions, call button, and WhatsApp button
- User dashboard allows profile updates and QR code download
- Analytics track profile visits
- Secure JWT authentication with bcrypt password hashing

## File Structure

```
Ring/
├── backend/                    # FastAPI backend server
│   ├── main.py                # Main FastAPI application
│   │   ├── Authentication routes (/signup, /login)
│   │   ├── Profile routes (/me, PUT /me)
│   │   ├── Public routes (/u/{username})
│   │   ├── QR Code routes (/qr/{username})
│   │   └── Analytics routes (/analytics/visits)
│   ├── config.py              # Configuration & environment variables
│   ├── database.py            # MongoDB connection & operations
│   ├── auth.py                # JWT & password hashing utilities
│   ├── models.py              # Pydantic data models
│   └── requirements.txt        # Python dependencies
│
├── frontend/                   # Web interface (HTML/CSS/JS)
│   ├── index.html             # Main app (login/dashboard)
│   │   ├── Login form
│   │   ├── Signup form
│   │   ├── User dashboard
│   │   ├── Profile management
│   │   ├── QR code display
│   │   └── Analytics section
│   ├── profile.html           # Public profile page (not used - served from backend)
│   ├── style.css              # Global styles
│   │   ├── Theme colors & variables
│   │   ├── Component styles
│   │   ├── Responsive design
│   │   ├── Dark mode support
│   │   └── Mobile optimizations
│   ├── script.js              # Main app logic
│   │   ├── Auth handlers (login/signup)
│   │   ├── Profile management
│   │   ├── QR code generation
│   │   └── Analytics loading
│   └── profile-script.js      # Public profile script (for API usage)
│
├── Configuration Files
│   ├── .env.example           # Environment variables template
│   ├── .gitignore             # Git ignore rules
│   ├── setup.sh               # Auto setup script (macOS/Linux)
│   ├── setup.bat              # Auto setup script (Windows)
│   ├── run.sh                 # Run all services (macOS/Linux)
│   └── run.bat                # Run all services (Windows)
│
├── Documentation
│   ├── README.md              # Full documentation
│   ├── QUICK_START.md         # 5-minute setup guide
│   ├── DEPLOYMENT.md          # Deployment instructions
│   └── PROJECT_OVERVIEW.md    # This file
```

## Key Features

### 1. Authentication (Backend)
- **Signup**: Create account with unique username
- **Login**: JWT-based authentication
- **Password Security**: Bcrypt hashing (never stored in plain text)
- **Token Management**: 30-minute expiration (configurable)

**Related Files:**
- `backend/auth.py` - JWT and password functions
- `backend/models.py` - User data models

### 2. User Dashboard (Frontend)
- View current profile information
- Update phone, WhatsApp, instructions
- Generate and download QR code
- View profile URL for sharing
- See profile analytics

**Related Files:**
- `frontend/index.html` - Dashboard markup
- `frontend/script.js` - Dashboard logic
- `frontend/style.css` - Dashboard styling

### 3. Public Profile (Backend)
- Accessible without login: `/u/{username}`
- Returns HTML for browser requests
- Shows instructions, call button, WhatsApp button
- Tracks visit analytics automatically
- Mobile-optimized design

**Related Files:**
- `backend/main.py` - Profile serving logic
- Analytics tracking in public profile endpoint

### 4. QR Code Generation (Backend)
- Generate QR code pointing to profile URL
- Return PNG image file
- Download functionality from dashboard

**Related Files:**
- `backend/main.py` - QR generation endpoint
- `frontend/script.js` - QR download trigger

### 5. Analytics (Backend)
- Track profile visits (IP, user agent)
- Count total visits
- 30-day visit statistics

**Related Files:**
- `backend/main.py` - Analytics endpoints
- MongoDB `visits` collection

### 6. Database Schema (MongoDB)

#### Users Collection
```javascript
{
  "_id": ObjectId,
  "username": "john_doe",           // unique index
  "password_hash": "$2b$12...",      // bcrypt hash
  "phone": "+1234567890",
  "whatsapp": "+1234567890",
  "instructions": "Available 9AM-5PM",
  "created_at": ISODate("2024-01-15T10:30:00Z"),
  "updated_at": ISODate("2024-01-15T10:30:00Z")
}
```

#### Visits Collection
```javascript
{
  "_id": ObjectId,
  "username": "john_doe",            // index
  "ip_address": "192.168.1.1",
  "user_agent": "Mozilla/5.0...",
  "timestamp": ISODate("2024-01-15T10:35:00Z")  // index
}
```

## Technology Stack

### Backend
- **Framework**: FastAPI (Python web framework)
- **Server**: Uvicorn (ASGI server)
- **Database**: MongoDB (NoSQL database)
- **Auth**: python-jose (JWT), passlib (password hashing)
- **Hashing**: bcrypt (secure password hashing)
- **QR Code**: qrcode library with Pillow
- **Validation**: Pydantic (data validation)

### Frontend
- **Markup**: HTML5
- **Styling**: CSS3 (responsive, mobile-first)
- **Logic**: Vanilla JavaScript (no frameworks)
- **Storage**: localStorage (for JWT tokens)
- **HTTP**: Fetch API (for API calls)

### DevOps
- **Package Manager**: pip (Python)
- **Virtual Environment**: venv
- **Scripts**: Bash/Batch

## API Endpoints

### Public Endpoints
- `GET /health` - Health check
- `GET /u/{username}` - Public profile (HTML for browser)
- `GET /api/u/{username}` - Public profile (JSON)

### Authentication
- `POST /signup` - Create new user
- `POST /login` - Login and get JWT

### Protected Endpoints (Require JWT)
- `GET /me` - Get current user profile
- `PUT /me` - Update profile
- `GET /qr/{username}` - Download QR code
- `GET /analytics/visits` - Get visit statistics

## Security Features

✅ **Password Security**
- Bcrypt hashing with 12 salt rounds
- Never stored in plain text
- Validated on login

✅ **Authentication**
- JWT tokens with expiration
- HTTPBearer security scheme
- Token-based authorization

✅ **Data Validation**
- Pydantic models for all requests
- Username format validation
- Phone number validation
- Input sanitization for HTML output

✅ **Database**
- Unique username index
- MongoDB connection pooling
- Secure connection string in .env

✅ **XSS Prevention**
- HTML escaping in public profile
- Proper Content-Type headers

## Running the Application

### Quick Start
```bash
# macOS/Linux
bash setup.sh
bash run.sh

# Windows
setup.bat
run.bat
```

### Manual Start
```bash
# Terminal 1: Backend
cd backend
python main.py

# Terminal 2: Frontend
cd frontend
python3 -m http.server 8001
```

## Development Workflow

1. **Make Changes**
   - Edit backend: `backend/main.py` (auto-reloads)
   - Edit frontend: `frontend/` (browser refresh)

2. **Test Locally**
   - Signup: http://localhost:8001
   - Login: http://localhost:8001
   - API Docs: http://localhost:8000/docs

3. **Deploy**
   - Push to GitHub
   - Follow [DEPLOYMENT.md](DEPLOYMENT.md)

## Common Modifications

### Change Token Expiration
Edit `backend/config.py`:
```python
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Changed from 30
```

### Change Database Name
Edit `backend/config.py`:
```python
DATABASE_NAME = "my_custom_db"
```

### Add New Fields to Profile
1. Update MongoDB schema
2. Add to `backend/models.py`
3. Update `backend/main.py` routes
4. Update `frontend/index.html` form
5. Update `frontend/script.js`

### Change UI Colors
Edit `frontend/style.css`:
```css
:root {
    --primary-color: #your-color;
    /* ... */
}
```

## Troubleshooting Guide

### Issue: Port Already in Use
```bash
# Change port in backend/main.py
uvicorn main:app --reload --port 8001
```

### Issue: MongoDB Connection Failed
```bash
# Check MongoDB is running
brew services list  # macOS
mongo --version     # Check installation
```

### Issue: JWT Token Error
```bash
# Clear localStorage
# In browser console:
localStorage.clear()
# Then refresh page
```

### Issue: CORS Error
```bash
# Update .env
APP_URL=http://localhost:8001  # Frontend URL
```

## Performance Tips

- Use MongoDB Atlas for better uptime
- Enable MongoDB indexing (already done)
- Cache profile data with Redis (future)
- Compress images for QR codes
- Use CDN for static files

## Future Enhancements

- [ ] Social media integration
- [ ] Profile picture upload
- [ ] Theme customization
- [ ] Email notifications
- [ ] Two-factor authentication
- [ ] Advanced analytics dashboard
- [ ] API rate limiting
- [ ] Data export functionality

## Learning Resources

- **FastAPI**: https://fastapi.tiangolo.com/
- **MongoDB**: https://docs.mongodb.com/
- **JWT**: https://jwt.io/
- **Bcrypt**: https://github.com/pyca/bcrypt
- **Pydantic**: https://docs.pydantic.dev/

## Support

For issues or questions:
1. Check README.md for detailed docs
2. Review API docs at http://localhost:8000/docs
3. Check browser console for JavaScript errors
4. Check backend logs in terminal
5. Check MongoDB connection string

---

**Created with ❤️ using FastAPI, MongoDB, and Vanilla JavaScript**

*This is production-ready code. Deploy with confidence!*
