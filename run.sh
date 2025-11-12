#!/bin/bash

# Create a simple config file for testing
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

# Change to source directory and execute Python application
cd /src
exec python3 -u main.py
