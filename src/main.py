#!/usr/bin/env python3
"""
Main entry point for HA Nostr Alert
"""
import sys
import os
import threading
import queue
import time
import logging
import asyncio
import signal

# Add debug logging at the very beginning
print("=== main.py starting ===", file=sys.stderr)
print(f"Python version: {sys.version}", file=sys.stderr)
print(f"Current working directory: {os.getcwd()}", file=sys.stderr)
print(f"Python path: {sys.path}", file=sys.stderr)

# Try to import modules and catch any import errors
try:
    from config import Config  # noqa: E402
    from exceptions import HA_Nostr_Alert_Error, ConfigurationError, RelayConnectionError, MessageProcessingError
    print("=== Successfully imported config ===", file=sys.stderr)
except Exception as e:
    print(f"=== Failed to import config: {e} ===", file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)

try:
    from webhook_server import WebhookServer
    print("=== Successfully imported webhook_server ===", file=sys.stderr)
except Exception as e:
    print(f"=== Failed to import webhook_server: {e} ===", file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)

try:
    from nostr_client import NostrClient
    print("=== Successfully imported nostr_client ===", file=sys.stderr)
except Exception as e:
    print(f"=== Failed to import nostr_client: {e} ===", file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)

try:
    from message_processor import MessageProcessor
    print("=== Successfully imported message_processor ===", file=sys.stderr)
except Exception as e:
    print(f"=== Failed to import message_processor: {e} ===", file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.info("Starting HA Nostr Alert service")

# Global variables for cleanup
message_processor = None
nostr_client = None
loop = None

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    logger.info(f"Received signal {signum}, shutting down gracefully...")
    if message_processor:
        message_processor.stop()
    if nostr_client and loop:
        try:
            # Cancel any pending tasks
            pending = asyncio.all_tasks(loop)
            for task in pending:
                task.cancel()
            
            # Create a new async function to handle the cleanup
            async def cleanup():
                await nostr_client.stop_health_monitoring()
                await nostr_client.disconnect_all()
            
            loop.run_until_complete(cleanup())
            loop.run_until_complete(loop.shutdown_asyncgens())
        except Exception as e:
            logger.error(f"Error disconnecting from Nostr: {e}")
        finally:
            loop.close()
    sys.exit(0)

def main():
    """Main function to start the HA Nostr Alert service"""
    logger.info("Starting HA Nostr Alert service main function")
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    global message_processor, nostr_client, loop
    
    # Load configuration
    try:
        logger.info("Loading configuration...")
        config = Config()
        logger.info("Configuration loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        return
    
    # Create message queue
    message_queue = queue.Queue(maxsize=config.max_queue_size)
    
    # Create event loop for main thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Initialize Nostr client
    try:
        logger.info("Initializing Nostr client...")
        nostr_client = NostrClient(config)
        # Connect to primary relay
        logger.info("Connecting to Nostr relay...")
        loop.run_until_complete(nostr_client.connect_to_primary_relay())
        # Start health monitoring
        loop.run_until_complete(nostr_client.start_health_monitoring())
        logger.info("Nostr client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Nostr client: {e}")
        return
    
    # Initialize message processor
    try:
        logger.info("Initializing message processor...")
        message_processor = MessageProcessor(config, message_queue, nostr_client)
        logger.info("Message processor initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize message processor: {e}")
        return
    
    # Initialize webhook server
    try:
        logger.info("Initializing webhook server...")
        webhook_server = WebhookServer(config, message_queue)
        logger.info("Webhook server initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize webhook server: {e}")
        return
    
    # Start components
    try:
        # Start message processor
        logger.info("Starting message processor...")
        message_processor.start()
        
        # Start webhook server in a separate thread
        logger.info("Starting webhook server...")
        server_thread = threading.Thread(
            target=webhook_server.run,
            kwargs={'host': '0.0.0.0', 'port': 5000}
        )
        server_thread.daemon = True
        server_thread.start()
        
        logger.info("HA Nostr Alert service started successfully")
        
        # Keep the main thread alive
        while True:
            time.sleep(1)
            
    except Exception as e:
        logger.error(f"Error in main loop: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
    finally:
        # Clean up
        if message_processor:
            message_processor.stop()
        if nostr_client and loop:
            try:
                loop.run_until_complete(nostr_client.stop_health_monitoring())
                loop.run_until_complete(nostr_client.disconnect_all())
            except Exception as e:
                logger.error(f"Error disconnecting from Nostr: {e}")
        logger.info("HA Nostr Alert service stopped")

if __name__ == "__main__":
    print("=== About to call main() ===", file=sys.stderr)
    main()
