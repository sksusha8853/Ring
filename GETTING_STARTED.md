# QR Contact App - Getting Started in 60 Seconds

## What is This?

A complete web app that lets users create personalized contact pages accessible via QR codes. When someone scans the QR code, they see your contact info with one-tap buttons to call or message you on WhatsApp.

## The Elevator Pitch

```
User creates account → Gets unique profile page → Generates QR code → 
Others scan code → See contact info → Can call or message directly
```

## Files You Need to Know

### Backend (Python/FastAPI)
```
backend/main.py      ← The app's brain
backend/auth.py      ← Security & login logic
backend/database.py  ← Connects to MongoDB
backend/config.py    ← Settings
```

### Frontend (HTML/CSS/JavaScript)
```
frontend/index.html  ← Main page (login/dashboard)
frontend/script.js   ← Dashboard logic
frontend/style.css   ← Design
```

### Setup Files
```
setup.sh / setup.bat ← Run this first!
run.sh / run.bat     ← Run this to start
validate.sh / .bat   ← Check if setup worked
```

## Installation (Pick Your OS)

### macOS/Linux
```bash
cd Ring
bash setup.sh
bash run.sh
# Open http://localhost:8001
```

### Windows
```bash
cd Ring
setup.bat
run.bat
REM Open http://localhost:8001
```

## What Happens When You Run It?

1. **Backend starts** at http://localhost:8000
   - Handles login, profile, QR codes
   - API docs at http://localhost:8000/docs

2. **Frontend starts** at http://localhost:8001
   - The beautiful web interface
   - Communicates with backend

3. **MongoDB** needs to be running
   - Local: `brew services start mongodb-community`
   - Cloud: Use MongoDB Atlas

## Try It Out (2 minutes)

### Step 1: Sign Up
- Go to http://localhost:8001
- Enter username, password, phone number
- Click "Sign Up"

### Step 2: Generate QR
- Click "Generate QR Code"
- Download the PNG file

### Step 3: Test Profile
- Open new private browser window
- Visit: http://localhost:8000/u/your_username
- You'll see the public profile!
- Try the "Call Now" and "WhatsApp" buttons

### Step 4: Share with Someone
- Show them the QR code
- They scan it
- They see your contact info
- They can call or message directly

## Project Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        QR Contact App                        │
└─────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                │                           │
         ┌──────▼──────┐            ┌──────▼──────┐
         │   Frontend  │            │   Backend   │
         │ (HTML/CSS)  │            │  (FastAPI)  │
         ├─────────────┤            ├─────────────┤
         │ index.html  │            │  main.py    │
         │ script.js   │─◄─────────►│  auth.py    │
         │ style.css   │            │  database.py│
         └─────────────┘            └──────┬──────┘
                                           │
                                    ┌──────▼──────┐
                                    │  MongoDB    │
                                    │  Database   │
                                    └─────────────┘
```

## How It Works

### User Journey
```
User → Sign Up (create account)
     → See Dashboard (manage profile)
     → Generate QR Code (download image)
     → Share QR Code (with others)

Others → Scan QR Code
      → See Profile Page
      → Click Call → Opens phone dialer
      → Click WhatsApp → Opens WhatsApp
```

### Behind the Scenes
```
Browser               Server              Database
─────────────────────────────────────────────────
Sign Up Form ──POST──► /signup ──────► Stores user
                          │
                    [Hash password]
                          │
                      Saves in DB
                          │
Login Form ──POST──► /login ◄──────── Gets user
                          │
                    [Verify password]
                          │
                   Returns JWT token
                          │
Public Profile ──GET──► /u/{user} ──► Gets profile
                          │
                    [Tracks visit]
                          │
                    Returns HTML
                          │
                    Shows to visitor
```

## Key Concepts

### JWT Authentication
- You log in once
- Get a token (like a ticket)
- Use it to access your dashboard
- Expires after 30 minutes

### Password Security
- Password is hashed (scrambled)
- We never store plain text
- Uses bcrypt (military-grade)

### QR Code
- Links to your public profile
- Others can scan with phone
- No app needed!

### Public Profile
- Anyone can visit (no login needed)
- Shows your contact info
- Tracks how many visits you get

## Configuration

### .env File (Environment Variables)
```
MONGODB_URL=mongodb://localhost:27017
SECRET_KEY=your-secret-key-here
APP_URL=http://localhost:8000
DATABASE_NAME=qr_contact_app
```

Get it from `.env.example` and customize.

## Common Questions

### Q: Do I need to deploy this?
**A:** No! It works perfectly on your local machine. But you CAN deploy for free to Render.com or Railway.app (see DEPLOYMENT.md).

### Q: Can I change the colors?
**A:** Yes! Edit `frontend/style.css` and change the color values under `:root`.

### Q: How do I add more fields?
**A:** Update MongoDB schema + backend models + frontend forms + JavaScript. See PROJECT_OVERVIEW.md for details.

### Q: Is it secure?
**A:** Yes! Uses JWT, bcrypt, validated inputs, and XSS protection. See FEATURES.md.

### Q: Can multiple people use it?
**A:** Yes! Each person signs up and gets their own profile URL.

## File Purposes

| File | Purpose |
|------|---------|
| main.py | All API routes & logic |
| auth.py | Login security |
| database.py | MongoDB connection |
| config.py | Settings |
| models.py | Data structures |
| index.html | Main interface |
| script.js | Dashboard code |
| style.css | Design & layout |

## Troubleshooting

### "Port 8000/8001 already in use"
```bash
# Use different port
python backend/main.py --port 9000
```

### "Cannot connect to MongoDB"
```bash
# Start MongoDB
brew services start mongodb-community  # macOS
sudo systemctl start mongod            # Linux
net start MongoDB                      # Windows
```

### "Import error: ModuleNotFoundError"
```bash
# Install dependencies
source venv/bin/activate
pip install -r backend/requirements.txt
```

### "Login not working"
```bash
# Clear browser storage and try again
# Open Developer Tools → Application → Clear Storage
```

## Next Steps

1. **Run it locally** (setup.sh + run.sh)
2. **Play with it** (create account, generate QR)
3. **Read documentation** (see docs folder)
4. **Customize it** (change colors, add fields)
5. **Deploy it** (see DEPLOYMENT.md for free options)

## Documentation Files

- **QUICK_START.md** - 5-minute setup
- **README.md** - Full documentation
- **DEPLOYMENT.md** - Deploy to internet
- **API_TESTING.md** - Test the API
- **PROJECT_OVERVIEW.md** - Code architecture
- **FEATURES.md** - What's implemented
- **BUILD_SUMMARY.md** - Complete overview

## Tech Stack (Simple Version)

| Layer | Technology |
|-------|------------|
| Interface | HTML5 + CSS3 |
| Logic | JavaScript (no framework!) |
| Backend | Python with FastAPI |
| Database | MongoDB |
| Security | JWT + Bcrypt |
| QR Codes | Python qrcode library |

## Support

- 📚 **Read Docs**: Start with QUICK_START.md
- 🧪 **Test API**: See API_TESTING.md
- 🏗️ **Understand Code**: Read PROJECT_OVERVIEW.md
- 🚀 **Deploy**: Follow DEPLOYMENT.md
- ✅ **Features**: Check FEATURES.md

## One More Thing

This is **production-ready code**! You can:
- Use it right now
- Deploy it for free
- Customize it
- Learn from it
- Build on top of it

**Let's build something cool!** 🚀

---

*For more details, see the documentation files or visit http://localhost:8000/docs when running.*
