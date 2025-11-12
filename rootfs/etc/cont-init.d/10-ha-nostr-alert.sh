#!/command/with-contenv bashio
# ==============================================================================
# Home Assistant Nostr Alert Initialization
# ==============================================================================

echo "=== HA Nostr Alert Initialization ==="

# Create required directories if they don't exist
if [ ! -d "/run/s6/container_environment" ]; then
    echo "Creating /run/s6/container_environment directory"
    mkdir -p /run/s6/container_environment
fi

# Set up environment variables
echo "Setting up environment variables"
echo "$(id -u)" > /run/s6/container_environment/PUID
echo "$(id -g)" > /run/s6/container_environment/PGID

# Also create a simple environment file
echo "Creating environment file"
echo "HOME=/root" > /run/s6/container_environment/HOME
echo "USER=root" > /run/s6/container_environment/USER

echo "=== Initialization Complete ==="
