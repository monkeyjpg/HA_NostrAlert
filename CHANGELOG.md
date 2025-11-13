# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
