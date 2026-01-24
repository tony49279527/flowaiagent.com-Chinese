"""
Unified Payment Polling Server

Features:
1. Stores payment status in memory
2. Provides /api/check_status for frontend polling
3. Provides /api/update_status for admin trigger
4. Provides /trigger UI for admin control

Usage:
1. Run: python payment_server.py
2. Expose: ngrok http 5000
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import logging
from datetime import datetime
import os

# Serve static files from current directory
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend polling

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- In-Memory State ---
payment_state = {
    "status": "PENDING",
    "updated_at": None,
    "last_order_id": None
}

@app.route('/')
def home():
    """Serve the Main Website Homepage"""
    return send_from_directory('.', 'index.html')

@app.route('/admin')
def admin_dashboard():
    """Admin Dashboard for Controlling Payment Status"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Payment Control Center</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: sans-serif; padding: 20px; text-align: center; }
            .btn { padding: 20px 40px; font-size: 20px; margin: 10px; border: none; border-radius: 8px; cursor: pointer; color: white; width: 80%; max-width: 300px; }
            .success { background: #4CAF50; }
            .failed { background: #f44336; }
            .reset { background: #9E9E9E; }
            .status { margin: 20px; padding: 15px; background: #eee; border-radius: 5px; }
        </style>
    </head>
    <body>
        <h1>🎛️ Payment Control Center</h1>
        
        <div class="status">
            Current Status: <strong id="status-text">PENDING</strong>
        </div>

        <button class="btn success" onclick="updateStatus('SUCCESS')">✅ Payment Received</button>
        <br>
        <button class="btn failed" onclick="updateStatus('FAILED')">❌ Payment Failed</button>
        <br>
        <button class="btn reset" onclick="updateStatus('PENDING')">🔄 Reset to Pending</button>

        <script>
            function updateStatus(status) {
                fetch('/api/update_status', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({status: status})
                })
                .then(res => res.json())
                .then(data => {
                    document.getElementById('status-text').innerText = data.current_status;
                    alert('Status updated to: ' + data.current_status);
                });
            }
            
            // Initial check
            fetch('/api/check_status')
                .then(res => res.json())
                .then(data => {
                    document.getElementById('status-text').innerText = data.status;
                });
        </script>
    </body>
    </html>
    """

@app.route('/<path:path>')
def serve_static(path):
    """Explicitly serve static files"""
    return send_from_directory('.', path)

@app.route('/api/update_status', methods=['POST'])
def update_status():
    """Admin Endpoint to Update Status"""
    data = request.json
    new_status = data.get('status')
    
    if new_status in ['SUCCESS', 'FAILED', 'PENDING']:
        payment_state['status'] = new_status
        payment_state['updated_at'] = datetime.now().isoformat()
        logger.info(f"State Updated: {payment_state}")
        return jsonify({"message": "Status updated", "current_status": new_status})
    
    return jsonify({"error": "Invalid status"}), 400

@app.route('/api/check_status', methods=['GET'])
def check_status():
    """Frontend Endpoint to Poll Status"""
    # Return current state
    return jsonify(payment_state)

if __name__ == '__main__':
    # Log files in current directory for debugging
    try:
        logger.info(f"Current Directory: {os.getcwd()}")
        logger.info(f"Files: {os.listdir('.')}")
    except Exception as e:
        logger.error(f"Error listing files: {e}")

    port = int(os.environ.get('PORT', 8080))
    logger.info(f"Starting Payment Polling Server on port {port}...")
    app.run(host='0.0.0.0', port=port)
