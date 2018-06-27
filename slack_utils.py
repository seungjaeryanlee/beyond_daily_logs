#_*_ coding: utf-8 _*_
from slacker import Slacker
import os
import pickle
import datetime
from slack_token import TOKEN
from config import Config
from utils import change_msg_to_db, nested_dict
from pprint import pprint # TODO: Unused import?


def get_channel_id(slack, channel_name):
    """Get channel id"""
    channel_list = slack.channels.list().body['channels']
    for channel in channel_list:
        if channel['name'] == channel_name:
            return channel['id']
    return None


def get_channel_msg(slack, channel_id, num_msg):
    """Get channel history messages"""
    channel_history = slack.channels.history(channel=channel_id, count=num_msg).body
    messages = channel_history['messages']
    return messages

def get_user_map(slack):
    """Get user information and map id and real_name"""
    # TODO: Any reason to use dict() instead of {}?
    users = dict()
    user_list = slack.users.list().body['members']
    for user in user_list:
        if 'real_name' in user:
            users[user['id']] = user['real_name']

    return users


def update_logs_db(slack, channel_name, num_msg):
    """Update logs and category database from daily_logs channel"""
    channel_id = get_channel_id(slack, channel_name)
    if channel_id:
        channel_msgs = get_channel_msg(slack, channel_id, num_msg)
        year = datetime.date.today().year
        db_path = os.path.join(os.getcwd(), Config.DB_DIR, Config.LOGS_DB)
        logs_db_path = os.path.join(db_path, str(year) + '.pkl')
        category_db_path = os.path.join(db_path, str(year) + '_category.pkl')

        if os.path.exists(logs_db_path) and os.path.getsize(logs_db_path) > 0:
            with open(logs_db_path, 'rb') as f, open(category_db_path, 'rb') as g:
                logs_db = pickle.load(f)
                category_db = pickle.load(g)
                change_msg_to_db(channel_msgs, logs_db, category_db, year_db=True)
        else:
            logs_db = nested_dict()
            category_db = nested_dict()
            change_msg_to_db(channel_msgs, logs_db, category_db, year_db=True)

        with open(logs_db_path, 'wb') as f, open(category_db_path, 'wb') as g:
            pickle.dump(logs_db, f, protocol=pickle.HIGHEST_PROTOCOL)
            pickle.dump(category_db, g, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        pass


def update_user_db(slack):
    """Update user database from slack"""
    user_map = get_user_map(slack)
    user_db_path = os.path.join(os.getcwd(), Config.DB_DIR, Config.USERS_DB)
    with open(user_db_path, 'wb') as f:
        pickle.dump(user_map, f, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    dfab_slack = Slacker(TOKEN)
    update_logs_db(dfab_slack, Config.LOG_CHANNEL, Config.MSG_COUNT)
#    update_user_db(dfab_slack)
