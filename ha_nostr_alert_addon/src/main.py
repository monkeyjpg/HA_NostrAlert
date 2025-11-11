"""
Main entry point for HA Nostr Alert
"""
import threading
import queue
import time
import logging
import asyncio
from config import Config
from webhook_server import WebhookServer
from nostr_client import NostrClient
from message_processor import MessageProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main function to start the HA Nostr Alert service"""
    logger.info("Starting HA Nostr Alert service")
    
    # Load configuration
    config = Config()
    
    # Create message queue
    message_queue = queue.Queue(maxsize=config.max_queue_size)
    
    # Create event loop for main thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Initialize Nostr client
    try:
        nostr_client = NostrClient(config)
        # Connect to relay
        loop.run_until_complete(nostr_client.connect_relay())
    except Exception as e:
        logger.error(f"Failed to initialize Nostr client: {e}")
        return
    
    # Initialize message processor
    message_processor = MessageProcessor(config, message_queue, nostr_client)
    
    # Initialize webhook server
    webhook_server = WebhookServer(config, message_queue)
    
    # Start components
    try:
        # Start message processor
        message_processor.start()
        
        # Start webhook server in a separate thread
        server_thread = threading.Thread(
            target=webhook_server.run,
            kwargs={'host': '0.0.0.0', 'port': 5000}
        )
        server_thread.daemon = True
        server_thread.start()
        
        logger.info("HA Nostr Alert service started successfully")
        logger.info("Press Ctrl+C to stop the service")
        
        # Keep the main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Shutting down HA Nostr Alert service")
    except Exception as e:
        logger.error(f"Error in main loop: {e}")
    finally:
        # Clean up
        message_processor.stop()
        loop.run_until_complete(nostr_client.disconnect())
        logger.info("HA Nostr Alert service stopped")

if __name__ == "__main__":
    main()
