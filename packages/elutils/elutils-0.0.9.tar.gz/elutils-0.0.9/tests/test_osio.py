from elutils.osio import *
import unittest
import  os


class TestOsIO(unittest.TestCase):
    test_json_file_name = 'test_json.json'
    test_dictionary_content = {"integer":123, "bool":True}

    def setUp(self) -> None:
        '''Remove files created by tests'''
        os.remove(TestOsIO.test_json_file_name)

    def test_write_json(self):
        d = TestOsIO.test_dictionary_content
        write_json(dictionary=d,filepath=TestOsIO.test_json_file_name)

        self.assertTrue(os.path.exists(TestOsIO.test_json_file_name))
        with open(TestOsIO.test_json_file_name,'r') as file:
            opend_d= json.load(file)
        self.assertEqual(d,opend_d)

    def test_read_json(self):
        d = read_json(TestOsIO.test_json_file_name)
        self.assertIsInstance(d,dict)
        self.assertEqual(d, TestOsIO.test_dictionary_content)

    def test_update_json(self):
        q = {"money":0}
        before_update_dict = read_json(TestOsIO.test_json_file_name)
        updated_dict = update_json(q,TestOsIO.test_json_file_name)
        q.update(before_update_dict)
        self.assertEqual(updated_dict,q)