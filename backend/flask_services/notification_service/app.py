from flask import Flask, request, jsonify
import os
from src.notification_handler import NotificationHandler

app = Flask(__name__)

# 初始化通知處理器
notification_handler = NotificationHandler()

@app.route('/health', methods=['GET'])
def health_check():
    """健康檢查端點"""
    return jsonify({'status': 'healthy', 'service': 'notification_service'})

@app.route('/send-notification', methods=['POST'])
def send_notification():
    """發送通知"""
    try:
        data = request.get_json()
        
        notification_type = data.get('type')  # email, sms, push
        recipient = data.get('recipient')
        message = data.get('message')
        subject = data.get('subject', '')
        
        result = notification_handler.send_notification(
            notification_type, recipient, message, subject
        )
        
        return jsonify({'success': True, 'result': result})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/notifications/batch', methods=['POST'])
def send_batch_notifications():
    """批量發送通知"""
    try:
        data = request.get_json()
        notifications = data.get('notifications', [])
        
        results = []
        for notification in notifications:
            result = notification_handler.send_notification(
                notification.get('type'),
                notification.get('recipient'),
                notification.get('message'),
                notification.get('subject', '')
            )
            results.append(result)
        
        return jsonify({'success': True, 'results': results})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
