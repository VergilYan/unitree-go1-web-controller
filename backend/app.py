"""
GO1 Web Controller - Flask Backend
This is the main web server that handles HTTP requests from the frontend.
It provides REST API endpoints for controlling the GO1 robot.
"""

# Import required modules
from flask import Flask, jsonify, request
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
    Body: {"speed": 0.5} (optional, range 0.1 to 1.0)
    Example: curl -X POST http://localhost:5000/forward -H "Content-Type: application/json" -d '{"speed": 0.8}'
    """
    speed = 0.5
    if request.is_json:
        data = request.get_json()
        if data and 'speed' in data:
            speed = max(0.1, min(1.0, float(data['speed'])))

    go1.forward(speed)
    return jsonify({
        "status": "success",
        "command": "forward",
        "speed": speed
    })

@app.route('/backward', methods=['POST'])
def backward():
    """
    API Endpoint: Move robot backward
    Method: POST
    Body: {"speed": 0.5} (optional, range 0.1 to 1.0)
    Example: curl -X POST http://localhost:5000/backward -H "Content-Type: application/json" -d '{"speed": 0.8}'
    """
    speed = 0.5
    if request.is_json:
        data = request.get_json()
        if data and 'speed' in data:
            speed = max(0.1, min(1.0, float(data['speed'])))

    go1.backward(speed)
    return jsonify({
        "status": "success",
        "command": "backward",
        "speed": speed
    })

@app.route('/left', methods=['POST'])
def left():
    """
    API Endpoint: Turn robot left
    Method: POST
    Body: {"speed": 0.5} (optional, range 0.1 to 1.0)
    Example: curl -X POST http://localhost:5000/left -H "Content-Type: application/json" -d '{"speed": 0.8}'
    """
    speed = 0.5
    if request.is_json:
        data = request.get_json()
        if data and 'speed' in data:
            speed = max(0.1, min(1.0, float(data['speed'])))

    go1.turn_left(speed)
    return jsonify({
        "status": "success",
        "command": "left",
        "speed": speed
    })

@app.route('/right', methods=['POST'])
def right():
    """
    API Endpoint: Turn robot right
    Method: POST
    Body: {"speed": 0.5} (optional, range 0.1 to 1.0)
    Example: curl -X POST http://localhost:5000/right -H "Content-Type: application/json" -d '{"speed": 0.8}'
    """
    speed = 0.5
    if request.is_json:
        data = request.get_json()
        if data and 'speed' in data:
            speed = max(0.1, min(1.0, float(data['speed'])))

    go1.turn_right(speed)
    return jsonify({
        "status": "success",
        "command": "right",
        "speed": speed
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

@app.route('/terrain', methods=['POST'])
def terrain():
    """
    API Endpoint: Set terrain mode
    Method: POST
    Body: {"terrain": "grass"} (options: grass, gravel, cobblestone, slope, stairs)
    Example: curl -X POST http://localhost:5000/terrain -H "Content-Type: application/json" -d '{"terrain": "gravel"}'
    """
    if not request.is_json:
        return jsonify({
            "status": "error",
            "message": "Request must be JSON"
        }), 400

    data = request.get_json()
    if not data or 'terrain' not in data:
        return jsonify({
            "status": "error",
            "message": "Missing 'terrain' field in request body"
        }), 400

    terrain_name = data['terrain']
    success = go1.set_terrain(terrain_name)

    if success:
        return jsonify({
            "status": "success",
            "terrain": terrain_name,
            "profile": go1.terrain_manager.current_profile.to_dict() if go1.terrain_manager else None
        })
    else:
        return jsonify({
            "status": "error",
            "message": f"Unknown terrain: {terrain_name}",
            "available_terrains": ["grass", "gravel", "cobblestone", "slope", "stairs"]
        }), 400

# ------------------- Run Server -------------------

if __name__ == '__main__':
    """
    Run the Flask web server.
    The server will be available at http://localhost:5000
    """
    print("Starting GO1 Web Controller backend...")
    print("Server running at: http://localhost:5000")
    print("API endpoints:")
    print("  Movement: /forward, /backward, /left, /right, /stop, /status")
    print("  Terrain: /terrain (POST)")

    # Run Flask in production mode (NOT debug mode)
    # debug=False prevents auto-reload which causes port conflicts with GO1 SDK
    # use_reloader=False prevents Flask from restarting and causing port conflicts
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
