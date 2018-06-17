#_*_ coding: utf-8 _*_
import os
import pickle
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

def change_id_to_name(user_id):
    """ """
    user_db_path = os.path.join(os.getcwd(), Config.DB_DIR, Config.USERS_DB)
    with open(user_db_path, 'rb') as f:
        user_db = pickle.load(f) 
        if user_id in user_db:
            return user_db[user_id]
        else:
            return None

def change_msg_to_db(messages, db_dict, year_db=False):
    """Filter parent messages from all messages and create database"""
    for msg in messages:
        if Config.CHILDREN_USER_FLAG not in msg and 'user' in msg:
            ymd = datetime.fromtimestamp(float(msg['ts'])).strftime("%Y%m%d")
            year, month_date = ymd[:4], ymd[4:]
            if year_db:
                db = db_dict
            else:
                db = db_dict[year]

            user_id, text = msg['user'], msg['text']
            user_name = change_id_to_name(user_id)
            user = user_name if user_name else user_id
            if month_date in db[user]:
                if text not in db[user][month_date]:
                    db[user][month_date].append(text)
            else:
                db[user][month_date] = [text]

    return db_dict
