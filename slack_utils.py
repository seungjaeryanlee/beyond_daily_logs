#_*_ coding: utf-8 _*_
from slacker import Slacker
import os
import pickle
import datetime
from slack_token import TOKEN
from config import Config
from utils import change_msg_to_db, nested_dict
from pprint import pprint

def get_channel_id(slack, channel_name):
    """Get channel id"""
    channel_list = slack.channels.list().body['channels']
    for channel in channel_list:
        if channel['name'] == channel_name:
            return channel['id']
    return None


def get_channel_msg(slack, channel_id):
    """Get channel history messages"""
    channel_history = slack.channels.history(channel=channel_id, count=Config.MSG_COUNT).body
    messages = channel_history['messages']
    return messages


def fetch_daily_logs(slack, channel_name):
    """Fetch messages of daily_logs channel"""
    channel_id = get_channel_id(slack, channel_name)
    if channel_id:
        channel_msgs = get_channel_msg(slack, channel_id)
        year = datetime.date.today().year
        logs_db_path = os.path.join(os.getcwd(), Config.DB_DIR, Config.LOGS_DB, str(year) + '.pkl')

        if os.path.exists(logs_db_path) and os.path.getsize(logs_db_path) > 0:
            with open(logs_db_path, 'rb') as f:
                logs_db = pickle.load(f)
                change_msg_to_db(channel_msgs, logs_db, year_db=True)
        else:
            logs_db = nested_dict()
            change_msg_to_db(channel_msgs, logs_db, year_db=True)

        with open(logs_db_path, 'wb') as f:
            pickle.dump(logs_db, f, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        pass

if __name__ == "__main__":
    dfab_slack = Slacker(TOKEN)
    fetch_daily_logs(dfab_slack, Config.LOG_CHANNEL)
