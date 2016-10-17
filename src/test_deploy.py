__author__ = 'teemu kanstren'

import deploy
import unittest
import sys

#http://stackoverflow.com/questions/11380413/python-unittest-passing-arguments

class DeploymentTests(unittest.TestCase):
    USERNAME = "t_e_e_m_u"
    PASSWORD = "==katesc.com=="

    def setUp(self):
        pass


    def test_single_file(self):
        error, args, config = deploy.parse_args(["-c", "test_data/test_config_deploy.ini", "-u", self.USERNAME, "-p", self.PASSWORD, "single_file"])
        deploy.deploy(args, config)


    def test_two_files(self):
        error, args, config = deploy.parse_args(["-c", "test_data/test_config_deploy.ini", "-u", self.USERNAME, "-p", self.PASSWORD, "two_files"])
        deploy.deploy(args, config)


    def test_full_dir(self):
        error, args, config = deploy.parse_args(["-c", "test_data/test_config_deploy.ini", "-u", self.USERNAME, "-p", self.PASSWORD, "full_dir"])
        deploy.deploy(args, config)


    def test_prefixed(self):
        error, args, config = deploy.parse_args(["-c", "test_data/test_config_deploy.ini", "-u", self.USERNAME, "-p", self.PASSWORD, "prefixed"])
        deploy.deploy(args, config)


    def test_nomatch(self):
        error, args, config = deploy.parse_args(["-c", "test_data/test_config_deploy.ini", "-u", self.USERNAME, "-p", self.PASSWORD, "no_match"])
        deploy.deploy(args, config)


    def test_group_of_2(self):
        error, args, config = deploy.parse_args(["-c", "test_data/test_config_deploy.ini", "-u", self.USERNAME, "-p", self.PASSWORD, "group_of_2"])
        deploy.deploy(args, config)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        DeploymentTests.PASSWORD = sys.argv.pop()
        DeploymentTests.USERNAME = sys.argv.pop()
    unittest.main()

