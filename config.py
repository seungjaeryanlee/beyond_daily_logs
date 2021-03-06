#_*_ coding: utf-8 _*_
class Config(object):
    """Configuration"""
    DB_DIR = "db"
    LOGS_DB = "logs"
    USERS_DB = "users/users.pkl"
    EXPORTED_DB_DIR = "exported_db"
    LOG_CHANNEL = "daily-logs"
    PAST_LOG_CHANNELS = ["daily-logs-alpha"]
    CHILDREN_USER_FLAG = 'parent_user_id'
    MSG_COUNT = 1000
    ETC_TASK_NAME = 'ETC'
    TASK_TYPE = ['완료', '오늘 할 일', '일시정지']
    TEST = False
