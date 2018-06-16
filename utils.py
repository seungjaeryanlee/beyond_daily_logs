#_*_ coding: utf-8 _*_
import os
from collections import defaultdict
from datetime import datetime
from config import Config

def nested_dict():
    """Create nested dictionary"""
    return defaultdict(nested_dict)


def get_logs_files(db_path):
    """Get log files of each log directory in exported data"""
    files = {}
    logs_dirs = [Config.LOG_CHANNEL] + Config.PAST_LOG_CHANNELS

    for logs_dir in logs_dirs:
        logs_path = os.path.join(db_path, logs_dir)
        files[logs_dir] = os.listdir(logs_path)

    return files


def filter_parent_msg(messages, db_dict):
    """Filter parent messages from all messages and return nested dict"""
    for msg in messages:
        if Config.CHILDREN_USER_FLAG not in msg and 'user' in msg:
            ymd = datetime.fromtimestamp(float(msg['ts'])).strftime("%Y%m%d")
            year, month_date = ymd[:4], ymd[4:]
            user, text = msg['user'], msg['text']
            db_dict[year][month_date][user] = text

    return db_dict
