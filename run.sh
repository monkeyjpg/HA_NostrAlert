#!/usr/bin/with-contenv bashio
# ==============================================================================
# Home Assistant Add-on: HA Nostr Alert
# ==============================================================================

# Log environment information for debugging
echo "=== Environment Debug Info ==="
echo "PID: $$"
echo "User: $(id)"
echo "Working directory: $(pwd)"

# Show configuration if it exists
echo "=== Configuration Debug Info ==="
if [ -f "/data/options.json" ]; then
    echo "Options file exists:"
    cat /data/options.json
else
    echo "No options file found"
fi

# Change to src directory and start the Python application
cd /src
echo "=== Starting Python application ==="
echo "Current directory: $(pwd)"
ls -la
exec python3 -u main.py
