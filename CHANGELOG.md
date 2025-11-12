# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
