"""
GO1 Controller Module
This module handles high-level control logic for the Unitree GO1 robot.

Key Features:
- SAFE MODE switch for testing without robot
- High-level UDP communication using Unitree SDK
- Movement commands: forward, backward, left, right, stop
- Continuous 500Hz command sending loop

Network Configuration:
- Robot IP (SPORT mode): 192.168.123.161
- Local UDP port: 8080
- Robot UDP port: 8082
- HIGHLEVEL control mode: 0xee

Safety Notes:
- Speed is limited to safe values (max 0.5 m/s forward/backward)
- Always test in SAFE MODE first
- Ensure robot has enough space before enabling REAL_ROBOT
"""

import time
import threading
import sys
import os

# ==============================================================================
# SAFETY SETTINGS - CHANGE THESE CAREFULLY!
# ==============================================================================
# Set to True ONLY when robot is connected and ready!
REAL_ROBOT = True

# Maximum movement speed (SAFE VALUES)
MAX_FORWARD_SPEED = 0.5   # m/s (GO1 max: 1.5 m/s in trot)
MAX_BACKWARD_SPEED = 0.3  # m/s (GO1 max: 1.1 m/s)
MAX_TURN_SPEED = 1.0      # rad/s (GO1 max: ~3.0 rad/s)

# Network settings
ROBOT_IP = "192.168.123.161"  # GO1 SPORT mode IP (for high-level control)
LOCAL_PORT = 8080              # Local UDP port
ROBOT_PORT = 8082              # GO1 SPORT mode port

# Control modes
HIGHLEVEL = 0xee  # Use high-level control (walking commands)
LOWLEVEL = 0xff   # Low-level control (direct motor control) - NOT USED HERE

# Try to import Unitree SDK (only if REAL_ROBOT is True)
sdk = None
if REAL_ROBOT:
    try:
        # Get absolute path to SDK (works from any directory)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sdk_path = os.path.join(current_dir, '../sdk/unitree_legged_sdk/lib/python/amd64')
        sdk_path = os.path.abspath(sdk_path)
        
        print(f"[GO1 Controller] 📂 Adding SDK path: {sdk_path}")
        sys.path.append(sdk_path)
        
        # Check if SDK file exists
        if os.path.exists(sdk_path):
            print(f"[GO1 Controller] ✅ SDK directory exists")
            files = os.listdir(sdk_path)
            print(f"[GO1 Controller] 📁 SDK files: {files}")
        else:
            print(f"[GO1 Controller] ❌ SDK directory not found: {sdk_path}")
        
        # Import the SDK
        import robot_interface as sdk
        print("[GO1 Controller] ✅ Successfully imported Unitree SDK")
        
    except ImportError as e:
        print(f"[GO1 Controller] ❌ ERROR: Could not import Unitree SDK: {e}")
        print(f"[GO1 Controller] ❌ Python version: {sys.version}")
        print("[GO1 Controller] Falling back to SAFE MODE")
        REAL_ROBOT = False
    except Exception as e:
        print(f"[GO1 Controller] ❌ Unexpected error: {e}")
        print(f"[GO1 Controller] ❌ Detailed error: {type(e).__name__}")
        print("[GO1 Controller] Falling back to SAFE MODE")
        REAL_ROBOT = False


