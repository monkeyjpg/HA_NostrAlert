"""
Webhook server for receiving Home Assistant state changes
"""
from flask import Flask, request, jsonify
import logging
import threading
import queue

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebhookServer:
    def __init__(self, config, message_queue):
        self.app = Flask(__name__)
        self.config = config
        self.message_queue = message_queue
        self.setup_routes()
    
    def setup_routes(self):
        """Set up Flask routes"""
        self.app.add_url_rule('/webhook', 'webhook', self.handle_webhook, methods=['POST'])
        self.app.add_url_rule('/health', 'health', self.health_check, methods=['GET'])
    
    def handle_webhook(self):
        """Handle incoming webhook from Home Assistant"""
        try:
            data = request.get_json()
            logger.info(f"Received webhook data: {data}")
            
            # Check if this is a monitored entity
            entity_id = data.get('entity_id')
            if entity_id in self.config.monitored_entities:
                logger.info(f"Monitored entity {entity_id} changed")
                
                # Add to message queue for processing
                if self.message_queue.qsize() < self.config.max_queue_size:
                    self.message_queue.put(data)
                    logger.info(f"Added to queue. Queue size: {self.message_queue.qsize()}")
                else:
                    logger.warning(f"Queue full, dropping message for {entity_id}")
            
            return jsonify({"status": "success"}), 200
        except Exception as e:
            logger.error(f"Error handling webhook: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500
    
    def health_check(self):
        """Health check endpoint"""
        return jsonify({
            "status": "healthy",
            "queue_size": self.message_queue.qsize(),
            "max_queue_size": self.config.max_queue_size
        }), 200
    
    def run(self, host='0.0.0.0', port=5000):
        """Run the webhook server"""
        logger.info(f"Starting webhook server on {host}:{port}")
        self.app.run(host=host, port=port, debug=False)

# Example of how to use the webhook server
if __name__ == "__main__":
    # This is just for testing the webhook server independently
    from config import Config
    config = Config()
    message_queue = queue.Queue(maxsize=5)
    server = WebhookServer(config, message_queue)
    server.run()
