"""
Unified Payment Polling Server (SQLite Version)

Features:
1. Stores payment status in SQLite database (orders.db)
2. Provides /api/check_status for frontend polling
3. Provides /api/update_status for admin trigger
4. Auto-creates SQLite table on startup

Usage:
1. Run: python payment_server.py
2. Expose: ngrok http 8080
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import logging
from datetime import datetime
import os
import requests
import threading
import sqlite3
import json

# Serve static files from current directory
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend polling

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_FILE = 'orders.db'

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    try:
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                status TEXT NOT NULL DEFAULT 'PENDING',
                order_data TEXT,
                updated_at TEXT,
                email TEXT,
                quota_usage INTEGER DEFAULT 0
            )
        ''')
        # Initialize default row if not exists (for single-user demo)
        cur = conn.execute('SELECT * FROM orders WHERE id = 1')
        if not cur.fetchone():
            conn.execute("INSERT INTO orders (id, status, updated_at) VALUES (1, 'PENDING', ?)", (datetime.now().isoformat(),))
            logger.info("Initialized default order row.")
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"DB Init Error: {e}")

# Initialize DB on start
init_db()

@app.route('/')
def home():
    """Serve the Main Website Homepage"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Explicitly serve static files"""
    return send_from_directory('.', path)

@app.route('/api/check_status', methods=['GET'])
def check_status():
    """Frontend Endpoint to Poll Status"""
    try:
        conn = get_db_connection()
        row = conn.execute('SELECT status, updated_at FROM orders WHERE id = 1').fetchone()
        conn.close()
        return jsonify(dict(row))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# n8n Webhook URL for report generation
N8N_WEBHOOK_URL = 'https://tony4927.app.n8n.cloud/webhook/1573cd32-8e6a-46ac-9d74-1e6f7c9ea5e7'

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
    
    # Optional: Update specific order data
    order_data = data.get('order_data', {})
    
    if new_status in ['SUCCESS', 'FAILED', 'PENDING']:
        updated_at = datetime.now().isoformat()
        try:
            conn = get_db_connection()
            # Update default row 1
            conn.execute('UPDATE orders SET status = ?, updated_at = ?, order_data = ? WHERE id = 1',
                         (new_status, updated_at, json.dumps(order_data)))
            conn.commit()
            conn.close()
            
            logger.info(f"State Updated: {new_status}")
            
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
        except Exception as e:
            logger.error(f"DB Update Error: {e}")
            return jsonify({"error": str(e)}), 500
    
    return jsonify({"error": "Invalid status"}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    logger.info(f"Starting Payment Polling Server (SQLite) on port {port}...")
    app.run(host='0.0.0.0', port=port)
