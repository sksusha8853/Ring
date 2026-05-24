from fastapi import FastAPI, HTTPException, status, Depends, Request
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from datetime import timedelta, datetime, timezone
from bson.objectid import ObjectId
import qrcode
import io
import logging
import os
from pathlib import Path

from config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    APP_NAME,
    APP_URL,
)
from database import connect_to_mongo, close_mongo_connection, get_database
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token,
    get_current_user,
    validate_phone,
    validate_username,
)
from models import (
    UserSignup,
    UserLogin,
    UserUpdate,
    UserResponse,
    LoginResponse,
    PublicProfileResponse,
    ErrorResponse,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title=APP_NAME, version="1.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup and Shutdown events
@app.on_event("startup")
async def startup_event():
    """Connect to MongoDB on startup"""
    try:
        connect_to_mongo()
        logger.info("Application started successfully")
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Close MongoDB connection on shutdown"""
    close_mongo_connection()

# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================

@app.post("/signup", response_model=LoginResponse, status_code=status.HTTP_201_CREATED)
async def signup(user: UserSignup):
    """
    User signup endpoint
    Creates a new user account with username, password, phone, and WhatsApp number
    """
    # Validate username format
    if not validate_username(user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username must be 3-50 characters and contain only alphanumeric characters and underscores"
        )
    
    # Validate phone number
    if not validate_phone(user.phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid phone number format. Must contain at least 10 digits"
        )
    
    # Validate WhatsApp number
    if not validate_phone(user.whatsapp):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid WhatsApp number format. Must contain at least 10 digits"
        )
    
    if not user.password or len(user.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters"
        )
    
    db = get_database()
    users_collection = db['users']
    
    # Check if username already exists
    existing_user = users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new user
    from datetime import datetime
    hashed_password = hash_password(user.password)
    new_user = {
        "username": user.username,
        "password_hash": hashed_password,
        "phone": user.phone,
        "whatsapp": user.whatsapp,
        "instructions": user.instructions,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }
    
    result = users_collection.insert_one(new_user)
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    profile_url = f"{APP_URL}/u/{user.username}"
    user_response = UserResponse(
        username=user.username,
        phone=user.phone,
        whatsapp=user.whatsapp,
        instructions=user.instructions,
        created_at=new_user["created_at"],
        updated_at=new_user["updated_at"],
        profile_url=profile_url
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_response
    )

@app.post("/login", response_model=LoginResponse)
async def login(credentials: UserLogin):
    """
    User login endpoint
    Authenticates user with username and password, returns JWT token
    """
    db = get_database()
    users_collection = db['users']
    
    # Find user by username
    user = users_collection.find_one({"username": credentials.username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Verify password
    if not verify_password(credentials.password, user['password_hash']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['username']},
        expires_delta=access_token_expires
    )
    
    profile_url = f"{APP_URL}/u/{user['username']}"
    user_response = UserResponse(
        username=user['username'],
        phone=user['phone'],
        whatsapp=user['whatsapp'],
        instructions=user['instructions'],
        created_at=user.get('created_at'),
        updated_at=user.get('updated_at'),
        profile_url=profile_url
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_response
    )

# ============================================================================
# USER PROFILE ROUTES
# ============================================================================

@app.get("/me", response_model=UserResponse)
async def get_current_user_profile(username: str = Depends(get_current_user)):
    """
    Get current user's profile (protected route)
    Requires valid JWT token
    """
    db = get_database()
    users_collection = db['users']
    
    user = users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    profile_url = f"{APP_URL}/u/{user['username']}"
    return UserResponse(
        username=user['username'],
        phone=user['phone'],
        whatsapp=user['whatsapp'],
        instructions=user['instructions'],
        created_at=user.get('created_at'),
        updated_at=user.get('updated_at'),
        profile_url=profile_url
    )

@app.put("/me", response_model=UserResponse)
async def update_user_profile(
    update_data: UserUpdate,
    username: str = Depends(get_current_user)
):
    """
    Update current user's profile (protected route)
    Can update phone, whatsapp, and instructions
    """
    db = get_database()
    users_collection = db['users']
    
    # Validate inputs if provided
    if update_data.phone and not validate_phone(update_data.phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid phone number format"
        )
    
    if update_data.whatsapp and not validate_phone(update_data.whatsapp):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid WhatsApp number format"
        )
    
    # Build update data
    update_fields = {"updated_at": datetime.now(timezone.utc)}
    
    if update_data.phone:
        update_fields['phone'] = update_data.phone
    if update_data.whatsapp:
        update_fields['whatsapp'] = update_data.whatsapp
    if update_data.instructions is not None:
        update_fields['instructions'] = update_data.instructions
    
    # Update user
    result = users_collection.update_one(
        {"username": username},
        {"$set": update_fields}
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Fetch updated user
    user = users_collection.find_one({"username": username})
    
    profile_url = f"{APP_URL}/u/{user['username']}"
    return UserResponse(
        username=user['username'],
        phone=user['phone'],
        whatsapp=user['whatsapp'],
        instructions=user['instructions'],
        created_at=user.get('created_at'),
        updated_at=user.get('updated_at'),
        profile_url=profile_url
    )

# ============================================================================
# PUBLIC PROFILE ROUTES
# ============================================================================

@app.get("/u/{username}")
async def get_public_profile(username: str, request: Request):
    """
    Get public profile for a user (no authentication required)
    Returns HTML for browser requests or JSON for API requests
    Also tracks visit analytics
    """
    db = get_database()
    users_collection = db['users']
    
    # Find user
    user = users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Record visit analytics
    visits_collection = db['visits']
    visits_collection.insert_one({
        "username": username,
        "ip_address": request.client.host if request.client else "unknown",
        "user_agent": request.headers.get("user-agent", "unknown"),
        "timestamp": datetime.now(timezone.utc)
    })
    
    # Check if browser request or API request
    accept_header = request.headers.get("accept", "")
    if "text/html" in accept_header and "application/json" not in accept_header:
        # Serve HTML for browser
        html_content = _get_profile_html(
            user['username'],
            user['phone'],
            user['whatsapp'],
            user['instructions'],
            user.get('updated_at')
        )
        return HTMLResponse(content=html_content)
    
    # Return JSON for API requests
    return PublicProfileResponse(
        username=user['username'],
        phone=user['phone'],
        whatsapp=user['whatsapp'],
        instructions=user['instructions'],
        updated_at=user.get('updated_at')
    )

def _get_profile_html(username: str, phone: str, whatsapp: str, instructions: str, updated_at) -> str:
    """Generate HTML for profile page"""
    from datetime import datetime
    
    last_updated = datetime.fromisoformat(updated_at.isoformat()).strftime('%b %d, %Y at %I:%M %p')
    
    # Escape HTML to prevent XSS
    def escape(text):
        if not text:
            return ""
        return (text.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                    .replace('"', "&quot;")
                    .replace("'", "&#039;"))
    
    phone_display = escape(phone)
    whatsapp_display = escape(whatsapp)
    instructions_display = escape(instructions) if instructions else "Available for contact"
    username_display = escape(username)
    
    # Clean phone number for WhatsApp (remove non-digits)
    whatsapp_clean = ''.join(c for c in whatsapp if c.isdigit())
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{username_display} - QR Contact</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1rem;
        }}
        
        .profile-display {{
            background-color: white;
            border-radius: 16px;
            padding: 2rem;
            max-width: 500px;
            width: 100%;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            text-align: center;
        }}
        
        .profile-display h1 {{
            font-size: 2rem;
            margin-bottom: 1rem;
            color: #007bff;
        }}
        
        .instructions-box {{
            background-color: #f8f9fa;
            padding: 1.5rem;
            border-radius: 8px;
            margin-bottom: 2rem;
            min-height: 80px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .instructions-text {{
            font-size: 1.1rem;
            line-height: 1.8;
            color: #212529;
            word-wrap: break-word;
        }}
        
        .action-buttons {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            margin: 2rem 0;
        }}
        
        .btn-call, .btn-whatsapp {{
            padding: 1rem;
            font-size: 1rem;
            font-weight: 700;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            color: white;
        }}
        
        .btn-call {{
            background-color: #4CAF50;
        }}
        
        .btn-call:hover {{
            transform: scale(1.05);
            box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
        }}
        
        .btn-whatsapp {{
            background-color: #25D366;
        }}
        
        .btn-whatsapp:hover {{
            transform: scale(1.05);
            box-shadow: 0 4px 12px rgba(37, 211, 102, 0.4);
        }}
        
        .last-updated {{
            color: #6c757d;
            font-size: 0.85rem;
            margin-top: 1.5rem;
        }}
        
        @media (max-width: 480px) {{
            .profile-display {{
                padding: 1.5rem;
            }}
            
            .profile-display h1 {{
                font-size: 1.5rem;
            }}
            
            .btn-call, .btn-whatsapp {{
                padding: 0.875rem;
                font-size: 0.95rem;
            }}
            
            .instructions-text {{
                font-size: 1rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="profile-display">
        <h1>📱 {username_display}</h1>
        
        <div class="instructions-box">
            <div class="instructions-text">{instructions_display}</div>
        </div>

        <div class="action-buttons">
            <a href="tel:{phone_display}" class="btn-call">📞 Call Now</a>
            <a href="https://wa.me/{whatsapp_clean}" target="_blank" rel="noopener noreferrer" class="btn-whatsapp">💬 WhatsApp</a>
        </div>

        <p class="last-updated">Last updated: {last_updated}</p>
    </div>
</body>
</html>"""

@app.get("/api/u/{username}", response_model=PublicProfileResponse)
async def get_public_profile_json(username: str, request: Request):
    """
    Get public profile as JSON (API endpoint)
    """
    db = get_database()
    users_collection = db['users']
    
    # Find user
    user = users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Record visit analytics
    visits_collection = db['visits']
    visits_collection.insert_one({
        "username": username,
        "ip_address": request.client.host if request.client else "unknown",
        "user_agent": request.headers.get("user-agent", "unknown"),
        "timestamp": datetime.now(timezone.utc)
    })
    
    return PublicProfileResponse(
        username=user['username'],
        phone=user['phone'],
        whatsapp=user['whatsapp'],
        instructions=user['instructions'],
        updated_at=user.get('updated_at')
    )

# ============================================================================
# QR CODE ROUTES
# ============================================================================

@app.get("/qr/{username}")
async def generate_qr_code(username: str, user: str = Depends(get_current_user)):
    """
    Generate QR code for user's public profile
    Only the user can generate their own QR code
    """
    if username != user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only generate QR code for your own profile"
        )
    
    # Verify user exists
    db = get_database()
    users_collection = db['users']
    existing_user = users_collection.find_one({"username": username})
    
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Generate QR code
    profile_url = f"{APP_URL}/u/{username}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(profile_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to bytes
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    return StreamingResponse(
        iter([img_byte_arr.getvalue()]),
        media_type="image/png",
        headers={"Content-Disposition": f"attachment; filename={username}_qr.png"}
    )

# ============================================================================
# ANALYTICS ROUTES (Optional/Bonus)
# ============================================================================

@app.get("/analytics/visits")
async def get_visit_analytics(username: str = Depends(get_current_user)):
    """
    Get visit analytics for user's profile (bonus feature)
    Returns count of visits and basic stats
    """
    if username != username:  # Authorization check
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own analytics"
        )
    
    db = get_database()
    visits_collection = db['visits']
    
    # Get visit count
    visit_count = visits_collection.count_documents({"username": username})
    
    # Get recent visits (last 30 days)
    from datetime import datetime, timedelta
    thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
    recent_visits = visits_collection.count_documents({
        "username": username,
        "timestamp": {"$gte": thirty_days_ago}
    })
    
    return {
        "username": username,
        "total_visits": visit_count,
        "visits_last_30_days": recent_visits
    }

# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app_name": APP_NAME,
        "version": "1.0.0"
    }

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
