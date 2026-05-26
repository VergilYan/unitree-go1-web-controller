# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Initial release of GO1 Web Controller
- Web-based control interface
- Flask backend with REST API
- HTML/CSS/JS frontend
- Keyboard controls (WASD + Space)
- Button controls for touch devices
- SAFE MODE for testing without real robot
- Unitree SDK integration
- UDP communication with GO1 robot
- Real-time status display
- Battery level monitoring
- Professional README documentation
- License file
- Contributing guide
- Usage documentation

### Changed
- Fixed left/right turn direction issue
- Disabled Flask debug mode to prevent port conflicts
- Updated speed limits for safe operation
- Improved error handling

### Security
- Added safety warnings in documentation
- Implemented SAFE MODE to prevent accidental robot movement

## [v1.0.0] - 2024-XX-XX

### Added
- First stable release
- All basic movement commands (forward, backward, left, right, stop)
- Web interface with modern design
- Cross-origin support for frontend
- Auto-detection of SDK path
- 500Hz control loop for real-time command sending
