#_*_ coding: utf-8 _*_
from app import app
import unittest
import os
from utils import get_logs_files


# TODO Rename 'BasicTestCode' class
class BasicTestCode(unittest.TestCase):

    def text_index(self):
        """Check flask set up correctly"""
        tester = app.test_client(self)
        resp = tester.get('/', content_type='html/text')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, b'Beyond daily logs')

    def test_database_existance(self):
        """Check existance of database"""
        db_path = os.path.join(os.getcwd(), app.config['DB_DIR'])
        self.assertTrue(os.path.isdir(db_path))
        self.assertTrue(os.path.isfile(os.path.join(db_path, app.config['LOGS_DB'], '2017.pkl')))
        self.assertTrue(os.path.isfile(os.path.join(db_path, app.config['LOGS_DB'], '2018.pkl')))
        self.assertTrue(os.path.isfile(os.path.join(db_path, app.config['USERS_DB'])))

    def test_exported_database_existance(self):
        """Check existance of exported database"""
        db_path = os.path.join(os.getcwd(), app.config['EXPORTED_DB_DIR'])
        self.assertTrue(os.path.isdir(db_path))

    def test_exported_database_file_extension(self):
        """Check file extension of exported database"""
        db_path = os.path.join(os.getcwd(), app.config['EXPORTED_DB_DIR'])

        file_names = []
        logs_files = get_logs_files(db_path)
        # TODO Why iterate both logs_files.values() and file_names()?
        for files in logs_files.values():
            file_names += files
        for name in file_names:
            self.assertTrue(name.endswith('.json'))


if __name__ == "__main__":
    unittest.main()
