#!/bin/bash
# Cleaner script to run tests without polluting system python

# 1. Clean up system files causing build errors
find . -name "._*" -delete

# 2. Build and start containers
docker-compose up --build -d

# 3. Wait for service to be healthy
echo "Waiting for API to be ready..."
sleep 5

# 4. Setup venv for testing
if [ ! -d "venv" ]; then
    python3 -m venv venv
    source venv/bin/activate
    pip install requests
else
    source venv/bin/activate
fi

# 5. Run verification
echo "Running verification script..."
python3 scripts/verify_async.py
