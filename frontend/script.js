/**
 * GO1 Web Controller - Frontend JavaScript
 * Handles:
 * - Button clicks
 * - Keyboard input
 * - API communication with Flask backend
 * - Status updates
 */

// Backend API URL (Flask server address)
const API_BASE_URL = 'http://localhost:5000';

// DOM elements we'll interact with
const connectionStatusElement = document.getElementById('connection-status');
const currentCommandElement = document.getElementById('current-command');
const speedSliderElement = document.getElementById('speed-slider');
const speedValueElement = document.getElementById('speed-value');

// Current speed value
let currentSpeed = 0.5;

// Button elements
const btnForward = document.getElementById('btn-forward');
const btnBackward = document.getElementById('btn-backward');
const btnLeft = document.getElementById('btn-left');
const btnRight = document.getElementById('btn-right');
const btnStop = document.getElementById('btn-stop');

// Terrain button elements
const terrainButtons = document.querySelectorAll('.terrain-btn');
const currentTerrainElement = document.getElementById('current-terrain');

// Foot raise slider elements
const footRaiseSlider = document.getElementById('foot-raise-slider');
const footRaiseValue = document.getElementById('foot-raise-value');

/**
 * Send command to backend API
 * @param {string} command - The command to send (forward, backward, left, right, stop)
 * @param {number} speed - The speed parameter (0.1 to 1.0)
 */
async function sendCommand(command, speed = 0.5) {
    try {
        // Show loading state
        currentCommandElement.textContent = `Sending ${command}...`;

        // Send POST request to backend using fetch()
        const response = await fetch(`${API_BASE_URL}/${command}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ speed: speed }),
        });

        // Parse JSON response from backend
        const data = await response.json();

        // Update UI with response
        if (data.status === 'success') {
            currentCommandElement.textContent = data.command.toUpperCase();
            updateConnectionStatus(true);
        } else {
            currentCommandElement.textContent = 'Error';
            updateConnectionStatus(false);
        }

    } catch (error) {
        // Handle errors (e.g., backend not running)
        console.error('Error sending command:', error);
        currentCommandElement.textContent = 'Connection Error';
        updateConnectionStatus(false);
    }
}

/**
 * Update connection status display
 * @param {boolean} isConnected - Whether we're connected to backend
 */
function updateConnectionStatus(isConnected) {
    if (isConnected) {
        connectionStatusElement.textContent = 'Connected';
        connectionStatusElement.classList.remove('disconnected');
    } else {
        connectionStatusElement.textContent = 'Disconnected';
        connectionStatusElement.classList.add('disconnected');
    }
}

/**
 * Set terrain mode
 * @param {string} terrain - Terrain name (grass, gravel, cobblestone, slope, stairs)
 */
async function setTerrain(terrain) {
    try {
        const response = await fetch(`${API_BASE_URL}/terrain`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ terrain: terrain }),
        });

        const data = await response.json();

        if (data.status === 'success') {
            console.log(`[Frontend] Terrain changed to: ${terrain}`);

            // Update all terrain buttons to remove active class
            terrainButtons.forEach(btn => {
                btn.classList.remove('active');
            });

            // Add active class to selected terrain button
            const selectedButton = document.getElementById(`terrain-${terrain}`);
            if (selectedButton) {
                selectedButton.classList.add('active');
            }

            // Update current terrain display
            if (currentTerrainElement && data.profile) {
                currentTerrainElement.textContent = data.profile.name;
            }

            updateConnectionStatus(true);
        } else {
            console.error('[Frontend] Failed to change terrain:', data.message);
            updateConnectionStatus(false);
        }
    } catch (error) {
        console.error('[Frontend] Error changing terrain:', error);
        updateConnectionStatus(false);
    }
}

/**
 * Set foot raise height
 * @param {number} height - Foot raise height in meters (0.05 to 0.30)
 */
async function setFootRaiseHeight(height) {
    try {
        const response = await fetch(`${API_BASE_URL}/foot_raise`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ height: height }),
        });

        const data = await response.json();

        if (data.status === 'success') {
            console.log(`[Frontend] Foot raise height set to: ${height}m`);
            updateConnectionStatus(true);
        } else {
            console.error('[Frontend] Failed to set foot raise height:', data.message);
            updateConnectionStatus(false);
        }
    } catch (error) {
        console.error('[Frontend] Error setting foot raise height:', error);
        updateConnectionStatus(false);
    }
}

/**
 * Check if backend is reachable
 */
async function checkBackendConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/status`);
        if (response.ok) {
            const data = await response.json();
            currentCommandElement.textContent = data.current_command.toUpperCase();
            updateConnectionStatus(true);
        } else {
            updateConnectionStatus(false);
        }
    } catch (error) {
        updateConnectionStatus(false);
    }
}

/**
 * Handle button click events
 */
function setupButtonListeners() {
    btnForward.addEventListener('click', () => sendCommand('forward', currentSpeed));
    btnBackward.addEventListener('click', () => sendCommand('backward', currentSpeed));
    btnLeft.addEventListener('click', () => sendCommand('left', currentSpeed));
    btnRight.addEventListener('click', () => sendCommand('right', currentSpeed));
    btnStop.addEventListener('click', () => sendCommand('stop', currentSpeed));
}

/**
 * Handle keyboard events
 * @param {KeyboardEvent} event - The keyboard event
 */
function handleKeyPress(event) {
    // Get the key pressed (convert to lowercase for consistency)
    const key = event.key.toLowerCase();
    
    // Prevent default behavior for space bar (don't scroll page)
    if (key === ' ') {
        event.preventDefault();
    }
    
    // Map keys to commands
    switch (key) {
        case 'w':
            sendCommand('forward', currentSpeed);
            break;
        case 's':
            sendCommand('backward', currentSpeed);
            break;
        case 'a':
            sendCommand('left', currentSpeed);
            break;
        case 'd':
            sendCommand('right', currentSpeed);
            break;
        case ' ':
            sendCommand('stop', currentSpeed);
            break;
        default:
            // Ignore other keys
            break;
    }
}

/**
 * Initialize the application
 */
function init() {
    console.log('Initializing GO1 Web Controller...');

    // Setup button click listeners
    setupButtonListeners();

    // Setup keyboard listener
    document.addEventListener('keydown', handleKeyPress);

    // Setup speed slider listener
    if (speedSliderElement) {
        speedSliderElement.addEventListener('input', function() {
            currentSpeed = parseFloat(this.value);
            if (speedValueElement) {
                speedValueElement.textContent = currentSpeed.toFixed(1);
            }
            console.log('Speed changed to:', currentSpeed);
        });
    }

    // Setup terrain button listeners
    terrainButtons.forEach(button => {
        button.addEventListener('click', function() {
            const terrain = this.getAttribute('data-terrain');
            console.log('Terrain button clicked:', terrain);
            setTerrain(terrain);
        });
    });

    // Setup foot raise slider listener
    if (footRaiseSlider) {
        footRaiseSlider.addEventListener('input', function() {
            const height = parseFloat(this.value);
            if (footRaiseValue) {
                footRaiseValue.textContent = height.toFixed(2) + 'm';
            }
            console.log('Foot raise height changed to:', height);
            setFootRaiseHeight(height);
        });
    }

    // Check backend connection on startup
    checkBackendConnection();

    // Check connection periodically (every 5 seconds)
    setInterval(checkBackendConnection, 5000);

    console.log('GO1 Web Controller ready!');
}

// Run initialization when the page loads
document.addEventListener('DOMContentLoaded', init);
