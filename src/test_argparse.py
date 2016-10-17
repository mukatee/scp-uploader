__author__ = 'teemu kanstren'

import deploy
import unittest

class ArgParserTests(unittest.TestCase):
    def setUp(self):
        pass


    def test_username_nopass(self):
        error, args, config = deploy.parse_args(["-u", "bob"])
        self.assertEqual('You need to specify either -l/--list or both -u/--username and -p/--password', error)


    def test_pass_nousername(self):
        error, args, config = deploy.parse_args(["-p", "mypass"])
        self.assertEqual('You need to specify either -l/--list or both -u/--username and -p/--password', error)


    def test_noargs(self):
        error, args, config = deploy.parse_args([])
        self.assertEqual('You need to specify either -l/--list or both -u/--username and -p/--password', error)


    def test_invalid_configfile(self):
        error, args, config = deploy.parse_args(["-c", "missing_file", "-l"])
        self.assertEqual("Unable to read content from config file 'missing_file'", error)


    def test_list_configfile(self):
        error, args, config = deploy.parse_args(["-c", "test_data/test_config.ini", "-l"])
        self.assertEqual("Targets found for 'test_data/test_config.ini': ['component1', 'component2', 'component3', 'component4', 'component5', 'component6', 'component7', 'component8', 'group1', 'group2', 'group3', 'group4', 'group5', 'group6', 'group7']", error)


    def test_no_target(self):
        error, args, config = deploy.parse_args(["-c", "test_data/test_config.ini", "-u", "bob", "-p", "mypass"])
        self.assertEqual("No deployment target specified. Doing nothing.", error)


    def test_user_pass_target(self):
        error, args, config = deploy.parse_args(["-c", "test_data/test_config.ini", "-u", "bob", "-p", "mypass", "all"])
        self.assertIsNone(error)
        self.assertEqual("test_data/test_config.ini", args.configfile)
        self.assertEqual("all", args.target)
        self.assertEqual("mypass", args.password)
        self.assertEqual("bob", args.username)



if __name__ == '__main__':
    unittest.main()

