#!/bin/bash
# ==============================================================================
# Home Assistant Add-on: HA Nostr Alert
# ==============================================================================

# Enable debug output
set -x

# Log environment information
echo "=== Environment Debug Info ==="
echo "PID: $$"
echo "User: $(id)"
echo "Working directory: $(pwd)"
echo "Environment variables:"
env | grep -E "(HOME|USER|PATH|S6|CONT)" | sort

# Show configuration if it exists
echo "=== Configuration Debug Info ==="
if [ -f "/data/options.json" ]; then
    echo "Options file exists:"
    cat /data/options.json
else
    echo "No options file found"
fi

# Simple approach - just start the Python application directly
echo "=== Starting Python application ==="
cd /src
echo "Current directory: $(pwd)"
ls -la
python3 -u main.py
