#_*_ coding: utf-8 _*_
from flask import Flask, render_template, url_for
import os
import json
import pickle
import datetime
from pprint import pprint

from utils import nested_dict, get_logs_files, change_msg_to_db

app = Flask(__name__)
app.config.from_object('config.Config')

def init_log_db():
    """Initilize logs and category database from exported data"""
    logs_db = nested_dict()
    category_db = nested_dict()

    # Lode data
    exported_db_path = os.path.join(os.getcwd(), app.config['EXPORTED_DB_DIR'])
    logs_files = get_logs_files(exported_db_path)
    for logs_dir in logs_files.keys():
        for log_file in logs_files[logs_dir]:
            with open(os.path.join(exported_db_path, logs_dir, log_file), 'rb') as f:
                logs_msgs = json.load(f)
                change_msg_to_db(logs_msgs, logs_db, category_db)

    # Save data
    db_path = os.path.join(os.getcwd(), app.config['DB_DIR'], app.config['LOGS_DB'])
    for year in logs_db.keys():
        with open(os.path.join(db_path, year + '.pkl'), 'wb') as f:
            pickle.dump(logs_db[year], f, protocol=pickle.HIGHEST_PROTOCOL)
        with open(os.path.join(db_path, year + '_category.pkl'), 'wb') as g:
            pickle.dump(category_db[year], g, protocol=pickle.HIGHEST_PROTOCOL)


def read_db(year):
    """Read data for year"""
    db_path = os.path.join(os.getcwd(), app.config['DB_DIR'], app.config['LOGS_DB'])
    logs_db_path = os.path.join(db_path, str(year) + '.pkl')
    category_db_path = os.path.join(db_path, str(year) + '_category.pkl')

    with open(logs_db_path, 'rb') as f, open(category_db_path, 'rb') as g:
        logs_db = pickle.load(f)
        category_db = pickle.load(g)
        return logs_db, category_db


@app.route('/')
def index():
    year = datetime.date.today().year
    db = read_logs_db(year)
    my_data = db['minzy']
    return render_template('index.html')

if __name__ == "__main__":
#    init_log_db()
    year = datetime.date.today().year
    logs_db, category_db = read_db(year)
    pprint(logs_db)
    pprint(category_db)
#    app.run()
