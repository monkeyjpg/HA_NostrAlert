"""
Nostr client for sending NIP-17 encrypted DMs
"""
from nostr_sdk import Client, Keys, PublicKey, EventBuilder
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NostrClient:
    def __init__(self, config):
        self.config = config
        self.client = None
        self.keys = None
        self.recipient_public_key = None
        self.connect()
    
    def connect(self):
        """Connect to Nostr relay"""
        try:
            # Create keys from private key in config
            self.keys = Keys.parse(self.config.private_key)
            
            # Parse recipient public key
            self.recipient_public_key = PublicKey.parse(self.config.recipient_npub)
            
            # Create client
            self.client = Client(self.keys)
            
            # Add relay
            self.client.add_relay(self.config.relay_url)
            
            # Connect to relay
            self.client.connect()
            logger.info(f"Connected to Nostr relay: {self.config.relay_url}")
            
        except Exception as e:
            logger.error(f"Error connecting to Nostr relay: {e}")
            raise
    
    def send_dm(self, message):
        """Send encrypted DM using NIP-17"""
        try:
            # Create and send encrypted direct message
            event = EventBuilder.encrypted_direct_msg(self.keys, self.recipient_public_key, message)
            event_id = self.client.send_event(event)
            logger.info(f"Sent DM with event ID: {event_id}")
            return event_id
        except Exception as e:
            logger.error(f"Error sending DM: {e}")
            # Try to reconnect and resend
            try:
                self.connect()
                event = EventBuilder.encrypted_direct_msg(self.keys, self.recipient_public_key, message)
                event_id = self.client.send_event(event)
                logger.info(f"Resent DM with event ID: {event_id}")
                return event_id
            except Exception as e2:
                logger.error(f"Error resending DM: {e2}")
                raise e
    
    def disconnect(self):
        """Disconnect from Nostr relay"""
        if self.client:
            self.client.disconnect()
            logger.info("Disconnected from Nostr relay")

# Example of how to use the Nostr client
if __name__ == "__main__":
    # This is just for testing the Nostr client independently
    from config import Config
    config = Config()
    
    try:
        nostr_client = NostrClient(config)
        nostr_client.send_dm("Test message from HA Nostr Alert")
        nostr_client.disconnect()
    except Exception as e:
        logger.error(f"Error in Nostr client test: {e}")
