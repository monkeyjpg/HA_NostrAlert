"""
Message processor for handling queued messages and sending consolidated alerts
"""
import logging
import threading
import time
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MessageProcessor:
    def __init__(self, config, message_queue, nostr_client):
        self.config = config
        self.message_queue = message_queue
        self.nostr_client = nostr_client
        self.running = False
        self.entity_states = {}
        self.processed_messages = set()
        
    def start(self):
        """Start the message processor"""
        self.running = True
        self.processor_thread = threading.Thread(target=self._process_messages)
        self.processor_thread.start()
        logger.info("Message processor started")
    
    def stop(self):
        """Stop the message processor"""
        self.running = False
        if hasattr(self, 'processor_thread'):
            self.processor_thread.join()
        logger.info("Message processor stopped")
    
    def _process_messages(self):
        """Process messages from the queue"""
        while self.running:
            try:
                # Process all available messages in the queue
                processed_entities = set()
                
                while not self.message_queue.empty() and self.running:
                    data = self.message_queue.get_nowait()
                    entity_id = data.get('entity_id')
                    
                    # Store the latest state for each entity
                    self.entity_states[entity_id] = data
                    processed_entities.add(entity_id)
                    logger.info(f"Processed entity update: {entity_id}")
                
                # If we have updates to monitored entities, send consolidated message
                if processed_entities and any(entity in self.config.monitored_entities 
                                            for entity in processed_entities):
                    self._send_consolidated_alert()
                
                # Wait a bit before checking the queue again
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error processing messages: {e}")
                time.sleep(5)  # Wait longer on error
    
    def _send_consolidated_alert(self):
        """Send consolidated alert with all relevant entity states"""
        try:
            # Gather information from consolidated entities
            message_parts = []
            
            for entity_id in self.config.consolidated_entities:
                if entity_id in self.entity_states:
                    state_data = self.entity_states[entity_id]
                    state_value = state_data.get('new_state', {}).get('state', 'N/A')
                    message_parts.append(f"{entity_id}: {state_value}")
            
            # Create consolidated message
            consolidated_message = "\n".join(message_parts)
            
            # Send via Nostr
            self.nostr_client.send_dm(consolidated_message)
            logger.info(f"Sent consolidated alert: {consolidated_message}")
            
        except Exception as e:
            logger.error(f"Error sending consolidated alert: {e}")
