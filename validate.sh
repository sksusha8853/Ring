#!/bin/bash

# QR Contact App - Validation Script
# Checks if everything is properly set up

echo "🔍 QR Contact App - Setup Validation"
echo "===================================="
echo ""

ERRORS=0
WARNINGS=0

# Check Python
echo "Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found"
    ERRORS=$((ERRORS + 1))
else
    PYTHON_VERSION=$(python3 --version 2>&1)
    echo "✅ $PYTHON_VERSION"
fi

# Check virtual environment
echo ""
echo "Checking virtual environment..."
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not created (run ./setup.sh first)"
    WARNINGS=$((WARNINGS + 1))
else
    echo "✅ Virtual environment exists"
fi

# Check backend files
echo ""
echo "Checking backend files..."
BACKEND_FILES=("backend/main.py" "backend/config.py" "backend/database.py" "backend/auth.py" "backend/models.py" "backend/requirements.txt")
for file in "${BACKEND_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file missing"
        ERRORS=$((ERRORS + 1))
    fi
done

# Check frontend files
echo ""
echo "Checking frontend files..."
FRONTEND_FILES=("frontend/index.html" "frontend/profile.html" "frontend/style.css" "frontend/script.js" "frontend/profile-script.js")
for file in "${FRONTEND_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file missing"
        ERRORS=$((ERRORS + 1))
    fi
done

# Check documentation
echo ""
echo "Checking documentation..."
DOC_FILES=("README.md" "QUICK_START.md" "DEPLOYMENT.md" "PROJECT_OVERVIEW.md")
for file in "${DOC_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file missing"
        WARNINGS=$((WARNINGS + 1))
    fi
done

# Check .env
echo ""
echo "Checking environment configuration..."
if [ -f ".env" ]; then
    echo "✅ .env file exists"
    if grep -q "MONGODB_URL" .env; then
        echo "✅ MONGODB_URL configured"
    else
        echo "⚠️  MONGODB_URL not configured"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo "⚠️  .env file not found (copy from .env.example)"
    WARNINGS=$((WARNINGS + 1))
fi

# Check MongoDB
echo ""
echo "Checking MongoDB..."
if ! command -v mongod &> /dev/null && ! command -v mongo &> /dev/null; then
    echo "⚠️  MongoDB CLI not found (might still work if using Atlas)"
    WARNINGS=$((WARNINGS + 1))
else
    echo "✅ MongoDB CLI found"
fi

# Test Python imports (if venv exists)
if [ -d "venv" ]; then
    echo ""
    echo "Testing Python imports..."
    source venv/bin/activate
    
    if python3 -c "import fastapi" 2>/dev/null; then
        echo "✅ FastAPI installed"
    else
        echo "⚠️  FastAPI not installed (run pip install -r backend/requirements.txt)"
        WARNINGS=$((WARNINGS + 1))
    fi
    
    if python3 -c "import pymongo" 2>/dev/null; then
        echo "✅ PyMongo installed"
    else
        echo "⚠️  PyMongo not installed"
        WARNINGS=$((WARNINGS + 1))
    fi
    
    if python3 -c "import qrcode" 2>/dev/null; then
        echo "✅ QRCode installed"
    else
        echo "⚠️  QRCode not installed"
        WARNINGS=$((WARNINGS + 1))
    fi
fi

# Summary
echo ""
echo "===================================="
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo "✅ All checks passed! Ready to run."
    echo ""
    echo "Next steps:"
    echo "1. Start MongoDB"
    echo "2. Run: bash run.sh"
    echo "3. Open: http://localhost:8001"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo "⚠️  Setup complete with $WARNINGS warnings"
    echo ""
    echo "You can still run the app, but check the warnings above."
    exit 0
else
    echo "❌ Setup incomplete: $ERRORS errors, $WARNINGS warnings"
    echo ""
    echo "Please fix the errors above and run setup.sh again"
    exit 1
fi
