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

# Create a minimal default config file to avoid any issues
echo "=== Creating config file ==="
cat > /config.yaml <<EOF
nostr:
  relay_url: "wss://relay.damus.io"
  recipient_npub: ""
  private_key: ""

alerts:
  monitored_entities: []
  consolidated_entities: []

queue:
  max_size: 5
EOF

# Show what we created
echo "=== Config file contents ==="
cat /config.yaml

# Simple approach - just start the Python application directly
echo "=== Starting Python application ==="
cd /src
echo "Current directory: $(pwd)"
ls -la
exec python3 -u main.py
