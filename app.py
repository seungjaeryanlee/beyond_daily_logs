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
    """Initilize database from exported data"""
    db = nested_dict()

    # Lode data
    exported_db_path = os.path.join(os.getcwd(), app.config['EXPORTED_DB_DIR'])
    logs_files = get_logs_files(exported_db_path)
    for logs_dir in logs_files.keys():
        for log_file in logs_files[logs_dir]:
            with open(os.path.join(exported_db_path, logs_dir, log_file), 'rb') as f:
                logs_msgs = json.load(f)
                change_msg_to_db(logs_msgs, db)

    # Save data
    db_path = os.path.join(os.getcwd(), app.config['DB_DIR'], app.config['LOGS_DB'])
    for year in db.keys():
        with open(os.path.join(db_path, year + '.pkl'), 'wb') as f:
            pickle.dump(db[year], f, protocol=pickle.HIGHEST_PROTOCOL)


def read_logs_db(year):
    """Read logs data for year"""
    db_path = os.path.join(os.getcwd(), app.config['DB_DIR'], app.config['LOGS_DB'], str(year) + '.pkl')
    with open(db_path, 'rb') as f:
        db = pickle.load(f)
        return db


@app.route('/')
def index():
    year = datetime.date.today().year
    db = read_logs_db(year)
    my_data = db['minzy']
    return render_template('index.html')

if __name__ == "__main__":
#    init_log_db()
    app.run()
