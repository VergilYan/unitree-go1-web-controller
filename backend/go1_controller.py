"""
GO1 Controller Module
This module handles the high-level control logic for the Unitree GO1 robot.
For now, it simply prints commands (safe mode).
Later, we'll add real UDP communication with the robot.
"""

class GO1Controller:
    """
    Main controller class for GO1 robot.
    Provides methods to send movement commands.
    """
    
    def __init__(self):
        """
        Initialize the GO1 controller.
        In safe mode, we just set up logging.
        Later, this will initialize UDP communication.
        """
        print("[GO1 Controller] Initializing in SAFE MODE (no real robot connection)")
        print("[GO1 Controller] Ready to receive commands...")
        
        # Store current movement state
        self.current_command = "stop"
    
    def forward(self, speed: float = 0.5):
        """
        Move the robot forward.
        
        Args:
            speed: Movement speed (0.0 to 1.0, where 1.0 is maximum)
        """
        self.current_command = "forward"
        print(f"[GO1 Controller] Command: FORWARD | Speed: {speed}")
        # TODO: Later, send actual UDP command to robot
    
    def backward(self, speed: float = 0.5):
        """
        Move the robot backward.
        
        Args:
            speed: Movement speed (0.0 to 1.0, where 1.0 is maximum)
        """
        self.current_command = "backward"
        print(f"[GO1 Controller] Command: BACKWARD | Speed: {speed}")
        # TODO: Later, send actual UDP command to robot
    
    def turn_left(self, speed: float = 0.5):
        """
        Turn the robot to the left.
        
        Args:
            speed: Turning speed (0.0 to 1.0, where 1.0 is maximum)
        """
        self.current_command = "left"
        print(f"[GO1 Controller] Command: TURN LEFT | Speed: {speed}")
        # TODO: Later, send actual UDP command to robot
    
    def turn_right(self, speed: float = 0.5):
        """
        Turn the robot to the right.
        
        Args:
            speed: Turning speed (0.0 to 1.0, where 1.0 is maximum)
        """
        self.current_command = "right"
        print(f"[GO1 Controller] Command: TURN RIGHT | Speed: {speed}")
        # TODO: Later, send actual UDP command to robot
    
    def stop(self):
        """
        Stop all movement of the robot.
        """
        self.current_command = "stop"
        print("[GO1 Controller] Command: STOP")
        # TODO: Later, send actual UDP command to robot
    
    def get_status(self):
        """
        Get current status of the controller.
        
        Returns:
            dict: Current command and connection status
        """
        return {
            "current_command": self.current_command,
            "connection_status": "safe_mode"  # Will change to "connected" later
        }
