"""
Webhook server for receiving Home Assistant state changes
"""
from flask import Flask, request, jsonify
import logging
import threading
import queue
from typing import Any, Dict, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebhookServer:
    def __init__(self, config: Any, message_queue: queue.Queue):
        self.app: Flask = Flask(__name__)
        self.config = config
        self.message_queue = message_queue
        self.setup_routes()
    
    def setup_routes(self) -> None:
        """Set up Flask routes"""
        self.app.add_url_rule('/webhook', 'webhook', self.handle_webhook, methods=['POST'])
        self.app.add_url_rule('/health', 'health', self.health_check, methods=['GET'])
    
    def handle_webhook(self):
        """Handle incoming webhook from Home Assistant"""
        try:
            data: Optional[Dict[str, Any]] = request.get_json()
            
            # Validate data structure with detailed error messages
            if not isinstance(data, dict):
                logger.warning("Invalid webhook data format - expected JSON object")
                return jsonify({
                    "status": "error", 
                    "message": "Invalid data format - expected JSON object",
                    "received_type": str(type(data)) if data is not None else "None"
                }), 400
            
            entity_id: Optional[str] = data.get('entity_id')
            new_state: Optional[Dict[str, Any]] = data.get('new_state')
            
            if not entity_id or new_state is None:
                logger.warning("Missing required fields in webhook data")
                return jsonify({
                    "status": "error", 
                    "message": "Missing required fields",
                    "missing_fields": {
                        "entity_id": "missing" if not entity_id else "present",
                        "new_state": "missing" if new_state is None else "present"
                    }
                }), 400
            
            logger.info(f"Received webhook data for {entity_id}")
            
            # Check if this is a monitored entity
            if entity_id in self.config.monitored_entities:
                logger.info(f"Monitored entity {entity_id} changed to {new_state.get('state', 'N/A')}")
                
                # Add to message queue for processing
                if self.message_queue.qsize() < self.config.max_queue_size:
                    self.message_queue.put(data)
                    logger.info(f"Added to queue. Queue size: {self.message_queue.qsize()}")
                else:
                    logger.warning(f"Queue full, dropping message for {entity_id}")
                    return jsonify({
                        "status": "warning",
                        "message": "Queue full, message dropped",
                        "queue_size": self.message_queue.qsize(),
                        "max_queue_size": self.config.max_queue_size
                    }), 503
            
            return jsonify({"status": "success"}), 200
        except Exception as e:
            logger.error(f"Error handling webhook: {e}")
            return jsonify({
                "status": "error", 
                "message": str(e),
                "type": type(e).__name__
            }), 500
    
    def health_check(self):
        """Health check endpoint"""
        return jsonify({
            "status": "healthy",
            "queue_size": self.message_queue.qsize(),
            "max_queue_size": self.config.max_queue_size
        }), 200
    
    def run(self, host: str = '0.0.0.0', port: int = 5000) -> None:
        """Run the webhook server"""
        logger.info(f"Starting webhook server on {host}:{port}")
        self.app.run(host=host, port=port, debug=False)

# Example of how to use the webhook server
if __name__ == "__main__":
    # This is just for testing the webhook server independently
    from config import Config
    config = Config()
    message_queue: queue.Queue = queue.Queue(maxsize=5)
    server = WebhookServer(config, message_queue)
    server.run()
