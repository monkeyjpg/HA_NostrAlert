#!/bin/bash
# ==============================================================================
# Home Assistant Add-on: HA Nostr Alert
# ==============================================================================

# Add some debugging to see if this script is being executed
echo "=== HA Nostr Alert run.sh started ==="
echo "Current directory: $(pwd)"
echo "User: $(id)"
echo "Environment variables:" >> /dev/stderr
env | grep -E "(HOME|USER|PATH)" >> /dev/stderr

# Check if we have the required files
echo "Checking for required files..."
if [ -d "/src" ]; then
    echo "Found /src directory"
    ls -la /src >> /dev/stderr
else
    echo "ERROR: /src directory not found!" >> /dev/stderr
    exit 1
fi

if [ -f "/src/main.py" ]; then
    echo "Found main.py"
else
    echo "ERROR: main.py not found!" >> /dev/stderr
    exit 1
fi

# Check for configuration
echo "Checking for configuration..."
if [ -f "/data/options.json" ]; then
    echo "Found Home Assistant options.json:" >> /dev/stderr
    cat /data/options.json >> /dev/stderr
elif [ -f "/config.yaml" ]; then
    echo "Found config.yaml:" >> /dev/stderr
    cat /config.yaml >> /dev/stderr
else
    echo "No configuration file found" >> /dev/stderr
fi

# Start the Python application
echo "=== Starting Python application ===" >> /dev/stderr
cd /src
python3 -u main.py
