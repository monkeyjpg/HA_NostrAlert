#!/command/with-contenv bashio
# ==============================================================================
# Home Assistant Nostr Alert Initialization
# ==============================================================================

echo "=== HA Nostr Alert Initialization ==="

# Create required directories
mkdir -p /run/s6/container_environment

# Set up environment variables
echo "PUID=$(id -u)" > /run/s6/container_environment/PUID
echo "PGID=$(id -g)" > /run/s6/container_environment/PGID

echo "=== Initialization Complete ==="
