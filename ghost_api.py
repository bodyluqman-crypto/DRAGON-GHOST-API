from flask import Flask, request, jsonify
from datetime import datetime
import threading
import time
from utils import logger, APIValidator, AccountManager
from account_handler import SingleAccountPool, GhostAccount
from config import Config

app = Flask(__name__)
account_pool = SingleAccountPool()

api_stats = {
    'start_time': datetime.now(),
    'total_requests': 0,
    'successful_ghost_attacks': 0,
    'failed_attacks': 0,
    'main_account': Config.MAIN_ACCOUNT_ID
}

@app.before_request
def before_request():
    api_stats['total_requests'] += 1
    
    if not APIValidator.check_api_status():
        return jsonify({
            'status': 'error',
            'message': 'API has expired. Please contact administrator.'
        }), 403

@app.route('/')
def home():
    return jsonify({
        'status': 'success',
        'message': '🚀 DRAGON Single Ghost API is running',
        'version': '2.0',
        'author': 'DRAGON',
        'mode': 'Single Account Mode',
        'main_account': Config.MAIN_ACCOUNT_ID,
        'uptime': str(datetime.now() - api_stats['start_time']),
        'stats': api_stats
    })

@app.route('/api/ghost/attack', methods=['POST'])
def ghost_attack():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No JSON data provided'
            }), 400
        
        team_code = data.get('team_code')
        ghost_name = data.get('ghost_name', 'DRAGON Ghost')
        
        if not team_code:
            return jsonify({
                'status': 'error',
                'message': 'Team code is required'
            }), 400
        
        if not APIValidator.validate_team_code(team_code):
            return jsonify({
                'status': 'error',
                'message': 'Invalid team code format'
            }), 400
        
        # إرسال شبح واحد فقط
        success, message = account_pool.send_single_ghost_attack(team_code, ghost_name)
        
        if success:
            api_stats['successful_ghost_attacks'] += 1
            return jsonify({
                'status': 'success',
                'message': message,
                'team_code': team_code,
                'ghost_name': ghost_name,
                'account_used': Config.MAIN_ACCOUNT_ID,
                'timestamp': datetime.now().isoformat()
            })
        else:
            api_stats['failed_attacks'] += 1
            return jsonify({
                'status': 'error',
                'message': message
            }), 500
            
    except Exception as e:
        logger.error(f"Ghost attack error: {e}")
        api_stats['failed_attacks'] += 1
        return jsonify({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }), 500

@app.route('/api/account/status', methods=['GET'])
def account_status():
    try:
        account = account_pool.get_main_account()
        
        if account:
            status_info = {
                'status': 'success',
                'account_id': account.account_id,
                'connected': account.is_connected,
                'last_activity': account.last_activity.isoformat(),
                'connection_attempts': account.connection_attempts
            }
        else:
            status_info = {
                'status': 'error',
                'message': 'Main account not available'
            }
        
        return jsonify(status_info)
        
    except Exception as e:
        logger.error(f"Account status error: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Error getting account status: {str(e)}'
        }), 500

@app.route('/api/system/health', methods=['GET'])
def system_health():
    try:
        elapsed = datetime.now() - Config.START_TIME
        days_remaining = (Config.API_DURATION - elapsed).days
        
        account = account_pool.get_main_account()
        account_status = "Connected" if account and account.is_connected else "Disconnected"
        
        return jsonify({
            'status': 'success',
            'api_running': True,
            'api_name': 'DRAGON Single Ghost API',
            'mode': 'Single Account',
            'main_account': Config.MAIN_ACCOUNT_ID,
            'account_status': account_status,
            'start_time': Config.START_TIME.isoformat(),
            'days_remaining': max(0, days_remaining),
            'statistics': api_stats
        })
        
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Health check failed: {str(e)}'
        }), 500

@app.route('/api/ghost/test', methods=['POST'])
def test_ghost():
    """اختبار إرسال شبح"""
    try:
        data = request.get_json()
        team_code = data.get('team_code', '12345678')
        ghost_name = data.get('ghost_name', 'TEST GHOST')
        
        success, message = account_pool.send_single_ghost_attack(team_code, ghost_name)
        
        return jsonify({
            'status': 'success' if success else 'error',
            'message': message,
            'test_data': {
                'team_code': team_code,
                'ghost_name': ghost_name,
                'account_used': Config.MAIN_ACCOUNT_ID
            }
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Test failed: {str(e)}'
        }), 500

def background_maintenance():
    """الصيانة الخلفية للحساب"""
    while True:
        try:
            account = account_pool.get_main_account()
            if account and not account.is_connected:
                logger.info("🔄 محاولة إعادة توصيل الحساب...")
                account.connect()
            
            time.sleep(60)  # التحقق كل دقيقة
            
        except Exception as e:
            logger.error(f"Background maintenance error: {e}")
            time.sleep(30)

if __name__ == '__main__':
    # بدء الصيانة الخلفية
    maintenance_thread = threading.Thread(target=background_maintenance, daemon=True)
    maintenance_thread.start()
    
    logger.info("🚀 Starting DRAGON Single Ghost API Server...")
    logger.info(f"📅 API will run for {Config.API_DURATION.days} days")
    logger.info(f"👤 Single Account Mode: {Config.MAIN_ACCOUNT_ID}")
    
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG,
        use_reloader=False
      )