class GO1Controller:
    """
    Main controller class for GO1 robot.
    Handles UDP communication and movement commands.
    """
    
    def __init__(self):
        """
        Initialize the GO1 controller.
        Sets up UDP communication if REAL_ROBOT is True.
        """
        # Store current movement state
        self.current_command = "stop"
        self.current_speed = 0.0
        self.current_yaw_speed = 0.0
        
        # UDP communication objects
        self.udp = None
        self.cmd = None
        self.state = None
        
        # Control loop flag
        self.running = False
        self.control_thread = None
        
        # Initialize connection if REAL_ROBOT is enabled
        if REAL_ROBOT:
            self._init_udp_connection()
        else:
            print("[GO1 Controller] 🟡 Initializing in SAFE MODE (no real robot connection)")
            print("[GO1 Controller] Set REAL_ROBOT = True to connect to actual robot")
        
        print("[GO1 Controller] Ready to receive commands...")
    
    def _init_udp_connection(self):
        """
        Initialize UDP connection to the GO1 robot.
        This sets up the communication pipe between computer and robot.
        """
        try:
            print(f"[GO1 Controller] 📡 Initializing UDP connection...")
            print(f"[GO1 Controller]   Robot IP: {ROBOT_IP}:{ROBOT_PORT}")
            print(f"[GO1 Controller]   Local port: {LOCAL_PORT}")
            
            # Create UDP object for high-level control (same as example)
            self.udp = sdk.UDP(HIGHLEVEL, LOCAL_PORT, ROBOT_IP, ROBOT_PORT)
            
            # Create command and state objects
            self.cmd = sdk.HighCmd()
            self.state = sdk.HighState()
            
            # Initialize command with safe defaults
            self.udp.InitCmdData(self.cmd)
            
            # Initialize command to idle state (like example)
            self._reset_command()
            
            # Start the control loop in a background thread
            self.running = True
            self.control_thread = threading.Thread(target=self._control_loop)
            self.control_thread.daemon = True
            self.control_thread.start()
            
            print("[GO1 Controller] ✅ UDP connection established successfully!")
            
        except Exception as e:
            print(f"[GO1 Controller] ❌ ERROR: Failed to initialize UDP connection: {e}")
            print(f"[GO1 Controller] ❌ Detailed error: {type(e).__name__}")
            print("[GO1 Controller] Falling back to SAFE MODE")
            REAL_ROBOT = False
    
    def _reset_command(self):
        """
        Reset command to safe idle state (same as example)
        """
        if self.cmd is not None:
            self.cmd.mode = 0           # 0: idle/stand
            self.cmd.gaitType = 0       # 0: idle
            self.cmd.speedLevel = 0     # Speed level
            self.cmd.footRaiseHeight = 0.08  # Foot raise height
            self.cmd.bodyHeight = 0     # Body height adjustment
            self.cmd.euler = [0, 0, 0]  # Orientation (roll, pitch, yaw)
            self.cmd.velocity = [0, 0]  # [forward, side] velocity
            self.cmd.yawSpeed = 0.0     # Rotation speed
            self.cmd.reserve = 0        # Reserved field
    
    def _control_loop(self):
        """
        Background control loop that runs at 500Hz.
        Continuously sends commands to the robot.
        Order matches official example: sleep first, then recv, then send
        """
        print("[GO1 Controller] 🔄 Starting control loop (500Hz)...")
        motiontime = 0
        command_count = 0
        
        while self.running:
            try:
                # Small delay FIRST (same as official example)
                time.sleep(0.002)
                motiontime += 1
                
                # Receive current robot state (IMU, battery, etc.)
                recv_result = self.udp.Recv()
                
                # Get received data
                self.udp.GetRecv(self.state)
                
                # Send the pre-set command
                self.udp.SetSend(self.cmd)
                send_result = self.udp.Send()
                
                # Debug: Print state every 100 cycles (500Hz / 100 = 5Hz)
                if motiontime % 100 == 0:
                    print(f"[GO1 Controller] 📊 State: mode={self.state.mode}, gait={self.state.gaitType}, battery={self.state.bms.SOC if hasattr(self.state, 'bms') else 'N/A'}%")
                    print(f"[GO1 Controller] 📤 Sending command: mode={self.cmd.mode}, gait={self.cmd.gaitType}, velocity={self.cmd.velocity}, yaw={self.cmd.yawSpeed}")
                    command_count = 0
                
                # Count how many times we send commands
                command_count += 1
                
            except Exception as e:
                print(f"[GO1 Controller] ❌ ERROR in control loop: {e}")
                time.sleep(0.002)
    
    def _set_walk_command(self, vx: float, vy: float = 0.0, yaw_speed: float = 0.0):
        """
        Set walking command parameters.
        
        Args:
            vx: Forward/backward speed (-0.3 to 0.5 m/s)
            vy: Sideways speed (-0.5 to 0.5 m/s)
            yaw_speed: Rotation speed (-1.0 to 1.0 rad/s)
        """
        if REAL_ROBOT and self.cmd is not None:
            # Set walking mode (same as example)
            self.cmd.mode = 2              # Mode 2 = continuous walking
            self.cmd.gaitType = 1          # Gait type 1 = trot
            self.cmd.speedLevel = 0        # Speed level
            self.cmd.footRaiseHeight = 0.08  # Foot raise height (8cm)
            self.cmd.bodyHeight = 0.0      # No body height adjustment
            self.cmd.euler = [0, 0, 0]     # Keep body level
            self.cmd.velocity = [vx, vy]   # [forward_speed, side_speed]
            self.cmd.yawSpeed = yaw_speed  # Rotation speed
            self.cmd.reserve = 0           # Reserved field
            
            print(f"[GO1 Controller] 📤 Setting walk command: vx={vx}, vy={vy}, yaw={yaw_speed}")
        
    def _set_idle_command(self):
        """
        Set robot to idle mode (stop moving).
        """
        if REAL_ROBOT and self.cmd is not None:
            # Set idle mode (robot will stand still)
            self._reset_command()
            print("[GO1 Controller] 📤 Setting idle command")
    
    def forward(self, speed: float = 0.5):
        """
        Move the robot forward.
        
        Args:
            speed: Movement speed (0.0 to 1.0, where 1.0 = MAX_FORWARD_SPEED)
        """
        # Calculate actual speed (limit to safe maximum)
        actual_speed = min(speed * MAX_FORWARD_SPEED, MAX_FORWARD_SPEED)
        
        self.current_command = "forward"
        self.current_speed = actual_speed
        self.current_yaw_speed = 0.0
        
        print(f"[GO1 Controller] ➡️ Command: FORWARD | Speed: {actual_speed:.2f} m/s")
        
        if REAL_ROBOT:
            self._set_walk_command(vx=actual_speed)
    
    def backward(self, speed: float = 0.5):
        """
        Move the robot backward.
        
        Args:
            speed: Movement speed (0.0 to 1.0, where 1.0 = MAX_BACKWARD_SPEED)
        """
        # Calculate actual speed (limit to safe maximum)
        actual_speed = min(speed * MAX_BACKWARD_SPEED, MAX_BACKWARD_SPEED)
        
        self.current_command = "backward"
        self.current_speed = -actual_speed
        self.current_yaw_speed = 0.0
        
        print(f"[GO1 Controller] ⬅️ Command: BACKWARD | Speed: {actual_speed:.2f} m/s")
        
        if REAL_ROBOT:
            self._set_walk_command(vx=-actual_speed)
    
    def turn_left(self, speed: float = 0.5):
        """
        Turn the robot to the left.
        
        Args:
            speed: Turning speed (0.0 to 1.0, where 1.0 = MAX_TURN_SPEED)
        """
        # Calculate actual turn speed (limit to safe maximum)
        actual_speed = min(speed * MAX_TURN_SPEED, MAX_TURN_SPEED)
        
        self.current_command = "left"
        self.current_speed = 0.0
        self.current_yaw_speed = actual_speed
        
        print(f"[GO1 Controller] 🔄 Command: TURN LEFT | Speed: {actual_speed:.2f} rad/s")
        
        if REAL_ROBOT:
            self._set_walk_command(vx=0.0, yaw_speed=actual_speed)
    
    def turn_right(self, speed: float = 0.5):
        """
        Turn the robot to the right.
        
        Args:
            speed: Turning speed (0.0 to 1.0, where 1.0 = MAX_TURN_SPEED)
        """
        # Calculate actual turn speed (limit to safe maximum)
        actual_speed = min(speed * MAX_TURN_SPEED, MAX_TURN_SPEED)
        
        self.current_command = "right"
        self.current_speed = 0.0
        self.current_yaw_speed = -actual_speed
        
        print(f"[GO1 Controller] 🔄 Command: TURN RIGHT | Speed: {actual_speed:.2f} rad/s")
        
        if REAL_ROBOT:
            self._set_walk_command(vx=0.0, yaw_speed=-actual_speed)
    
    def stop(self):
        """
        Stop all movement of the robot.
        """
        self.current_command = "stop"
        self.current_speed = 0.0
        self.current_yaw_speed = 0.0
        
        print("[GO1 Controller] ⏹️ Command: STOP")
        
        if REAL_ROBOT:
            self._set_idle_command()
    
    def get_status(self):
        """
        Get current status of the controller.
        
        Returns:
            dict: Current command, speed, and connection status
        """
        status = {
            "current_command": self.current_command,
            "current_speed": self.current_speed,
            "current_yaw_speed": self.current_yaw_speed,
            "connection_status": "connected" if REAL_ROBOT else "safe_mode",
            "real_robot_enabled": REAL_ROBOT
        }
        
        # Add robot state if connected
        if REAL_ROBOT and self.state is not None:
            status.update({
                "robot_mode": self.state.mode,
                "robot_gait_type": self.state.gaitType,
                "battery_soc": self.state.bms.SOC if hasattr(self.state, 'bms') else "N/A"
            })
        
        return status
    
    def __del__(self):
        """
        Cleanup when controller is destroyed.
        """
        if REAL_ROBOT:
            self.running = False
            if self.control_thread:
                self.control_thread.join(timeout=1.0)
            print("[GO1 Controller] 🔌 UDP connection closed")
