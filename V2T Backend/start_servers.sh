#!/bin/bash

# V2T Backend Startup Script
# This script starts Redis, Celery worker, and FastAPI server

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   V2T Backend Startup${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Base directory
BASE_DIR="/Users/waqassafdar/V2T/V2T Backend"
cd "$BASE_DIR"

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Check Redis
echo -e "${YELLOW}Checking Redis...${NC}"
if redis-cli ping > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Redis is running${NC}"
else
    echo -e "${RED}✗ Redis is not running${NC}"
    echo -e "${YELLOW}Starting Redis...${NC}"
    brew services start redis
    sleep 2
    if redis-cli ping > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Redis started successfully${NC}"
    else
        echo -e "${RED}✗ Failed to start Redis${NC}"
        exit 1
    fi
fi

# Check FFmpeg
echo -e "${YELLOW}Checking FFmpeg...${NC}"
if command -v ffmpeg > /dev/null 2>&1; then
    echo -e "${GREEN}✓ FFmpeg is installed${NC}"
else
    echo -e "${RED}✗ FFmpeg is not installed${NC}"
    echo -e "${YELLOW}Install with: brew install ffmpeg${NC}"
    exit 1
fi

# Check Tesseract
echo -e "${YELLOW}Checking Tesseract OCR...${NC}"
if command -v tesseract > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Tesseract is installed${NC}"
else
    echo -e "${RED}✗ Tesseract is not installed${NC}"
    echo -e "${YELLOW}Install with: brew install tesseract${NC}"
    exit 1
fi

# Create upload directories
echo -e "${YELLOW}Creating upload directories...${NC}"
mkdir -p uploads/videos uploads/frames
echo -e "${GREEN}✓ Upload directories ready${NC}"

# Kill existing processes
echo -e "${YELLOW}Checking for existing processes...${NC}"
pkill -f "celery.*worker" 2>/dev/null || true
pkill -f "uvicorn main:app" 2>/dev/null || true
sleep 1

# Start Celery worker
echo -e "${YELLOW}Starting Celery worker...${NC}"
celery -A app.tasks.video_tasks worker --loglevel=info > logs/celery.log 2>&1 &
CELERY_PID=$!
sleep 3

# Check if Celery started successfully
if ps -p $CELERY_PID > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Celery worker started (PID: $CELERY_PID)${NC}"
else
    echo -e "${RED}✗ Failed to start Celery worker${NC}"
    echo -e "${YELLOW}Check logs/celery.log for details${NC}"
    exit 1
fi

# Start FastAPI server
echo -e "${YELLOW}Starting FastAPI server...${NC}"
uvicorn main:app --reload --host 0.0.0.0 --port 8000 > logs/fastapi.log 2>&1 &
FASTAPI_PID=$!
sleep 3

# Check if FastAPI started successfully
if ps -p $FASTAPI_PID > /dev/null 2>&1; then
    echo -e "${GREEN}✓ FastAPI server started (PID: $FASTAPI_PID)${NC}"
else
    echo -e "${RED}✗ Failed to start FastAPI server${NC}"
    echo -e "${YELLOW}Check logs/fastapi.log for details${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   All services started successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}Services Status:${NC}"
echo -e "  Redis:        Running (brew services)"
echo -e "  Celery:       Running (PID: $CELERY_PID)"
echo -e "  FastAPI:      Running (PID: $FASTAPI_PID)"
echo ""
echo -e "${YELLOW}Access Points:${NC}"
echo -e "  API:          http://localhost:8000"
echo -e "  Swagger Docs: http://localhost:8000/docs"
echo -e "  ReDoc:        http://localhost:8000/redoc"
echo ""
echo -e "${YELLOW}Logs:${NC}"
echo -e "  Celery:       tail -f logs/celery.log"
echo -e "  FastAPI:      tail -f logs/fastapi.log"
echo ""
echo -e "${YELLOW}Stop Services:${NC}"
echo -e "  All:          ./stop_servers.sh"
echo -e "  Celery only:  kill $CELERY_PID"
echo -e "  FastAPI only: kill $FASTAPI_PID"
echo ""
