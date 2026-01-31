"""
简化版支付确认触发服务器

使用方法:
1. 运行此脚本: python simple_trigger_server.py
2. 使用 ngrok/cpolar 暴露到公网
3. 在手机浏览器创建书签指向触发URL
4. 收到付款后点击书签即可

优点:
- 无需企业微信管理员权限
- 配置简单，立即可用
- 支持手机/电脑触发
"""

from flask import Flask, jsonify
import webbrowser
import logging
from datetime import datetime

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 配置
SUCCESS_URL = "http://localhost:8000/payment_success.html"
FAILED_URL = "http://localhost:8000/payment_failed.html"

@app.route('/')
def index():
    """首页 - 显示可用的触发链接"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>支付确认触发器</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .card {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }
            h1 {
                color: #333;
                text-align: center;
            }
            .btn {
                display: block;
                width: 100%;
                padding: 15px;
                margin: 10px 0;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
                text-decoration: none;
                text-align: center;
                color: white;
            }
            .btn-success {
                background: #4CAF50;
            }
            .btn-danger {
                background: #f44336;
            }
            .btn:hover {
                opacity: 0.9;
            }
            .info {
                background: #e3f2fd;
                padding: 15px;
                border-radius: 5px;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>💳 支付确认触发器</h1>
            <p style="text-align: center; color: #666;">点击按钮触发浏览器打开对应页面</p>
            
            <a href="/trigger/success" class="btn btn-success">✅ 支付成功</a>
            <a href="/trigger/failed" class="btn btn-danger">❌ 支付失败</a>
        </div>
        
        <div class="info">
            <strong>📱 使用提示:</strong>
            <ul>
                <li>将此页面添加到手机浏览器书签</li>
                <li>或直接收藏触发链接</li>
                <li>收到付款后点击对应按钮</li>
            </ul>
        </div>
    </body>
    </html>
    """
    return html

@app.route('/trigger/success')
def trigger_success():
    """触发支付成功"""
    logger.info("触发支付成功 - 打开成功页面")
    try:
        webbrowser.open(SUCCESS_URL)
        return jsonify({
            "status": "success",
            "message": "Success page opened",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"打开浏览器失败: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/trigger/failed')
def trigger_failed():
    """触发支付失败"""
    logger.info("触发支付失败 - 打开失败页面")
    try:
        webbrowser.open(FAILED_URL)
        return jsonify({
            "status": "failed",
            "message": "Failed page opened",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"打开浏览器失败: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    """健康检查"""
    return jsonify({
        "status": "running",
        "service": "Simple Payment Trigger",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    logger.info("=" * 50)
    logger.info("简化版支付确认触发服务器")
    logger.info("=" * 50)
    logger.info(f"成功页面: {SUCCESS_URL}")
    logger.info(f"失败页面: {FAILED_URL}")
    logger.info("")
    logger.info("服务器运行在: http://localhost:5000")
    logger.info("访问首页查看触发按钮: http://localhost:5000")
    logger.info("")
    logger.info("暴露到公网:")
    logger.info("  ngrok http 5000")
    logger.info("  或 cpolar http 5000")
    logger.info("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=False)
