#!/bin/bash
# ==============================================================================
# Home Assistant Add-on: HA Nostr Alert
# ==============================================================================

# Create a minimal default config file to avoid any issues
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

# Simple approach - just start the Python application directly
cd /src
exec python3 -u main.py
