# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.8] - 2025-11-12

### Fixed

- Simplified run.sh to work properly with s6-overlay environment
- Removed excessive debugging output that may interfere with s6-overlay
- Updated version to 0.1.8 to force cache refresh

## [0.1.7] - 2025-11-12

### Fixed

- Fixed build.json to use correct Home Assistant base images
- Updated Dockerfile to have proper default value for BUILD_FROM argument
- Updated version to 0.1.7 to force cache refresh

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
