# QR Contact App - API Testing Guide

This guide shows how to test all API endpoints.

## Setup

1. Make sure backend is running: `python backend/main.py`
2. Use Postman, curl, or the interactive docs at `http://localhost:8000/docs`

## Endpoints

### 1. Health Check

**Endpoint:** `GET /health`

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "app_name": "QR Contact App",
  "version": "1.0.0"
}
```

---

### 2. Signup

**Endpoint:** `POST /signup`

```bash
curl -X POST http://localhost:8000/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "SecurePassword123!",
    "phone": "+1234567890",
    "whatsapp": "+1234567890",
    "instructions": "Available Monday-Friday, 9AM-5PM EST"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "username": "john_doe",
    "phone": "+1234567890",
    "whatsapp": "+1234567890",
    "instructions": "Available Monday-Friday, 9AM-5PM EST",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00",
    "profile_url": "http://localhost:8000/u/john_doe"
  }
}
```

**Error: Username taken**
```json
{
  "detail": "Username already taken"
}
```

**Error: Invalid password**
```json
{
  "detail": "Password must be at least 8 characters"
}
```

---

### 3. Login

**Endpoint:** `POST /login`

```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "SecurePassword123!"
  }'
```

**Response:** (same as signup response)

**Error: Invalid credentials**
```json
{
  "detail": "Invalid username or password"
}
```

---

### 4. Get Current User Profile

**Endpoint:** `GET /me`

```bash
curl http://localhost:8000/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "username": "john_doe",
  "phone": "+1234567890",
  "whatsapp": "+1234567890",
  "instructions": "Available Monday-Friday, 9AM-5PM EST",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00",
  "profile_url": "http://localhost:8000/u/john_doe"
}
```

**Error: No token**
```json
{
  "detail": "Invalid authentication credentials"
}
```

---

### 5. Update User Profile

**Endpoint:** `PUT /me`

```bash
curl -X PUT http://localhost:8000/me \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "phone": "+0987654321",
    "whatsapp": "+0987654321",
    "instructions": "Available 10AM-6PM EST (updated)"
  }'
```

**Response:** (updated user object)

**Note:** You can update any or all fields. Send empty object `{}` to make no changes.

---

### 6. Get Public Profile (HTML)

**Endpoint:** `GET /u/{username}`

```bash
curl http://localhost:8000/u/john_doe \
  -H "Accept: text/html"
```

**Response:** HTML page with profile display

---

### 7. Get Public Profile (JSON)

**Endpoint:** `GET /api/u/{username}`

```bash
curl http://localhost:8000/api/u/john_doe
```

**Response:**
```json
{
  "username": "john_doe",
  "phone": "+1234567890",
  "whatsapp": "+1234567890",
  "instructions": "Available Monday-Friday, 9AM-5PM EST",
  "updated_at": "2024-01-15T10:30:00"
}
```

**Error: User not found**
```json
{
  "detail": "User not found"
}
```

---

### 8. Generate QR Code

**Endpoint:** `GET /qr/{username}`

```bash
curl http://localhost:8000/qr/john_doe \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -o john_doe_qr.png
```

**Response:** PNG image file

**Error: Can only generate your own QR**
```json
{
  "detail": "You can only generate QR code for your own profile"
}
```

---

### 9. Get Analytics

**Endpoint:** `GET /analytics/visits`

```bash
curl http://localhost:8000/analytics/visits \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "username": "john_doe",
  "total_visits": 42,
  "visits_last_30_days": 15
}
```

---

## Testing Flow

Here's a complete testing sequence:

### Step 1: Create an account
```bash
TOKEN=$(curl -s -X POST http://localhost:8000/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "TestPass123!",
    "phone": "+11234567890",
    "whatsapp": "+11234567890",
    "instructions": "Test instructions"
  }' | jq -r '.access_token')

echo "Token: $TOKEN"
```

### Step 2: Get your profile
```bash
curl http://localhost:8000/me \
  -H "Authorization: Bearer $TOKEN"
```

### Step 3: Update profile
```bash
curl -X PUT http://localhost:8000/me \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "instructions": "Updated instructions"
  }'
```

### Step 4: Generate QR code
```bash
curl http://localhost:8000/qr/testuser \
  -H "Authorization: Bearer $TOKEN" \
  -o testuser_qr.png
```

### Step 5: View public profile
```bash
# In browser: http://localhost:8000/u/testuser
# Or get JSON:
curl http://localhost:8000/api/u/testuser
```

### Step 6: Check analytics
```bash
curl http://localhost:8000/analytics/visits \
  -H "Authorization: Bearer $TOKEN"
```

---

## Using Postman

1. Download [Postman](https://www.postman.com/downloads/)
2. Create new collection "QR Contact App"
3. Create requests for each endpoint
4. Use environment variables for:
   - `base_url` = http://localhost:8000
   - `token` = (copy from signup response)

---

## Using curl Script

Create `test_api.sh`:

```bash
#!/bin/bash

BASE_URL="http://localhost:8000"

# 1. Signup
echo "1. Signing up..."
RESPONSE=$(curl -s -X POST $BASE_URL/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser'$(date +%s)'",
    "password": "TestPass123!",
    "phone": "+11234567890",
    "whatsapp": "+11234567890",
    "instructions": "Test"
  }')

TOKEN=$(echo $RESPONSE | jq -r '.access_token')
USERNAME=$(echo $RESPONSE | jq -r '.user.username')
echo "Created user: $USERNAME"
echo "Token: $TOKEN"

# 2. Get profile
echo ""
echo "2. Getting profile..."
curl -s $BASE_URL/me \
  -H "Authorization: Bearer $TOKEN" | jq

# 3. Update profile
echo ""
echo "3. Updating profile..."
curl -s -X PUT $BASE_URL/me \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"instructions": "Updated"}' | jq

# 4. Get public profile
echo ""
echo "4. Getting public profile..."
curl -s $BASE_URL/api/u/$USERNAME | jq

# 5. Get analytics
echo ""
echo "5. Getting analytics..."
curl -s $BASE_URL/analytics/visits \
  -H "Authorization: Bearer $TOKEN" | jq
```

Run with: `bash test_api.sh`

---

## Common Errors & Solutions

### 401 Unauthorized
**Problem:** Token is invalid or expired
**Solution:** 
- Get a new token with `/login`
- Make sure Authorization header is correct: `Authorization: Bearer TOKEN`

### 400 Bad Request
**Problem:** Invalid input data
**Solution:**
- Check field values (phone format, password length, etc.)
- See error message for specific field

### 404 Not Found
**Problem:** User doesn't exist
**Solution:**
- Check username spelling
- Verify user was created

### 403 Forbidden
**Problem:** Not authorized for this action
**Solution:**
- Can only modify own profile
- Can only generate own QR code

---

## Performance Testing

Test with multiple users:

```bash
for i in {1..10}; do
  curl -X POST http://localhost:8000/signup \
    -H "Content-Type: application/json" \
    -d "{
      \"username\": \"user$i\",
      \"password\": \"Password123!\",
      \"phone\": \"+1234567890\",
      \"whatsapp\": \"+1234567890\",
      \"instructions\": \"Test user $i\"
    }"
  echo ""
done
```

---

## Tips

- Use `jq` to format JSON output: `curl ... | jq`
- Save tokens in environment variables
- Test both happy and error paths
- Check database with MongoDB Compass
- Monitor backend logs for errors

---

**Happy testing! 🚀**
