# GO1 Web Controller

> A web-based control system for the Unitree GO1 quadruped robot. Control your robot dog from any browser!

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Flask Version](https://img.shields.io/badge/Flask-2.0%2B-green.svg)](https://flask.palletsprojects.com)

---

## 🎯 Project Overview

GO1 Web Controller is an open-source web-based control system for the Unitree GO1 quadruped robot. This project provides a simple, intuitive interface to control the GO1 robot using a web browser, with support for both keyboard and button controls.

**No ROS required!** This is a lightweight, standalone solution that uses the official Unitree SDK for direct UDP communication with the robot.

---

## ✨ Features

- **Web-Based Interface**: Control your GO1 from any modern web browser
- **Multiple Control Modes**: 
  - Button controls for touch devices
  - Keyboard controls (WASD + Space)
- **SAFE MODE**: Test commands without connecting to the real robot
- **Real-time Status**: Monitor robot state and battery level
- **UDP Communication**: Direct communication with the GO1 using Unitree SDK
- **Beginner-Friendly**: Simple setup and clear documentation
- **Cross-Platform**: Works on Linux, macOS, and Windows

---

## 🎮 Demo

### Video Demo
[![GO1 Web Controller Demo](https://img.youtube.com/vi/VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=VIDEO_ID)

### Screenshots

| Web Interface | Robot in Action |
|--------------|-----------------|
| ![Web Interface](docs/screenshots/web_interface.png) | ![Robot in Action](docs/screenshots/robot_action.png) |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Web Browser (Frontend)                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  HTML/CSS/JS Interface                                │   │
│  │  - Direction buttons (Forward/Backward/Left/Right)    │   │
│  │  - Keyboard listener (W/A/S/D + Space)                │   │
│  │  - Status display (connection, battery, command)      │   │
│  └─────────────────┬─────────────────────────────────────┘   │
│                    │ HTTP POST Requests                        │
│                    ▼                                          │
├─────────────────────────────────────────────────────────────────┤
│                    Flask Server (Backend)                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  REST API Endpoints                                    │   │
│  │  - /forward, /backward, /left, /right, /stop, /status │   │
│  └─────────────────┬─────────────────────────────────────┘   │
│                    │ Python Function Calls                     │
│                    ▼                                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  GO1 Controller                                        │   │
│  │  - HIGHLEVEL UDP communication                         │   │
│  │  - 500Hz control loop                                  │   │
│  │  - Command generation                                  │   │
│  └─────────────────┬─────────────────────────────────────┘   │
│                    │ UDP Packets (192.168.123.161:8082)       │
│                    ▼                                          │
├─────────────────────────────────────────────────────────────────┤
│                      Unitree GO1 Robot                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  SPORT Mode Controller                                 │   │
│  │  - High-level walking commands                         │   │
│  │  - Trot gait control                                   │   │
│  │  - Real-time state feedback                            │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 Installation

### Prerequisites

- Ubuntu 22.04 (Recommended)
- Python 3.8+
- Unitree GO1 robot with Ethernet connection
- Unitree Legged SDK (included in this repo)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/go1-web-controller.git
cd go1-web-controller
```

### Step 2: Set Up Python Environment

```bash
# Create a virtual environment
conda create -n go1_web python=3.8
conda activate go1_web

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Network Configuration

1. Connect your computer to the GO1 via Ethernet
2. Set your Ethernet IP to `192.168.123.2/24`

```bash
# Example for Ubuntu
sudo ip addr add 192.168.123.2/24 dev enp0s3
sudo ip link set enp0s3 up
```

3. Verify connection to the robot

```bash
ping 192.168.123.161
```

---

## 🚀 Running the Application

### Step 1: Start the Backend

```bash
cd go1-web-controller
./start_backend.sh
```

### Step 2: Start the Frontend

```bash
cd go1-web-controller
./start_frontend.sh
```

### Step 3: Open the Web Interface

Open your browser and go to:
```
http://localhost:8080
```

### Step 4: Control the Robot

**Button Controls:**
- ▲ **Forward**
- ▼ **Backward**
- ◀ **Turn Left**
- ▶ **Turn Right**
- ⏹️ **Stop**

**Keyboard Controls:**
- **W** - Forward
- **S** - Backward
- **A** - Turn Left
- **D** - Turn Right
- **Space** - Stop

---

## ⚠️ Safety Warnings

**IMPORTANT: READ THESE BEFORE OPERATING THE ROBOT**

1. **Start in SAFE MODE**: Always test in SAFE MODE first to verify commands work
2. **Clear Space**: Ensure the robot has at least 2 meters of clear space in all directions
3. **Battery Check**: Verify the robot has sufficient battery before operation
4. **Emergency Stop**: Know how to quickly stop the robot (Space key or Stop button)
5. **Start Slow**: Begin with low speeds and gradually increase
6. **Supervision**: Always have someone nearby who can manually stop the robot if needed

### SAFE MODE

To enable/disable real robot control, edit `backend/go1_controller.py`:

```python
# Set to True only when robot is connected and ready!
REAL_ROBOT = False  # Safe Mode (default)
# REAL_ROBOT = True  # Real Robot Mode
```

---

## 📁 Project Structure

```
go1-web-controller/
├── backend/                  # Flask backend
│   ├── app.py                # Flask web server with API endpoints
│   └── go1_controller.py     # GO1 control logic and UDP communication
├── frontend/                 # Web frontend
│   ├── index.html            # Main HTML interface
│   ├── style.css             # Modern dark theme styling
│   └── script.js             # Interactive logic and API calls
├── sdk/                      # Unitree Legged SDK
│   └── unitree_legged_sdk/   # Official Unitree SDK files
├── docs/                     # Documentation
│   └── screenshots/          # Project screenshots
├── start_backend.sh          # Backend startup script
├── start_frontend.sh         # Frontend startup script
├── requirements.txt          # Python dependencies
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

---

## 🛣️ Future Roadmap

- [ ] Add speed control slider
- [ ] Add gait selection (trot, walk, run)
- [ ] Add body height adjustment
- [ ] Add real-time video feed from robot
- [ ] Add joystick support
- [ ] Add mobile app compatibility
- [ ] Add autonomous navigation mode
- [ ] Add obstacle avoidance
- [ ] Add ROS integration (optional)
- [ ] Add voice control

---

## 🤝 Contributing

Contributions are welcome! Please feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Unitree Robotics** for providing the official SDK
- **Flask** for the lightweight web framework
- **All contributors** to this project

---

## 📞 Contact

For questions or support, please open an issue on GitHub or contact the maintainer.

---

*Built with ❤️ for the robotics community*
