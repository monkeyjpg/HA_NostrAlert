"""
Configuration management for HA Nostr Alert
"""
import yaml
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Config:
    def __init__(self, config_path='config.yaml'):
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from YAML file"""
        if not os.path.exists(self.config_path):
            # Create default configuration
            default_config = {
                'nostr': {
                    'relay_url': 'ws://localhost:6969',
                    'recipient_npub': '',
                    'private_key': ''
                },
                'alerts': {
                    'monitored_entities': [
                        'input_number.logic_pwrlimit',
                        'input_text.logic_m1_switch'
                    ],
                    'consolidated_entities': [
                        'input_number.logic_pwrlimit',
                        'input_text.logic_m1_switch',
                        'input_text.logic_m1_logstring'
                    ]
                },
                'queue': {
                    'max_size': 5
                }
            }
            self.save_config(default_config)
            return default_config
        
        with open(self.config_path, 'r') as file:
            config = yaml.safe_load(file)
            # Validate configuration
            self.validate_config(config)
            return config
    
    def validate_config(self, config):
        """Validate configuration parameters"""
        # Check nostr section
        if 'nostr' not in config:
            raise ValueError("Missing 'nostr' section in configuration")
        
        if 'relay_url' not in config['nostr']:
            raise ValueError("Missing 'relay_url' in nostr configuration")
        
        if 'recipient_npub' not in config['nostr']:
            raise ValueError("Missing 'recipient_npub' in nostr configuration")
        
        if 'private_key' not in config['nostr']:
            raise ValueError("Missing 'private_key' in nostr configuration")
        
        # Validate npub format (basic check)
        if config['nostr']['recipient_npub'] and not config['nostr']['recipient_npub'].startswith('npub1'):
            logger.warning("Recipient npub may not be in correct format")
        
        # Validate nsec format (basic check)
        if config['nostr']['private_key'] and not config['nostr']['private_key'].startswith('nsec1'):
            logger.warning("Private key may not be in correct format")
        
        # Check alerts section
        if 'alerts' not in config:
            raise ValueError("Missing 'alerts' section in configuration")
        
        if 'monitored_entities' not in config['alerts']:
            raise ValueError("Missing 'monitored_entities' in alerts configuration")
        
        if 'consolidated_entities' not in config['alerts']:
            raise ValueError("Missing 'consolidated_entities' in alerts configuration")
        
        # Check queue section
        if 'queue' not in config:
            raise ValueError("Missing 'queue' section in configuration")
        
        if 'max_size' not in config['queue']:
            raise ValueError("Missing 'max_size' in queue configuration")
        
        logger.info("Configuration validation completed")
    
    def save_config(self, config):
        """Save configuration to YAML file"""
        with open(self.config_path, 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
    
    @property
    def relay_url(self):
        return self.config['nostr']['relay_url']
    
    @property
    def recipient_npub(self):
        return self.config['nostr']['recipient_npub']
    
    @property
    def private_key(self):
        return self.config['nostr']['private_key']
    
    @property
    def monitored_entities(self):
        return self.config['alerts']['monitored_entities']
    
    @property
    def consolidated_entities(self):
        return self.config['alerts']['consolidated_entities']
    
    @property
    def max_queue_size(self):
        return self.config['queue']['max_size']
