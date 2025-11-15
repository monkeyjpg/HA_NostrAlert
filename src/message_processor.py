"""
Message processor for handling queued messages and sending consolidated alerts
"""
import logging
import threading
import time
import asyncio
import queue
from collections import defaultdict
from typing import Any, Dict, Set, Optional
from src.exceptions import MessageProcessingError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MessageProcessor:
    def __init__(self, config: Any, message_queue: queue.Queue, nostr_client: Any):
        self.config = config
        self.message_queue = message_queue
        self.nostr_client = nostr_client
        self.running = False
        self.entity_states: Dict[str, Any] = {}
        self.processed_messages: Set[str] = set()
        self._lock = threading.Lock()
        
    def start(self) -> None:
        """Start the message processor"""
        self.running = True
        self.processor_thread = threading.Thread(target=self._process_messages)
        self.processor_thread.start()
        logger.info("Message processor started")
    
    def stop(self) -> None:
        """Stop the message processor"""
        self.running = False
        if hasattr(self, 'processor_thread'):
            self.processor_thread.join()
        logger.info("Message processor stopped")
    
    def _process_messages(self) -> None:
        """Process messages from the queue"""
        # Create a new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        while self.running:
            try:
                # Process all available messages in the queue
                processed_entities: Set[str] = set()
                
                with self._lock:
                    while not self.message_queue.empty() and self.running:
                        data = self.message_queue.get_nowait()
                        entity_id: str = data.get('entity_id')
                        
                        # Store the latest state for each entity
                        self.entity_states[entity_id] = data
                        processed_entities.add(entity_id)
                        logger.info(f"Processed entity update: {entity_id}")
                
                # If we have updates to monitored entities, send consolidated message
                if processed_entities and any(entity in self.config.monitored_entities 
                                            for entity in processed_entities):
                    # Use the event loop to handle the async operation
                    loop.run_until_complete(self._send_consolidated_alert())
                
                # Wait a bit before checking the queue again
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error processing messages: {e}")
                time.sleep(5)  # Wait longer on error
        
        # Close the event loop when stopping
        loop.close()
    
    async def _send_consolidated_alert(self) -> None:
        """Send consolidated alert with all relevant entity states"""
        try:
            # Gather information from consolidated entities
            message_parts: list = []
            
            for entity_id in self.config.consolidated_entities:
                if entity_id in self.entity_states:
                    state_data: Dict[str, Any] = self.entity_states[entity_id]
                    state_value: str = state_data.get('new_state', {}).get('state', 'N/A')
                    message_parts.append(f"{entity_id}: {state_value}")
            
            # Create consolidated message
            consolidated_message: str = "\n".join(message_parts)
            
            # Send via Nostr (async operation)
            result: Optional[str] = await self.nostr_client.send_dm(consolidated_message)
            if result:
                logger.info(f"Sent consolidated alert: {consolidated_message}")
            else:
                logger.error(f"Failed to send consolidated alert: {consolidated_message}")
            
        except Exception as e:
            logger.error(f"Error sending consolidated alert: {e}")
