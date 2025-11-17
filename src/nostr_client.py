"""
Nostr client for sending NIP-17 encrypted DMs with multi-relay failover support
"""
from nostr_sdk import Client, Keys, PublicKey, EventBuilder, NostrSigner, RelayUrl
import logging
import time
import asyncio
import random
from typing import List, Dict, Optional, Any, Union
import traceback
from exceptions import RelayConnectionError, MessageProcessingError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NostrClient:
    def __init__(self, config: Any) -> None:
        self.config = config
        self.clients: Dict[str, Client] = {}  # relay_url -> client
        self.keys: Optional[Keys] = None
        self.signer: Optional[NostrSigner] = None
        self.recipient_public_key: Optional[PublicKey] = None
        self.active_relay: Optional[str] = None
        self.relay_status: Dict[str, Dict[str, Union[bool, int, float]]] = {}  # relay_url -> {connected, last_checked, failure_count}
        self.health_check_task: Optional[asyncio.Task] = None
        self.connect()  # Initialize components immediately
    
    def connect(self) -> None:
        """Initialize Nostr client components"""
        try:
            # Create keys from private key in config (only if provided)
            if self.config.private_key:
                self.keys = Keys.parse(self.config.private_key)
            else:
                # Create random keys for testing
                self.keys = Keys.generate()
            
            # Parse recipient public key (only if provided)
            if self.config.recipient_npub:
                try:
                    self.recipient_public_key = PublicKey.parse(self.config.recipient_npub)
                except Exception as e:
                    logger.warning(f"Invalid recipient public key, generating random one for testing: {e}")
                    # Generate a random public key for testing
                    test_keys = Keys.generate()
                    self.recipient_public_key = test_keys.public_key()
            else:
                # Generate a random public key for testing
                test_keys = Keys.generate()
                self.recipient_public_key = test_keys.public_key()
            
            # Create signer from keys
            self.signer = NostrSigner.keys(self.keys)
            
            # Initialize relay status tracking
            for relay_url in self.config.relay_urls:
                self.relay_status[relay_url] = {
                    'connected': False,
                    'last_checked': 0,
                    'failure_count': 0
                }
            
            logger.info(f"Initialized Nostr client with {len(self.config.relay_urls)} relays")
            
        except Exception as e:
            logger.error(f"Error initializing Nostr client: {e}")
            raise  # Re-raise the exception
    
    async def connect_to_relay(self, relay_url: str) -> bool:
        """Connect to a specific Nostr relay"""
        try:
            # If we already have a client for this relay, disconnect it first to avoid stale connections
            if relay_url in self.clients:
                try:
                    old_client = self.clients[relay_url]
                    await asyncio.wait_for(old_client.disconnect(), timeout=5.0)
                    logger.debug(f"Disconnected stale client for relay {relay_url}")
                except Exception as e:
                    logger.debug(f"Error disconnecting stale client for {relay_url}: {e}")
                finally:
                    # Remove the old client
                    if relay_url in self.clients:
                        del self.clients[relay_url]
            
            # Create a fresh client for this relay
            client = Client(self.signer)
            self.clients[relay_url] = client
            
            # Parse relay URL
            parsed_relay_url = RelayUrl.parse(relay_url)
            
            # Add relay with timeout
            await asyncio.wait_for(client.add_relay(parsed_relay_url), timeout=15.0)
            
            # Connect to relay with timeout
            await asyncio.wait_for(client.connect(), timeout=15.0)
            
            # Wait a bit for the connection to stabilize
            await asyncio.sleep(2)
            
            # Check if relay is actually connected by trying to get relay info
            try:
                relays = await asyncio.wait_for(client.relays(), timeout=5.0)
                if parsed_relay_url in relays:
                    relay = relays[parsed_relay_url]
                    if relay.is_connected():
                        logger.debug(f"Relay {relay_url} is connected")
                        self.relay_status[relay_url]['connected'] = True
                        self.relay_status[relay_url]['failure_count'] = 0
                        return True
                    else:
                        logger.debug(f"Relay {relay_url} is not connected")
                        self.relay_status[relay_url]['connected'] = False
                else:
                    logger.debug(f"Relay {relay_url} not found in relays list")
                    self.relay_status[relay_url]['connected'] = False
            except Exception as e:
                logger.debug(f"Could not get relay info for {relay_url}: {e}")
                self.relay_status[relay_url]['connected'] = False
                
        except asyncio.TimeoutError:
            logger.error(f"Timeout connecting to Nostr relay: {relay_url}")
            self.relay_status[relay_url]['connected'] = False
            self.relay_status[relay_url]['failure_count'] += 1
        except Exception as e:
            logger.error(f"Error connecting to Nostr relay {relay_url}: {e}")
            self.relay_status[relay_url]['connected'] = False
            self.relay_status[relay_url]['failure_count'] += 1
        finally:
            # Clean up client if connection failed
            if relay_url in self.relay_status and not self.relay_status[relay_url]['connected']:
                if relay_url in self.clients:
                    try:
                        await asyncio.wait_for(self.clients[relay_url].disconnect(), timeout=5.0)
                    except:
                        pass
                    del self.clients[relay_url]
            
        return False
    
    async def verify_relay_connection(self, relay_url: str) -> bool:
        """Verify that a relay connection is still active with active testing"""
        if relay_url not in self.clients:
            return False
            
        # Don't rely solely on internal status, actively test the connection
        try:
            client = self.clients[relay_url]
            
            # First check if client thinks it's connected
            relays = await asyncio.wait_for(client.relays(), timeout=5.0)
            parsed_relay_url = RelayUrl.parse(relay_url)
            
            if parsed_relay_url not in relays:
                logger.debug(f"Relay {relay_url} not found in client relays")
                self.relay_status[relay_url]['connected'] = False
                return False
            
            relay = relays[parsed_relay_url]
            if not relay.is_connected():
                logger.debug(f"Relay {relay_url} reports not connected")
                self.relay_status[relay_url]['connected'] = False
                return False
            
            # Actively test the connection by sending a lightweight request
            # We'll subscribe to a filter that shouldn't return any events as a keepalive
            try:
                from nostr_sdk import Filter, Kind
                # Create a filter that's unlikely to match any events (using a future date)
                future_timestamp = int(time.time()) + 86400  # 24 hours in the future
                filter_obj = Filter().kinds([Kind(65535)]).since(future_timestamp)
                
                # Try to send the subscription - this will fail if connection is dead
                await asyncio.wait_for(client.req_events_of([filter_obj]), timeout=5.0)
                logger.debug(f"Active connection test successful for {relay_url}")
                self.relay_status[relay_url]['connected'] = True
                return True
            except asyncio.TimeoutError:
                logger.debug(f"Active connection test timeout for {relay_url}")
                self.relay_status[relay_url]['connected'] = False
                return False
            except Exception as active_test_error:
                logger.debug(f"Active connection test failed for {relay_url}: {active_test_error}")
                # Some errors might indicate the connection is still alive
                # Check if it's a "no events found" type error which is actually good
                error_str = str(active_test_error).lower()
                if "timeout" in error_str or "disconnected" in error_str or "closed" in error_str:
                    self.relay_status[relay_url]['connected'] = False
                    return False
                else:
                    # Other errors might not indicate connection problems
                    logger.debug(f"Active test error may not indicate connection issue: {active_test_error}")
                    self.relay_status[relay_url]['connected'] = True
                    return True
                
        except Exception as e:
            logger.debug(f"Connection verification failed for relay {relay_url}: {e}")
            self.relay_status[relay_url]['connected'] = False
            return False
    
    async def connect_to_primary_relay(self) -> bool:
        """Connect to the primary (first) relay, or failover to next available"""
        for relay_url in self.config.relay_urls:
            if await self.connect_to_relay(relay_url):
                self.active_relay = relay_url
                logger.info(f"Connected to primary relay: {relay_url}")
                return True
        
        logger.error("Failed to connect to any relay")
        self.active_relay = None
        return False
    
    async def send_dm(self, message: str) -> Optional[str]:
        """Send encrypted DM using NIP-17 with failover support"""
        # Ensure we have a recipient public key
        if not self.recipient_public_key:
            logger.error("No recipient public key configured")
            return None
            
        # Ensure we have an active relay, or establish one
        if not self.active_relay or not self.relay_status[self.active_relay]['connected']:
            logger.info("No active relay or connection lost, attempting to connect to primary relay")
            if not await self.connect_to_primary_relay():
                logger.error("Failed to establish connection to any relay")
                return None
        
        # Verify the active relay is still connected before sending
        if not await self.verify_relay_connection(self.active_relay):
            logger.warning(f"Active relay {self.active_relay} connection verification failed")
            # Try to reconnect to the active relay first
            if not await self.connect_to_relay(self.active_relay):
                # If that fails, try to connect to primary relay
                if not await self.connect_to_primary_relay():
                    logger.error("Failed to reconnect to any relay")
                    return None
        
        # Try to send message with the active relay
        try:
            client = self.clients[self.active_relay]
            
            # Send encrypted direct message with timeout
            event_id = await asyncio.wait_for(
                client.send_private_msg(self.recipient_public_key, message),
                timeout=15.0
            )
            logger.info(f"Sent DM with event ID: {event_id} via relay {self.active_relay}")
            return str(event_id)
            
        except asyncio.TimeoutError:
            logger.error(f"Timeout sending DM via relay {self.active_relay}")
            # Mark relay as disconnected and try failover
            self.relay_status[self.active_relay]['connected'] = False
            self.relay_status[self.active_relay]['failure_count'] += 1
            
        except Exception as e:
            logger.error(f"Error sending DM via relay {self.active_relay}: {e}")
            # Mark relay as disconnected and try failover
            self.relay_status[self.active_relay]['connected'] = False
            self.relay_status[self.active_relay]['failure_count'] += 1
        
        # Try failover to next available relay
        logger.info("Attempting failover to next available relay")
        for relay_url in self.config.relay_urls:
            # Skip the currently failed relay
            if relay_url == self.active_relay:
                continue
                
            if await self.connect_to_relay(relay_url):
                self.active_relay = relay_url
                try:
                    client = self.clients[self.active_relay]
                    event_id = await asyncio.wait_for(
                        client.send_private_msg(self.recipient_public_key, message),
                        timeout=15.0
                    )
                    logger.info(f"Sent DM with event ID: {event_id} via failover relay {self.active_relay}")
                    return str(event_id)
                except Exception as e2:
                    logger.error(f"Error sending DM via failover relay {self.active_relay}: {e2}")
                    self.relay_status[self.active_relay]['connected'] = False
                    self.relay_status[self.active_relay]['failure_count'] += 1
        
        logger.error("Failed to send DM via any relay")
        return None
    
    async def health_check_relays(self) -> None:
        """Periodically check relay health and attempt reconnections"""
        while True:
            try:
                health_config = self.config.relay_health_config
                check_interval = health_config.get('check_interval', 300)  # Default 5 minutes
                
                logger.debug("Running relay health check")
                
                # Check each relay
                for relay_url in self.config.relay_urls:
                    status = self.relay_status[relay_url]
                    current_time = time.time()
                    
                    # Skip if checked recently (within last 60 seconds)
                    if current_time - status['last_checked'] < 60:
                        continue
                    
                    status['last_checked'] = current_time
                    
                    # If relay is connected, send a keepalive ping
                    if status['connected']:
                        logger.debug(f"Sending keepalive ping to relay {relay_url}")
                        if not await self._send_keepalive_ping(relay_url):
                            logger.warning(f"Keepalive ping failed for relay {relay_url}")
                            status['connected'] = False
                    
                    # If relay is disconnected and we haven't exceeded retry attempts
                    if not status['connected'] and status['failure_count'] < health_config.get('retry_attempts', 3):
                        logger.info(f"Attempting to reconnect to relay {relay_url}")
                        await self.connect_to_relay(relay_url)
                
                # Wait for next check
                await asyncio.sleep(check_interval)
                
            except asyncio.CancelledError:
                logger.info("Health check task cancelled")
                break
            except Exception as e:
                logger.error(f"Error in relay health check: {e}")
                await asyncio.sleep(60)  # Wait 1 minute on error
    
    async def _send_keepalive_ping(self, relay_url: str) -> bool:
        """Send a lightweight keepalive ping to maintain connection"""
        if relay_url not in self.clients:
            return False
            
        try:
            client = self.clients[relay_url]
            
            # Send a lightweight request to keep the connection alive
            # We'll subscribe to a filter that shouldn't return any events
            from nostr_sdk import Filter, Kind
            # Create a filter that's unlikely to match any events (using a future date)
            future_timestamp = int(time.time()) + 86400  # 24 hours in the future
            filter_obj = Filter().kinds([Kind(65535)]).since(future_timestamp)
            
            # Send the subscription request with a short timeout
            await asyncio.wait_for(client.req_events_of([filter_obj]), timeout=3.0)
            logger.debug(f"Keepalive ping successful for {relay_url}")
            return True
        except Exception as e:
            logger.debug(f"Keepalive ping failed for {relay_url}: {e}")
            return False
    
    async def start_health_monitoring(self) -> None:
        """Start background health monitoring task"""
        if self.health_check_task is None or self.health_check_task.done():
            self.health_check_task = asyncio.create_task(self.health_check_relays())
            logger.info("Started relay health monitoring")
    
    async def stop_health_monitoring(self) -> None:
        """Stop background health monitoring task"""
        if self.health_check_task and not self.health_check_task.done():
            self.health_check_task.cancel()
            try:
                await self.health_check_task
            except asyncio.CancelledError:
                pass
            logger.info("Stopped relay health monitoring")
    
    async def disconnect_all(self) -> None:
        """Disconnect from all Nostr relays"""
        logger.info("Disconnecting from all Nostr relays")
        
        # Create a list of relay URLs to avoid dictionary modification during iteration
        relay_urls = list(self.clients.keys())
        
        for relay_url in relay_urls:
            try:
                client = self.clients[relay_url]
                # Cancel any pending tasks associated with this client
                if hasattr(client, 'close_subscription'):
                    try:
                        await client.close_subscription()
                    except:
                        pass
                
                # Disconnect with timeout
                await asyncio.wait_for(client.disconnect(), timeout=5.0)
                self.relay_status[relay_url]['connected'] = False
                logger.info(f"Disconnected from Nostr relay: {relay_url}")
            except asyncio.TimeoutError:
                logger.error(f"Timeout disconnecting from Nostr relay: {relay_url}")
                self.relay_status[relay_url]['connected'] = False
            except Exception as e:
                logger.error(f"Error disconnecting from Nostr relay {relay_url}: {e}")
                self.relay_status[relay_url]['connected'] = False
            finally:
                # Always remove the client from our tracking
                if relay_url in self.clients:
                    del self.clients[relay_url]
        
        self.active_relay = None
        logger.info("Finished disconnecting from all Nostr relays")

# Example of how to use the Nostr client
if __name__ == "__main__":
    # This is just for testing the Nostr client independently
    from config import Config
    config = Config()
    
    async def test_client():
        try:
            nostr_client = NostrClient(config)
            # nostr_client.connect()  # Already called in __init__
            await nostr_client.connect_to_primary_relay()
            result = await nostr_client.send_dm("Test message from HA Nostr Alert")
            await nostr_client.disconnect_all()
            print(f"Test result: {result}")
        except Exception as e:
            logger.error(f"Error in Nostr client test: {e}")
    
    # Run the async function
    asyncio.run(test_client())
