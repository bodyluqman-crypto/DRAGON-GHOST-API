import os
from datetime import datetime, timedelta

class Config:
    HOST = '0.0.0.0'
    PORT = int(os.environ.get('PORT', 5000))
    DEBUG = False
    
    AES_KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    AES_IV = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    
    FREEFIRE_VERSION = "OB51"
    GET_LOGIN_URL = "https://clientbp.common.ggbluefox.com/GetLoginData"
    MAJOR_LOGIN_URL = "https://loginbp.ggblueshark.com/MajorLogin"
    
    MAX_RETRIES = 3
    RECONNECT_DELAY = 5
    SOCKET_TIMEOUT = 30
    
    ACCOUNTS_FILE = "accounts.json"
    LOG_FILE = "ghost_api.log"
    
    API_DURATION = timedelta(days=30)
    START_TIME = datetime.now()
    
    # إعدادات الشبح الفردي
    SINGLE_ACCOUNT_MODE = True
    MAIN_ACCOUNT_ID = "4315220774"
