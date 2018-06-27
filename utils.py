#_*_ coding: utf-8 _*_
import os
import re
import pickle
from collections import defaultdict
from datetime import datetime
from config import Config
from pprint import pprint

def nested_dict():
    """Create nested dictionary"""
    # TODO More description of what this function returns would be helpful.
    #      Is the intended effect to have defaultdict as a default value?
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
    """Change user id to user real name"""
    user_db_path = os.path.join(os.getcwd(), Config.DB_DIR, Config.USERS_DB)
    with open(user_db_path, 'rb') as f:
        user_db = pickle.load(f) 
        if user_id in user_db:
            return user_db[user_id]
        else:
            return None


def parse_tasks(text):
    """Parse text and categorize tasks"""
    # TODO Is there a particular reason you called dict() instead of {}?
    task_logs = dict()
    task_category = dict()

    text = re.sub('[\n]+','\n', text)
    matching_str = re.findall('[*]([\u3131-\u3163\uac00-\ud7a3\s]+)[*]\n([^*]+)', text)
    if matching_str:
        for (title, task) in matching_str:
            if title in Config.TASK_TYPE:
                task_list = task.split('\n')
                task_list = [ t for t in task_list if len(t) > 0 ]
                task_logs[title] = task_list
                task_category[title] = {}

                for t in task_list:
                    task_type_str = re.search('\[(\w+)\]', t)
                    if task_type_str:
                        task_type = task_type_str.group(1)
                    else:
                        task_type = Config.ETC_TASK_NAME

                    if task_type in task_category[title]:
                        task_category[title][task_type] += 1
                    else:
                        task_category[title][task_type] = 1

    return task_logs, task_category


def change_msg_to_db(messages, logs_db_dict, category_db_dict, year_db=False):
    """Filter parent messages from all messages and update logs and category database"""
    for msg in messages:
        if Config.CHILDREN_USER_FLAG not in msg and 'user' in msg:
            text = msg['text']
            task_logs, task_category = parse_tasks(text)

            if task_logs:
                ymd = datetime.fromtimestamp(float(msg['ts'])).strftime("%Y%m%d")
                year, month, date = ymd[:4], ymd[4:6], ymd[6:]

                if year_db:
                    logs_db = logs_db_dict
                    category_db = category_db_dict
                else:
                    logs_db = logs_db_dict[year]
                    category_db = category_db_dict[year]

                user_id = msg['user']
                user_name = change_id_to_name(user_id)
                user = user_name if user_name else user_id

                if date not in logs_db[user][month]:
                    logs_db[user][month][date] = task_logs
                    category_db[user][month][date] = task_category
