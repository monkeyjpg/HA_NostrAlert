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
        self.connect()
    
    def connect(self):
        """Connect to Nostr relay"""
        try:
            # Create keys from private key in config
            self.keys = Keys.parse(self.config.private_key)
            
            # Create signer from keys
            self.signer = NostrSigner.keys(self.keys)
            
            # Parse recipient public key
            self.recipient_public_key = PublicKey.parse(self.config.recipient_npub)
            
            # Create client with signer
            self.client = Client(self.signer)
            
            logger.info(f"Created Nostr client for relay: {self.config.relay_url}")
            
        except Exception as e:
            logger.error(f"Error creating Nostr client: {e}")
            raise
    
    async def connect_relay(self):
        """Connect to Nostr relay"""
        try:
            # Parse relay URL
            relay_url = RelayUrl.parse(self.config.relay_url)
            
            # Add relay
            await self.client.add_relay(relay_url)
            
            # Connect to relay
            await self.client.connect()
            logger.info(f"Connected to Nostr relay: {self.config.relay_url}")
            
        except Exception as e:
            logger.error(f"Error connecting to Nostr relay: {e}")
            raise
    
    async def send_dm(self, message):
        """Send encrypted DM using NIP-17"""
        try:
            # Send encrypted direct message
            event_id = await self.client.send_private_msg(self.recipient_public_key, message)
            logger.info(f"Sent DM with event ID: {event_id}")
            return event_id
        except Exception as e:
            logger.error(f"Error sending DM: {e}")
            # Try to reconnect and resend
            try:
                await self.connect_relay()
                event_id = await self.client.send_private_msg(self.recipient_public_key, message)
                logger.info(f"Resent DM with event ID: {event_id}")
                return event_id
            except Exception as e2:
                logger.error(f"Error resending DM: {e2}")
                raise e
    
    async def disconnect(self):
        """Disconnect from Nostr relay"""
        if self.client:
            await self.client.disconnect()
            logger.info("Disconnected from Nostr relay")

# Example of how to use the Nostr client
if __name__ == "__main__":
    # This is just for testing the Nostr client independently
    from config import Config
    config = Config()
    
    async def test_client():
        try:
            nostr_client = NostrClient(config)
            await nostr_client.connect_relay()
            await nostr_client.send_dm("Test message from HA Nostr Alert")
            await nostr_client.disconnect()
        except Exception as e:
            logger.error(f"Error in Nostr client test: {e}")
    
    # Run the async function
    asyncio.run(test_client())
