#_*_ coding: utf-8 _*_
from app import app
import unittest
import os
from utils import get_logs_files

class BasicTestCode(unittest.TestCase):

    def text_index(self):
        """Check flask set up correctly"""
        tester = app.test_client(self)
        resp = tester.get('/', content_type='html/text')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, b'Beyond daily logs')

    def test_database(self):
        """Check existance of database"""
        db_path = os.path.join(os.getcwd(), app.config['DB_DIR'])
        tester = os.path.isdir(db_path)
        self.assertTrue(tester)
        tester = os.path.isfile(os.path.join(db_path, app.config['LOGS_DB'], '2017.pkl'))
        self.assertTrue(tester)
        tester = os.path.isfile(os.path.join(db_path, app.config['LOGS_DB'], '2018.pkl'))
        self.assertTrue(tester)
        tester = os.path.isfile(os.path.join(db_path, app.config['USERS_DB']))
        self.assertTrue(tester)

    def test_exported_data(self):
        """Check existance and file extension of exported database"""
        db_path = os.path.join(os.getcwd(), app.config['EXPORTED_DB_DIR'])
        tester = os.path.isdir(db_path)
        self.assertTrue(tester)

        file_names = []
        logs_files = get_logs_files(db_path)
        for files in logs_files.values():
            file_names += files
        for name in file_names:
            self.assertTrue(name.endswith('.json'))


if __name__ == "__main__":
    unittest.main()
