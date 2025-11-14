"""
Configuration management for HA Nostr Alert
"""
import yaml
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Config:
    def __init__(self, config_path='/config.yaml'):
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from Home Assistant add-on options or YAML file"""
        # First check if we're in Home Assistant add-on environment
        if os.path.exists('/data/options.json'):
            logger.info("Loading configuration from Home Assistant add-on options")
            return self.load_ha_config()
        else:
            logger.info("Loading configuration from YAML file")
            return self.load_yaml_config()
    
    def load_ha_config(self):
        """Load configuration from Home Assistant add-on options"""
        with open('/data/options.json', 'r') as file:
            options = json.load(file)
        
        # Handle backward compatibility for single relay_url
        relay_urls = options.get('relay_urls')
        if not relay_urls:
            # Fallback to single relay_url for backward compatibility
            single_relay = options.get('relay_url', 'wss://relay.damus.io')
            relay_urls = [single_relay] if isinstance(single_relay, str) else single_relay
        
        # Map Home Assistant options to our internal config structure
        config = {
            'nostr': {
                'relay_urls': relay_urls,
                'recipient_npub': options.get('recipient_npub', ''),
                'private_key': options.get('private_key', '')
            },
            'alerts': {
                'monitored_entities': options.get('monitored_entities', []),
                'consolidated_entities': options.get('consolidated_entities', [])
            },
            'queue': {
                'max_size': 5  # Default value
            },
            'relay_health': {
                'check_interval': 300,  # 5 minutes default
                'retry_attempts': 3,
                'retry_backoff_factor': 2
            }
        }
        
        # Validate configuration
        self.validate_config(config)
        return config
    
    def load_yaml_config(self):
        """Load configuration from YAML file"""
        if not os.path.exists(self.config_path):
            # Create default configuration with multiple relays
            default_config = {
                'nostr': {
                    'relay_urls': [
                        'wss://relay.0xchat.com',
                        'wss://relay.damus.io',
                        'wss://relay.primal.net',
                        'wss://relay.nostr.band'
                    ],
                    'recipient_npub': '',
                    'private_key': ''
                },
                'alerts': {
                    'monitored_entities': [
                        'input_number.entity1',
                        'input_text.entity2'
                    ],
                    'consolidated_entities': [
                        'input_number.entity1',
                        'input_text.entity2',
                        'input_text.entity3'
                    ]
                },
                'queue': {
                    'max_size': 5
                },
                'relay_health': {
                    'check_interval': 300,  # 5 minutes
                    'retry_attempts': 3,
                    'retry_backoff_factor': 2
                }
            }
            self.save_config(default_config)
            return default_config
        
        with open(self.config_path, 'r') as file:
            config = yaml.safe_load(file)
            # Handle backward compatibility for single relay_url
            if 'nostr' in config and 'relay_url' in config['nostr'] and 'relay_urls' not in config['nostr']:
                config['nostr']['relay_urls'] = [config['nostr']['relay_url']]
                # Remove the old single relay_url field
                del config['nostr']['relay_url']
            
            # Add default relay_health config if missing
            if 'relay_health' not in config:
                config['relay_health'] = {
                    'check_interval': 300,  # 5 minutes
                    'retry_attempts': 3,
                    'retry_backoff_factor': 2
                }
            
            # Validate configuration
            self.validate_config(config)
            return config
    
    def validate_config(self, config):
        """Validate configuration parameters"""
        # Check nostr section
        if 'nostr' not in config:
            raise ValueError("Missing 'nostr' section in configuration")
        
        nostr_section = config['nostr']
        # Updated to check for relay_urls instead of relay_url
        required_nostr_fields = ['relay_urls', 'recipient_npub', 'private_key']
        for field in required_nostr_fields:
            if field not in nostr_section:
                raise ValueError(f"Missing '{field}' in nostr configuration")
        
        # Validate relay_urls is a list
        if not isinstance(nostr_section['relay_urls'], list) or len(nostr_section['relay_urls']) == 0:
            raise ValueError("'relay_urls' must be a non-empty list")
        
        # Validate each relay URL format (basic check)
        for relay_url in nostr_section['relay_urls']:
            if not isinstance(relay_url, str) or not relay_url.startswith('wss://'):
                logger.warning(f"Relay URL may not be in correct format: {relay_url}")
        
        # Validate npub format (basic check)
        if nostr_section['recipient_npub'] and not nostr_section['recipient_npub'].startswith('npub1'):
            logger.warning("Recipient npub may not be in correct format")
        
        # Validate nsec format (basic check)
        if nostr_section['private_key'] and not nostr_section['private_key'].startswith(('nsec1', 'ncryptsec1')):
            logger.warning("Private key may not be in correct format")
        
        # Check alerts section
        if 'alerts' not in config:
            raise ValueError("Missing 'alerts' section in configuration")
        
        alerts_section = config['alerts']
        required_alerts_fields = ['monitored_entities', 'consolidated_entities']
        for field in required_alerts_fields:
            if field not in alerts_section:
                raise ValueError(f"Missing '{field}' in alerts configuration")
            
            # Ensure fields are lists
            if not isinstance(alerts_section[field], list):
                raise ValueError(f"'{field}' must be a list")
        
        # Check queue section
        if 'queue' not in config:
            raise ValueError("Missing 'queue' section in configuration")
        
        queue_section = config['queue']
        if 'max_size' not in queue_section:
            raise ValueError("Missing 'max_size' in queue configuration")
        
        # Ensure max_size is a positive integer
        if not isinstance(queue_section['max_size'], int) or queue_section['max_size'] <= 0:
            raise ValueError("'max_size' must be a positive integer")
        
        # Check relay_health section
        if 'relay_health' not in config:
            raise ValueError("Missing 'relay_health' section in configuration")
        
        relay_health_section = config['relay_health']
        required_relay_health_fields = ['check_interval', 'retry_attempts', 'retry_backoff_factor']
        for field in required_relay_health_fields:
            if field not in relay_health_section:
                raise ValueError(f"Missing '{field}' in relay_health configuration")
        
        logger.info("Configuration validation completed")
    
    def save_config(self, config):
        """Save configuration to YAML file"""
        with open(self.config_path, 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
    
    @property
    def relay_urls(self):
        return self.config['nostr']['relay_urls']
    
    @property
    def relay_url(self):
        # Backward compatibility - return the first relay URL
        return self.config['nostr']['relay_urls'][0] if self.config['nostr']['relay_urls'] else None
    
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
    
    @property
    def relay_health_config(self):
        return self.config.get('relay_health', {
            'check_interval': 300,
            'retry_attempts': 3,
            'retry_backoff_factor': 2
        })
