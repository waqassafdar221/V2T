#!/bin/bash

# V2T Backend Stop Script
# This script stops Celery worker and FastAPI server

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Stopping V2T Backend services...${NC}"

# Stop Celery workers
echo -e "${YELLOW}Stopping Celery workers...${NC}"
if pkill -f "celery.*worker" 2>/dev/null; then
    echo -e "${GREEN}✓ Celery workers stopped${NC}"
else
    echo -e "${YELLOW}No Celery workers running${NC}"
fi

# Stop FastAPI server
echo -e "${YELLOW}Stopping FastAPI server...${NC}"
if pkill -f "uvicorn main:app" 2>/dev/null; then
    echo -e "${GREEN}✓ FastAPI server stopped${NC}"
else
    echo -e "${YELLOW}No FastAPI server running${NC}"
fi

# Optionally stop Redis (usually keep it running)
# echo -e "${YELLOW}Stopping Redis...${NC}"
# brew services stop redis

echo -e "${GREEN}All services stopped${NC}"
