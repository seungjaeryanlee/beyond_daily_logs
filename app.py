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

    try:
        with open(logs_db_path, 'rb') as f, open(category_db_path, 'rb') as g:
            logs_db = pickle.load(f)
            category_db = pickle.load(g)
            return logs_db, category_db
    except IOError as e:
        print("Operation failed: %s" %e.strerror)


@app.route('/')
def index():
    """Show daily logs and categorize task"""
    now = datetime.datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    logs_db, category_db = read_db(year)
    user = 'minzy'
    my_logs = logs_db[user][month]
    type_logs = dict()

    for date in sorted(my_logs.keys()):
        tasks = my_logs[date]
        type_logs[date] = []
        for task_type in app.config['TASK_TYPE']:
            if task_type not in tasks.keys():
                tasks[task_type] = []
            type_logs[date].append(tasks[task_type])

    my_cate = category_db[user][month]
    category_count = nested_dict()

    for cate in my_cate.values():
        intersected_types = set(app.config['TASK_TYPE']) & set(cate.keys())
        for task_type in intersected_types:
            for task_cate in cate[task_type].keys():
                if task_cate in category_count[task_type]:
                    category_count[task_type][task_cate] += cate[task_type][task_cate]
                else:
                    category_count[task_type][task_cate] = cate[task_type][task_cate]
    
    done_cate, todo_cate, pause_cate = dict(), dict(), dict()
    done_cate = category_count[app.config['TASK_TYPE'][0]] 
    todo_cate = category_count[app.config['TASK_TYPE'][1]] 
    pause_cate = category_count[app.config['TASK_TYPE'][2]] 
    
    return render_template('index.html', types=app.config['TASK_TYPE'], type_logs=type_logs, month=month, done_cate=done_cate, todo_cate=todo_cate, pause_cate=pause_cate, category_count=category_count)

if __name__ == "__main__":
#    init_log_db()
    year = datetime.date.today().year
    month = datetime.date.today().month
    logs_db, category_db = read_db(year)
#    print(logs_db.keys())
#    print(logs_db['minzy']['06'])
#    pprint(logs_db)
#    pprint(category_db)
    app.run()
