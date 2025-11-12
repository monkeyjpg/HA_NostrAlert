#!/command/with-contenv bashio
# ==============================================================================
# Home Assistant Add-on: HA Nostr Alert
# ==============================================================================

# Add some debugging to see if this script is being executed
echo "=== HA Nostr Alert run.sh started ==="
echo "Current directory: $(pwd)"
echo "User: $(id)"
echo "Environment variables:"
env | grep -E "(HOME|USER|PATH)" || true

# Check if we have the required files
echo "Checking for required files..."
if [ -d "/src" ]; then
    echo "Found /src directory"
    ls -la /src || true
else
    echo "ERROR: /src directory not found!"
    exit 1
fi

if [ -f "/src/main.py" ]; then
    echo "Found main.py"
else
    echo "ERROR: main.py not found!"
    exit 1
fi

# Check for configuration
echo "Checking for configuration..."
if [ -f "/data/options.json" ]; then
    echo "Found Home Assistant options.json:"
    cat /data/options.json || true
elif [ -f "/config.yaml" ]; then
    echo "Found config.yaml:"
    cat /config.yaml || true
else
    echo "No configuration file found"
fi

# Start the Python application
echo "=== Starting Python application ==="
cd /src
python3 -u main.py
