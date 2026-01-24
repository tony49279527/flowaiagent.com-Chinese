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
import requests
import threading

# Serve static files from current directory
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend polling

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import json

# ... (logging config)

QUOTA_FILE = 'usage_quota.json'

def load_quota():
    if not os.path.exists(QUOTA_FILE):
        return {}
    try:
        with open(QUOTA_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_quota(data):
    with open(QUOTA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

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

# ... (admin_dashboard)

@app.route('/<path:path>')
def serve_static(path):
    """Explicitly serve static files"""
    return send_from_directory('.', path)

@app.route('/api/check_quota', methods=['POST'])
def check_quota():
    """Check and increment user quota"""
    data = request.json
    email = data.get('email', '').strip().lower()
    
    if not email:
        return jsonify({"error": "Email required"}), 400
        
    quota_db = load_quota()
    current_usage = quota_db.get(email, 0)
    
    if current_usage >= 2:
        return jsonify({"allowed": False, "usage": current_usage, "message": "Quota exceeded"})
    
    # Increment and save
    quota_db[email] = current_usage + 1
    save_quota(quota_db)
    
    logger.info(f"Quota used for {email}: {current_usage + 1}/2")
    return jsonify({"allowed": True, "usage": current_usage + 1})


# n8n Webhook URL for report generation
N8N_WEBHOOK_URL = 'https://tony4927.app.n8n.cloud/webhook/1573cd32-8e6a-46ac-9d74-1e6f7c9ea5e7'

# Store pending order data for webhook
pending_order_data = {}

def trigger_n8n_webhook(order_data):
    """Trigger n8n webhook to generate report"""
    try:
        logger.info(f"Triggering n8n webhook with data: {order_data}")
        response = requests.post(
            N8N_WEBHOOK_URL,
            json=order_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        logger.info(f"n8n webhook response: {response.status_code} - {response.text[:200]}")
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Error triggering n8n webhook: {e}")
        return False

@app.route('/api/update_status', methods=['POST'])
def update_status():
    """Admin Endpoint to Update Status and trigger webhook on SUCCESS"""
    data = request.json
    new_status = data.get('status')
    order_data = data.get('order_data', pending_order_data.get('latest', {}))
    
    if new_status in ['SUCCESS', 'FAILED', 'PENDING']:
        payment_state['status'] = new_status
        payment_state['updated_at'] = datetime.now().isoformat()
        logger.info(f"State Updated: {payment_state}")
        
        # If SUCCESS, trigger n8n webhook in background thread
        if new_status == 'SUCCESS' and order_data:
            logger.info("Payment SUCCESS - Triggering n8n webhook...")
            thread = threading.Thread(target=trigger_n8n_webhook, args=(order_data,))
            thread.start()
        
        return jsonify({
            "message": "Status updated", 
            "current_status": new_status,
            "webhook_triggered": new_status == 'SUCCESS'
        })
    
    return jsonify({"error": "Invalid status"}), 400

@app.route('/api/set_order_data', methods=['POST'])
def set_order_data():
    """Store order data for webhook trigger"""
    data = request.json
    pending_order_data['latest'] = data
    logger.info(f"Order data stored: {data}")
    return jsonify({"message": "Order data stored"})

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
