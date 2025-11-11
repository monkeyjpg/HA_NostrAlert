"""
Nostr client for sending NIP-17 encrypted DMs
"""
from nostr_sdk import Client, Keys, PublicKey, EventBuilder, NostrSigner, RelayUrl
import logging
import time
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NostrClient:
    def __init__(self, config):
        self.config = config
        self.client = None
        self.keys = None
        self.signer = None
        self.recipient_public_key = None
        self.connected = False
        self.connect()  # Initialize components immediately
    
    def connect(self):
        """Initialize Nostr client components"""
        try:
            # Create keys from private key in config
            self.keys = Keys.parse(self.config.private_key)
            
            # Create signer from keys
            self.signer = NostrSigner.keys(self.keys)
            
            # Parse recipient public key
            self.recipient_public_key = PublicKey.parse(self.config.recipient_npub)
            
            # Create client with signer
            self.client = Client(self.signer)
            
            logger.info(f"Initialized Nostr client for relay: {self.config.relay_url}")
            
        except Exception as e:
            logger.error(f"Error initializing Nostr client: {e}")
            raise
    
    async def connect_relay(self):
        """Connect to Nostr relay"""
        try:
            # Parse relay URL
            relay_url = RelayUrl.parse(self.config.relay_url)
            
            # Add relay with timeout
            await self.client.add_relay(relay_url)
            
            # Connect to relay with timeout
            await asyncio.wait_for(self.client.connect(), timeout=15.0)
            
            # Wait a bit for the connection to stabilize
            await asyncio.sleep(2)
            
            # Check if relay is actually connected by trying to get relay info
            try:
                relays = await asyncio.wait_for(self.client.relays(), timeout=5.0)
                if relay_url in relays:
                    relay = relays[relay_url]
                    if relay.is_connected():
                        logger.debug(f"Relay {relay_url} is connected")
                        self.connected = True
                    else:
                        logger.debug(f"Relay {relay_url} is not connected")
                        self.connected = False
                else:
                    logger.debug(f"Relay {relay_url} not found in relays list")
                    self.connected = False
            except Exception as e:
                logger.debug(f"Could not get relay info: {e}")
                self.connected = False
            
            if self.connected:
                logger.info(f"Connected to Nostr relay: {self.config.relay_url}")
            else:
                logger.error(f"Failed to connect to Nostr relay: {self.config.relay_url}")
                raise Exception(f"Relay connection failed: {self.config.relay_url}")
            
        except asyncio.TimeoutError:
            logger.error(f"Timeout connecting to Nostr relay: {self.config.relay_url}")
            self.connected = False
            raise
        except Exception as e:
            logger.error(f"Error connecting to Nostr relay: {e}")
            self.connected = False
            raise
    
    async def send_dm(self, message):
        """Send encrypted DM using NIP-17"""
        try:
            # Ensure we're connected before sending
            if not self.connected:
                await self.connect_relay()
            
            # Send encrypted direct message with timeout
            event_id = await asyncio.wait_for(
                self.client.send_private_msg(self.recipient_public_key, message),
                timeout=15.0
            )
            logger.info(f"Sent DM with event ID: {event_id}")
            return event_id
        except asyncio.TimeoutError:
            logger.error("Timeout sending DM")
            # Try to reconnect and resend
            try:
                await self.connect_relay()
                event_id = await asyncio.wait_for(
                    self.client.send_private_msg(self.recipient_public_key, message),
                    timeout=15.0
                )
                logger.info(f"Resent DM with event ID: {event_id}")
                return event_id
            except Exception as e2:
                logger.error(f"Error resending DM: {e2}")
                raise e2
        except Exception as e:
            logger.error(f"Error sending DM: {e}")
            # Try to reconnect and resend
            try:
                await self.connect_relay()
                event_id = await asyncio.wait_for(
                    self.client.send_private_msg(self.recipient_public_key, message),
                    timeout=15.0
                )
                logger.info(f"Resent DM with event ID: {event_id}")
                return event_id
            except Exception as e2:
                logger.error(f"Error resending DM: {e2}")
                raise e2
    
    async def disconnect(self):
        """Disconnect from Nostr relay"""
        if self.client and self.connected:
            try:
                await asyncio.wait_for(self.client.disconnect(), timeout=5.0)
                self.connected = False
                logger.info("Disconnected from Nostr relay")
            except asyncio.TimeoutError:
                logger.error("Timeout disconnecting from Nostr relay")
                self.connected = False
            except Exception as e:
                logger.error(f"Error disconnecting from Nostr relay: {e}")
                self.connected = False

# Example of how to use the Nostr client
if __name__ == "__main__":
    # This is just for testing the Nostr client independently
    from config import Config
    config = Config()
    
    async def test_client():
        try:
            nostr_client = NostrClient(config)
            # nostr_client.connect()  # Already called in __init__
            await nostr_client.connect_relay()
            await nostr_client.send_dm("Test message from HA Nostr Alert")
            await nostr_client.disconnect()
        except Exception as e:
            logger.error(f"Error in Nostr client test: {e}")
    
    # Run the async function
    asyncio.run(test_client())
