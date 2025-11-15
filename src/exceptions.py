"""
Custom exceptions for HA Nostr Alert
"""
class HA_Nostr_Alert_Error(Exception):
    """Base exception for HA Nostr Alert"""
    pass

class ConfigurationError(HA_Nostr_Alert_Error):
    """Raised when configuration is invalid"""
    pass

class RelayConnectionError(HA_Nostr_Alert_Error):
    """Raised when relay connection fails"""
    pass

class MessageProcessingError(HA_Nostr_Alert_Error):
    """Raised when message processing fails"""
    pass

class ValidationError(HA_Nostr_Alert_Error):
    """Raised when validation fails"""
    pass
