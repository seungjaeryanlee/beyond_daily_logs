#_*_ coding: utf-8 _*_
class Config(object):
    """Configuration"""
    DB_DIR = "db"
    EXPORTED_DB_DIR = "exported_db"
    LOG_CHANNEL = "daily-logs"
    PAST_LOG_CHANNELS = ["daily-logs-alpha"]
    CHILDREN_USER_FLAG = 'parent_user_id'
    MSG_COUNT = 1000
