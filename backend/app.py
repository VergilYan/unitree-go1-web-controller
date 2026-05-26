"""
GO1 Web Controller - Flask Backend
This is the main web server that handles HTTP requests from the frontend.
It provides REST API endpoints for controlling the GO1 robot.
"""

# Import required modules
from flask import Flask, jsonify
from flask_cors import CORS  # Handle cross-origin requests from frontend

# Import our GO1 controller
from go1_controller import GO1Controller

# Initialize Flask app
app = Flask(__name__)

# Enable CORS (allows frontend to communicate with backend)
CORS(app)

# Initialize the GO1 controller
go1 = GO1Controller()

# ------------------- API Endpoints -------------------

@app.route('/forward', methods=['POST'])
def forward():
    """
    API Endpoint: Move robot forward
    Method: POST
    Example: curl -X POST http://localhost:5000/forward
    """
    go1.forward()
    return jsonify({
        "status": "success",
        "command": "forward"
    })

@app.route('/backward', methods=['POST'])
def backward():
    """
    API Endpoint: Move robot backward
    Method: POST
    Example: curl -X POST http://localhost:5000/backward
    """
    go1.backward()
    return jsonify({
        "status": "success",
        "command": "backward"
    })

@app.route('/left', methods=['POST'])
def left():
    """
    API Endpoint: Turn robot left
    Method: POST
    Example: curl -X POST http://localhost:5000/left
    """
    go1.turn_left()
    return jsonify({
        "status": "success",
        "command": "left"
    })

@app.route('/right', methods=['POST'])
def right():
    """
    API Endpoint: Turn robot right
    Method: POST
    Example: curl -X POST http://localhost:5000/right
    """
    go1.turn_right()
    return jsonify({
        "status": "success",
        "command": "right"
    })

@app.route('/stop', methods=['POST'])
def stop():
    """
    API Endpoint: Stop robot movement
    Method: POST
    Example: curl -X POST http://localhost:5000/stop
    """
    go1.stop()
    return jsonify({
        "status": "success",
        "command": "stop"
    })

@app.route('/status', methods=['GET'])
def status():
    """
    API Endpoint: Get robot status
    Method: GET
    Example: curl http://localhost:5000/status
    """
    status = go1.get_status()
    return jsonify(status)

# ------------------- Run Server -------------------

if __name__ == '__main__':
    """
    Run the Flask web server.
    The server will be available at http://localhost:5000
    """
    print("Starting GO1 Web Controller backend...")
    print("Server running at: http://localhost:5000")
    print("API endpoints: /forward, /backward, /left, /right, /stop, /status")
    
    # Run Flask in debug mode for development
    # debug=True allows auto-reload when code changes
    app.run(host='0.0.0.0', port=5000, debug=True)
