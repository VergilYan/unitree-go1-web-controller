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

// Button elements
const btnForward = document.getElementById('btn-forward');
const btnBackward = document.getElementById('btn-backward');
const btnLeft = document.getElementById('btn-left');
const btnRight = document.getElementById('btn-right');
const btnStop = document.getElementById('btn-stop');

/**
 * Send command to backend API
 * @param {string} command - The command to send (forward, backward, left, right, stop)
 */
async function sendCommand(command) {
    try {
        // Show loading state
        currentCommandElement.textContent = `Sending ${command}...`;
        
        // Send POST request to backend using fetch()
        const response = await fetch(`${API_BASE_URL}/${command}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
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
    btnForward.addEventListener('click', () => sendCommand('forward'));
    btnBackward.addEventListener('click', () => sendCommand('backward'));
    btnLeft.addEventListener('click', () => sendCommand('left'));
    btnRight.addEventListener('click', () => sendCommand('right'));
    btnStop.addEventListener('click', () => sendCommand('stop'));
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
            sendCommand('forward');
            break;
        case 's':
            sendCommand('backward');
            break;
        case 'a':
            sendCommand('left');
            break;
        case 'd':
            sendCommand('right');
            break;
        case ' ':
            sendCommand('stop');
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
    
    // Check backend connection on startup
    checkBackendConnection();
    
    // Check connection periodically (every 5 seconds)
    setInterval(checkBackendConnection, 5000);
    
    console.log('GO1 Web Controller ready!');
}

// Run initialization when the page loads
document.addEventListener('DOMContentLoaded', init);
