"""
企业微信 Webhook 支付确认服务器

功能:
1. 接收企业微信群机器人的 Webhook 消息
2. 解析消息内容 (支付成功/支付失败)
3. 自动打开对应的浏览器页面

使用方法:
1. 运行此脚本: python wechat_webhook_server.py
2. 使用 ngrok 或 cpolar 暴露本地端口到公网
3. 在企业微信群机器人配置中设置 Webhook URL
4. 在群里发送消息触发
"""

from flask import Flask, request, jsonify
import webbrowser
import logging
from datetime import datetime

app = Flask(__name__)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 配置
PAYMENT_SUCCESS_URL = "http://localhost:8000/payment_success.html"
PAYMENT_FAILED_URL = "http://localhost:8000/payment_failed.html"

@app.route('/webhook/payment', methods=['POST'])
def handle_payment_webhook():
    """
    处理企业微信 Webhook 消息
    
    企业微信消息格式:
    {
        "msgtype": "text",
        "text": {
            "content": "支付成功 订单号:123456"
        }
    }
    """
    try:
        data = request.json
        logger.info(f"Received webhook: {data}")
        
        # 解析消息类型
        if data.get('msgtype') != 'text':
            return jsonify({"error": "Only text messages are supported"}), 400
        
        # 获取消息内容
        content = data.get('text', {}).get('content', '').strip()
        logger.info(f"Message content: {content}")
        
        # 判断支付状态
        if '支付成功' in content or 'PAY_SUCCESS' in content.upper():
            logger.info("Payment SUCCESS detected - Opening success page...")
            webbrowser.open(PAYMENT_SUCCESS_URL)
            
            # 提取订单号 (如果有)
            order_id = extract_order_id(content)
            
            return jsonify({
                "status": "success",
                "action": "opened_success_page",
                "order_id": order_id,
                "timestamp": datetime.now().isoformat()
            })
            
        elif '支付失败' in content or 'PAY_FAIL' in content.upper():
            logger.info("Payment FAILED detected - Opening failed page...")
            webbrowser.open(PAYMENT_FAILED_URL)
            
            return jsonify({
                "status": "failed",
                "action": "opened_failed_page",
                "timestamp": datetime.now().isoformat()
            })
            
        else:
            logger.warning(f"Unknown message format: {content}")
            return jsonify({
                "status": "ignored",
                "message": "Message does not contain payment keywords"
            })
            
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return jsonify({"error": str(e)}), 500

def extract_order_id(content):
    """从消息中提取订单号"""
    import re
    # 匹配 "订单号:123456" 或 "订单号 123456"
    match = re.search(r'订单号[:\s]*(\w+)', content)
    if match:
        return match.group(1)
    return None

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        "status": "running",
        "service": "WeChat Work Payment Webhook",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/test/success', methods=['GET'])
def test_success():
    """测试成功页面"""
    webbrowser.open(PAYMENT_SUCCESS_URL)
    return jsonify({"message": "Success page opened"})

@app.route('/test/failed', methods=['GET'])
def test_failed():
    """测试失败页面"""
    webbrowser.open(PAYMENT_FAILED_URL)
    return jsonify({"message": "Failed page opened"})

if __name__ == '__main__':
    logger.info("Starting WeChat Work Payment Webhook Server...")
    logger.info(f"Success URL: {PAYMENT_SUCCESS_URL}")
    logger.info(f"Failed URL: {PAYMENT_FAILED_URL}")
    logger.info("Server running on http://localhost:5000")
    logger.info("Webhook endpoint: http://localhost:5000/webhook/payment")
    logger.info("\nTo expose to internet, use:")
    logger.info("  ngrok http 5000")
    logger.info("  or cpolar http 5000")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
