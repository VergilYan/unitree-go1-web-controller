# GO1 Web Controller Usage Guide

This guide provides detailed instructions on how to use the GO1 Web Controller.

## 🚀 Quick Start

### Prerequisites

1. **Network Connection**: 
   - Connect your computer to the GO1 via Ethernet
   - Set IP address: `192.168.123.2/24`
   - Robot IP: `192.168.123.161`

2. **Robot Setup**:
   - Turn on the GO1 robot
   - Ensure robot is in SPORT mode (check display)

### Starting the Application

1. **Terminal 1 - Backend**:
   ```bash
   cd go1-web-controller
   ./start_backend.sh
   ```

2. **Terminal 2 - Frontend**:
   ```bash
   cd go1-web-controller
   ./start_frontend.sh
   ```

3. **Open Browser**:
   ```
   http://localhost:8080
   ```

## 🎮 Controls

### Button Controls

| Button | Action |
|--------|--------|
| ▲ Forward | Move forward |
| ▼ Backward | Move backward |
| ◀ Left | Turn left |
| ▶ Right | Turn right |
| ⏹️ Stop | Stop all movement |

### Keyboard Controls

| Key | Action |
|-----|--------|
| W | Forward |
| S | Backward |
| A | Turn left |
| D | Turn right |
| Space | Stop |

## ⚠️ Safety First

### SAFE MODE

SAFE MODE allows you to test the system without connecting to the real robot.

**To enable SAFE MODE:**
1. Edit `backend/go1_controller.py`
2. Set `REAL_ROBOT = False`
3. Restart the backend

**To enable REAL ROBOT MODE:**
1. Edit `backend/go1_controller.py`
2. Set `REAL_ROBOT = True`
3. Restart the backend

### Safety Checklist

✅ Always start in SAFE MODE to verify commands work  
✅ Ensure 2+ meters of clear space around the robot  
✅ Check battery level before operation  
✅ Know how to stop the robot quickly (Space key)  
✅ Start with low speeds  
✅ Have someone nearby to assist if needed

## 🔧 Configuration

### Speed Settings

Edit `backend/go1_controller.py` to adjust speed limits:

```python
MAX_FORWARD_SPEED = 0.5   # m/s
MAX_BACKWARD_SPEED = 0.3  # m/s  
MAX_TURN_SPEED = 1.0      # rad/s
```

### Network Settings

```python
ROBOT_IP = "192.168.123.161"  # GO1 SPORT mode IP
LOCAL_PORT = 8080              # Local UDP port
ROBOT_PORT = 8082              # GO1 port
```

## 📊 Status Information

The web interface displays:

- **Connection Status**: Connected/Disconnected
- **Current Command**: Current movement command
- **Battery Level**: Robot battery percentage
- **Robot Mode**: Current robot mode

## 🐛 Troubleshooting

### Common Issues

**1. Cannot connect to robot**
- Check Ethernet cable connection
- Verify IP address settings
- Ping the robot: `ping 192.168.123.161`

**2. Robot does not move**
- Ensure `REAL_ROBOT = True`
- Check robot is in SPORT mode
- Verify UDP connection in backend logs

**3. Port already in use**
- Kill previous processes: `pkill -f "python.*app.py"`
- Restart backend

**4. Web interface not responding**
- Check frontend server is running
- Verify backend is running on port 5000
- Check browser console for errors

## 📡 API Endpoints

### POST Endpoints

| Endpoint | Description |
|----------|-------------|
| `/forward` | Move forward |
| `/backward` | Move backward |
| `/left` | Turn left |
| `/right` | Turn right |
| `/stop` | Stop movement |

### GET Endpoints

| Endpoint | Description |
|----------|-------------|
| `/status` | Get robot status |

### Example cURL Commands

```bash
# Move forward
curl -X POST http://localhost:5000/forward

# Stop
curl -X POST http://localhost:5000/stop

# Get status
curl http://localhost:5000/status
```

## 📝 Log Files

Backend logs are displayed in the terminal where you started the backend. Key log messages:

- `✅ Successfully imported Unitree SDK` - SDK loaded correctly
- `✅ UDP connection established successfully!` - Connected to robot
- `📊 State: mode=1, battery=77%` - Robot state received
- `📤 Setting walk command: vx=0.5` - Command sent to robot

## 🎯 Tips for Beginners

1. **Start slow**: Begin with SAFE MODE to understand the system
2. **Test incrementally**: Test each movement direction individually
3. **Read the logs**: Check backend logs to understand what's happening
4. **Ask for help**: Don't hesitate to open an issue if you need help

## 📞 Support

For questions or issues:
- Check the README.md
- Open an issue on GitHub
- Review existing documentation

Happy robot controlling! 🤖
