#!/command/with-contenv bashio

# ==============================================================================
# Home Assistant Add-on: HA Nostr Alert
# ==============================================================================

# Read configuration from Home Assistant
RELAY_URL=$(bashio::config 'relay_url')
RECIPIENT_NPUB=$(bashio::config 'recipient_npub')
PRIVATE_KEY=$(bashio::config 'private_key')

# Create application config.yaml
cat > /config.yaml <<EOF
nostr:
  relay_url: "${RELAY_URL}"
  recipient_npub: "${RECIPIENT_NPUB}"
  private_key: "${PRIVATE_KEY}"

alerts:
  monitored_entities:
EOF

bashio::config 'monitored_entities' | jq -r '.[]' | while read entity; do
  echo "    - \"${entity}\"" >> /config.yaml
done

echo "  consolidated_entities:" >> /config.yaml

bashio::config 'consolidated_entities' | jq -r '.[]' | while read entity; do
  echo "    - \"${entity}\"" >> /config.yaml
done

cat >> /config.yaml <<EOF

queue:
  max_size: 5
EOF

# Change to source directory and execute Python application
cd /src
exec python3 -u main.py
