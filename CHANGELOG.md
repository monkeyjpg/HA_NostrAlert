# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.26] - 2025-11-15

### Fixed

- Resolved ModuleNotFoundError in Home Assistant add-on environment by correcting import statements
- Changed absolute package imports to direct module imports to match container file structure
- Fixed import paths in config.py, main.py, message_processor.py, and nostr_client.py
- This resolves the issue where the add-on was failing to start with "No module named 'src'" error

## [0.1.25] - 2025-11-15

### Added

- Timestamp formatting for DM messages (YYYY-MM-DD HH:MM:SS) for better temporal context
- Friendly name support in DM messages for improved readability
- Enhanced signal handling with proper task cancellation and event loop cleanup
- Improved thread safety in message processor with better queue handling

### Changed

- Enhanced resource management with proper cleanup of asyncio tasks and clients
- Improved error messages in webhook server with detailed diagnostic information
- Enhanced configuration validation using urllib for more robust URL parsing
- Better queue full handling with appropriate HTTP status codes (503 Service Unavailable)

### Fixed

- Race conditions in message processor through improved thread synchronization
- Resource leaks through proper cleanup of asyncio tasks and client connections
- Incomplete shutdown procedures with enhanced signal handling

## [0.1.24] - 2025-11-15

### Added

- Comprehensive type hints throughout the codebase for better code clarity and IDE support
- Custom exception classes for more granular error handling (ConfigurationError, ValidationError, RelayConnectionError, MessageProcessingError)
- Enhanced relay URL validation with stricter format checking
- Thread synchronization in message processor for improved thread safety

### Changed

- Improved configuration validation with more robust URL format checking
- Updated import statements to use absolute imports for better module organization
- Enhanced error handling with custom exception types
- Added type annotations to all function signatures and variable declarations

## [0.1.23] - 2025-11-15

### Fixed

- Enhanced relay connection verification to detect and recover from disconnections
- Improved failover mechanism with better error handling and reporting
- Added proactive connection checking before message sending
- Fixed false success reporting when messages fail to send
- Enhanced error propagation from Nostr client to message processor

## [0.1.22] - 2025-11-14

### Added

- Multi-relay support with priority-based failover for improved reliability
- Background health monitoring with periodic relay connection checks
- Automatic reconnection attempts with configurable retry logic
- Support for configuring multiple Nostr relays in order of preference
- Enhanced relay status tracking and failure count monitoring

### Changed

- Updated configuration structure to support `relay_urls` array instead of single `relay_url`
- Modified NostrClient to manage multiple concurrent relay connections
- Enhanced error handling and logging for relay management
- Updated main application to integrate relay health monitoring

### Fixed

- Relay disconnection issues that caused message delivery failures
- Improved resilience when individual relays become unavailable
- Enhanced failover mechanism for seamless relay switching

## [0.1.21] - 2025-11-13

### Fixed

- Added `init: false` to config.yaml to properly integrate with Home Assistant's s6-overlay system
- Ensured proper s6-overlay service structure in rootfs/etc/services.d/ha-nostr-alert/
- Confirmed correct shebang `#!/usr/bin/with-contenv bashio` in run script
- Verified finish script for proper service termination handling
- Updated to version 0.1.21 for proper s6-overlay integration

## [0.1.20] - 2025-11-13

### Fixed

- Implemented proper s6-overlay service structure following Home Assistant addon best practices
- Created rootfs/etc/services.d/ha-nostr-alert with run and finish scripts
- Using correct shebang `#!/usr/bin/with-contenv bashio` for s6-overlay integration
- Removed direct execution approach that was causing s6-overlay-suexec errors
- Updated Dockerfile to use rootfs approach instead of CMD
- Updated to version 0.1.20 to force cache refresh with proper s6-overlay structure

## [0.1.19] - 2025-11-13

### Fixed

- Fixed Dockerfile to remove reference to deleted rootfs directory
- Removed `COPY rootfs/ /` line that was causing build failures
- Updated to version 0.1.19 to force cache refresh with fixed Dockerfile

## [0.1.18] - 2025-11-13

### Fixed

- Created clean deployment package without archive directory that contained old problematic files
- Removed all archived files from deployment package that may have contained conflicting scripts
- Updated to version 0.1.18 to force cache refresh with clean package

## [0.1.17] - 2025-11-13

### Fixed

- Completely removed s6-overlay initialization script that was causing suexec errors
- Removed rootfs/etc/cont-init.d/10-ha-nostr-alert.sh entirely
- Removed unnecessary directory creation that may have interfered with s6-overlay
- Updated version to 0.1.17 to force cache refresh

## [0.1.16] - 2025-11-13

### Fixed

- Fixed s6-overlay-suexec error by correcting shebang in initialization script
- Changed `#!/command/with-contenv bashio` to `#!/bin/bash` in 10-ha-nostr-alert.sh
- Updated version to 0.1.16 to force cache refresh

## [0.1.15] - 2025-11-12

### Fixed

- Reverted to direct execution approach that was working in version 0.1.3
- Simplified run.sh to directly execute Python application
- Removed complex s6-overlay service structure
- Simplified initialization script
- Updated version to 0.1.15 to force cache refresh

## [0.1.14] - 2025-11-12

### Fixed

- Added proper s6-overlay service structure
- Created services.d directory with run and finish scripts
- Simplified run.sh to be a placeholder
- Updated version to 0.1.14 to force cache refresh

## [0.1.6] - 2025-11-12

### Fixed

- Changed shebang back to `#!/usr/bin/with-contenv bashio` to properly integrate with Home Assistant's s6-overlay
- Added build.json file to specify base images for different architectures
- Changed Dockerfile to use ENTRYPOINT instead of CMD
- Updated run.sh to use exec with python3 to properly hand off process control
- Updated version to 0.1.6 to force cache refresh

## [0.1.3] - 2025-11-12

### Fixed

- Add extensive debugging to identify s6-overlay suexec root cause
- Enhanced run.sh with environment debugging
- Enhanced main.py with import and startup debugging
- Updated version to force cache refresh

## [0.1.2] - 2025-11-12

### Fixed

- Simplify run.sh to avoid s6-overlay suexec conflicts
- Use plain bash shebang instead of with-contenv
- Create minimal default config to avoid configuration reading issues
- Updated version to force cache refresh

## [0.1.1] - 2025-11-12

### Fixed

- Attempt to resolve s6-overlay suexec error
- Updated version to force cache refresh

## [0.1.0] - 2025-11-12

### Added

- Initial release of HA Nostr Alert as a Home Assistant add-on
- Nostr NIP-17 encrypted DM support
- Webhook listener for receiving Home Assistant alerts
- Configurable entity monitoring
- Queue management for handling message bursts
- Support for multiple relay connections
- Add-on configuration interface
- Documentation for installation and usage

### Changed

- Modified configuration loading to work with Home Assistant add-on environment
- Updated file paths to work within containerized environment
- Enhanced error handling for add-on environment
- Updated default relay URL to wss://relay.damus.io
- Updated example entity names in documentation and default configuration

### Fixed

- Configuration file path issues for containerized deployment
- Improved logging for better debugging in add-on environment
