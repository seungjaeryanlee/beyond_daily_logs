#_*_ coding: utf-8 _*_
from flask import Flask
import os
import json
import pickle
from pprint import pprint

from utils import nested_dict, get_logs_files, filter_parent_msg

app = Flask(__name__)
app.config.from_object('config.Config')

def init_db():
    """Initilize database from exported data"""
    db = nested_dict()

    # Lode data
    exported_db_path = os.path.join(os.getcwd(), app.config['EXPORTED_DB_DIR'])
    logs_files = get_logs_files(exported_db_path)
    for logs_dir in logs_files.keys():
        for log_file in logs_files[logs_dir]:
            with open(os.path.join(exported_db_path, logs_dir, log_file), 'rb') as f:
                logs_msgs = json.load(f)
                filter_parent_msg(logs_msgs, db)

    # Save data
    db_path = os.path.join(os.getcwd(), app.config['DB_DIR'])
    for year in db.keys():
        with open(os.path.join(db_path, year + '.pkl'), 'wb') as f:
            pickle.dump(db[year], f, protocol=pickle.HIGHEST_PROTOCOL)

## It will be modified
def read_db():
    """Read data"""
    db_path = os.path.join(os.getcwd(), app.config['DB_DIR'])
    logs_files = os.listdir(db_path)
    db = []
    for logs_file in sorted(logs_files):
        with open(os.path.join(db_path, logs_file), 'rb') as f:
            db.append(pickle.load(f))
    return db


@app.route('/')
def index():
    return "Beyond daily logs"

if __name__ == "__main__":
    init_db()
    db = read_db()
    app.run()
