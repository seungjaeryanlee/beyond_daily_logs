from app import app
import unittest

class BasicTestCode(unittest.TestCase):

    def text_index(self):
        tester = app.test_client(self)
        resp = tester.get('/', content_type='html/text')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, b'Beyond daily logs')


if __name__ == "__main__":
    unittest.main()
