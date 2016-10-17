__author__ = 'teemu kanstren'

import deploy
import unittest

class FileDataParserTests(unittest.TestCase):
    def setUp(self):
        pass


    def test_component1(self):
        error, args, config = deploy.parse_args(["-c", "test_data/test_config.ini", "-u", "bob", "-p", "mypass", "all"])
        error, files, dirs = deploy.create_file_list(config, "component1", set())
        self.assertEqual("Could not find file starting with 'test_file_1' and ending with '.txt' in path './test_data'. Skipping deployment target 'component1'.", error)
        self.assertIsNone(files)
        self.assertIsNone(dirs)

    def test_component2(self):
        error, args, config = deploy.parse_args(["-c", "test_data/test_config.ini", "-u", "bob", "-p", "mypass", "all"])
        error, files, dirs = deploy.create_file_list(config, "component2", set())
        self.assertIsNone(error)
        dst_ip = "192.168.56.101"
        src_dir = './test_data/'
        dst_dir = '/home/randomguy/testtarget'
        self.assertEqual(0, len(files))
        self.assertEqual(2, len(dirs))
        self.assertEqual(src_dir, dirs[0].src_path)
        self.assertEqual(dst_dir, dirs[0].dst_path)
        self.assertEqual(dst_ip, dirs[0].dst_ip)
        self.assertEqual(22, dirs[0].dst_port)
        self.assertEqual(src_dir, dirs[1].src_path)
        self.assertEqual(dst_dir, dirs[1].dst_path)
        self.assertEqual("service1.target.example", dirs[1].dst_ip)
        self.assertEqual(22, dirs[1].dst_port)

    def test_component3(self):
        error, args, config = deploy.parse_args(["-c", "test_data/test_config.ini", "-u", "bob", "-p", "mypass", "all"])
        error, files, dirs = deploy.create_file_list(config, "component3", set())
        self.assertIsNone(error)
        self.assertEqual(0, len(dirs))
        dst_ip = "192.168.56.102"
        src_dir = './test_data/'
        dst_dir = '/home/randomguy/testtarget'
        self.assertEqual(2, len(files))
        self.assertEqual(src_dir + "file1.txt", files[0].src_path)
        self.assertEqual(dst_dir, files[0].dst_path)
        self.assertEqual(dst_ip, files[0].dst_ip)
        self.assertEqual(22, files[0].dst_port)
        self.assertEqual(src_dir + "file2.txt", files[1].src_path)
        self.assertEqual(dst_dir, files[1].dst_path)
        self.assertEqual(dst_ip, files[1].dst_ip)
        self.assertEqual(22, files[1].dst_port)


    def test_component4(self):
        error, args, config = deploy.parse_args(["-c", "test_data/test_config.ini", "-u", "bob", "-p", "mypass", "all"])
        error, files, dirs = deploy.create_file_list(config, "component4", set())
        self.assertEqual(
            "Could not find file starting with 'file' and ending with 'json' in path './test_data/'. Skipping deployment target 'component4'.",
            error)
        self.assertIsNone(files)
        self.assertIsNone(dirs)

    def test_component5(self):
        error, args, config = deploy.parse_args(["-c", "test_data/test_config.ini", "-u", "bob", "-p", "mypass", "all"])
        error, files, dirs = deploy.create_file_list(config, "component5", set())
        self.assertIsNone(error)
        self.assertEqual(0, len(dirs))
        dst_ip = "192.168.56.101"
        src_dir = './test_data/'
        dst_dir = '/home/randomguy/testtarget/component1'
        self.assertEqual(2, len(files))
        self.assertEqual(src_dir + "file1.txt", files[0].src_path)
        self.assertEqual(dst_dir, files[0].dst_path)
        self.assertEqual(dst_ip, files[0].dst_ip)
        self.assertEqual(src_dir + "hello.xml", files[1].src_path)
        self.assertEqual(dst_dir, files[1].dst_path)
        self.assertEqual(dst_ip, files[1].dst_ip)


    def test_component6(self):
        error, args, config = deploy.parse_args(["-c", "test_data/test_config.ini", "-u", "bob", "-p", "mypass", "all"])
        error, files, dirs = deploy.create_file_list(config, "component6", set())
        self.assertEqual("Target 'component6' specifies both pre/postfix and 'file_names'. Remove one. Skipping target.",
                         error)
        self.assertIsNone(files)


    def test_component7(self):
        error, args, config = deploy.parse_args(["-c", "test_data/test_config.ini", "-u", "bob", "-p", "mypass", "all"])
        error, files, dirs = deploy.create_file_list(config, "component7", set())
        self.assertEqual("Directory './non-existant/' not found (or is not a directory).",
                         error)
        self.assertIsNone(files)
        self.assertIsNone(dirs)


    def test_component8(self):
        error, args, config = deploy.parse_args(["-c", "test_data/test_config.ini", "-u", "bob", "-p", "mypass", "all"])
        error, files, dirs = deploy.create_file_list(config, "component8", set())
        self.assertEqual(
            "Directory '' not found (or is not a directory).",
            error)
        self.assertIsNone(files)
        self.assertIsNone(dirs)


    def test_group1(self):
        error, args, config = deploy.parse_args(["-c", "test_data/test_config.ini", "-u", "bob", "-p", "mypass", "all"])
        error, files, dirs = deploy.create_file_list(config, "group1", set())
        self.assertEqual("Could not find file starting with 'test_file_1' and ending with '.txt' in path './test_data'. Skipping deployment target 'component1'.", error)
        dst_ip = "192.168.56.101"
        src_dir = './test_data/'
        dst_dir = '/home/randomguy/testtarget/component1'
        self.assertEqual(2, len(files))
        self.assertEqual(0, len(dirs))
        self.assertEqual(src_dir + "file1.txt", files[0].src_path)
        self.assertEqual(dst_dir, files[0].dst_path)
        self.assertEqual(dst_ip, files[0].dst_ip)
        self.assertEqual(src_dir + "hello.xml", files[1].src_path)
        self.assertEqual(dst_dir, files[1].dst_path)
        self.assertEqual(dst_ip, files[1].dst_ip)

    def test_group2(self):
        error, args, config = deploy.parse_args(["-c", "test_data/test_config.ini", "-u", "bob", "-p", "mypass", "all"])
        error, files, dirs = deploy.create_file_list(config, "group2", set())
        self.assertEqual("Key 'bad-component1' not found in configuration.",
                         error)
        dst_ip = "192.168.56.101"
        src_dir = './test_data/'
        dst_dir = '/home/randomguy/testtarget/component1'
        self.assertEqual(2, len(files))
        self.assertEqual(0, len(dirs))
        self.assertEqual(src_dir + "file1.txt", files[0].src_path)
        self.assertEqual(dst_dir, files[0].dst_path)
        self.assertEqual(dst_ip, files[0].dst_ip)
        self.assertEqual(src_dir + "hello.xml", files[1].src_path)
        self.assertEqual(dst_dir, files[1].dst_path)
        self.assertEqual(dst_ip, files[1].dst_ip)


    def test_group3(self):
        error, args, config = deploy.parse_args(["-c", "test_data/test_config.ini", "-u", "bob", "-p", "mypass", "all"])
        error, files, dirs = deploy.create_file_list(config, "group3", set())
        self.assertEqual("Key '' not found in configuration.",
                         error)
        dst_ip = "www.kanstren.net"
        src_dir = './test_data/'
        dst_dir = '/home/randomguy/testtarget/component1/'
        self.assertIsNone(files)
        self.assertEqual(0, len(dirs))


    def test_group4(self):
        error, args, config = deploy.parse_args(["-c", "test_data/test_config.ini", "-u", "bob", "-p", "mypass", "all"])
        error, files, dirs = deploy.create_file_list(config, "group4", set())
        self.assertEqual("Could not find file starting with 'test_file_1' and ending with '.txt' in path './test_data'. Skipping deployment target 'component1'.",
                         error)
        dst_ip = "192.168.56.101"
        src_dir = './test_data/'
        dst_dir = '/home/randomguy/testtarget/component1'
        self.assertEqual(2, len(files))
        self.assertEqual(src_dir + "file1.txt", files[0].src_path)
        self.assertEqual(dst_dir, files[0].dst_path)
        self.assertEqual(dst_ip, files[0].dst_ip)
        self.assertEqual(src_dir + "hello.xml", files[1].src_path)
        self.assertEqual(dst_dir, files[1].dst_path)
        self.assertEqual(dst_ip, files[1].dst_ip)
        self.assertEqual(0, len(dirs))


    def test_group5(self):
        error, args, config = deploy.parse_args(["-c", "test_data/test_config.ini", "-u", "bob", "-p", "mypass", "all"])
        files, dirs = deploy.create_total_filelist(config, ["group5"])
        dst_ip = "192.168.56.101"
        src_dir = './test_data/'
        dst_dir = '/home/randomguy/testtarget/component1'
        self.assertEqual(4, len(files))

        self.assertEqual(src_dir + "file1.txt", files[0].src_path)
        self.assertEqual(dst_dir, files[0].dst_path)
        self.assertEqual(dst_ip, files[0].dst_ip)
        self.assertEqual(src_dir + "hello.xml", files[1].src_path)
        self.assertEqual(dst_dir, files[1].dst_path)
        self.assertEqual(dst_ip, files[1].dst_ip)

        dst_ip = "192.168.56.102"
        dst_dir = '/home/randomguy/testtarget'
        self.assertEqual(src_dir + "file1.txt", files[2].src_path)
        self.assertEqual(dst_dir, files[2].dst_path)
        self.assertEqual(dst_ip, files[2].dst_ip)
        self.assertEqual(src_dir + "file2.txt", files[3].src_path)
        self.assertEqual(dst_dir, files[3].dst_path)
        self.assertEqual(dst_ip, files[3].dst_ip)

        dst_ip = "192.168.56.101"
        self.assertEqual(2, len(dirs))
        self.assertEqual(src_dir, dirs[0].src_path)
        self.assertEqual(dst_dir, dirs[0].dst_path)
        self.assertEqual(dst_ip, dirs[0].dst_ip)
        self.assertEqual(22, dirs[0].dst_port)
        self.assertEqual(src_dir, dirs[1].src_path)
        self.assertEqual(dst_dir, dirs[1].dst_path)
        self.assertEqual("service1.target.example", dirs[1].dst_ip)
        self.assertEqual(22, dirs[1].dst_port)

    def test_group6(self):
        error, args, config = deploy.parse_args(["-c", "test_data/test_config.ini", "-u", "bob", "-p", "mypass", "all"])
        files, dirs = deploy.create_total_filelist(config, ["group6"])

        dst_ip = "192.168.56.101"
        src_dir = './test_data/'
        dst_dir = '/home/randomguy/testtarget/component1'
        self.assertEqual(4, len(files))

        self.assertEqual(src_dir + "file1.txt", files[0].src_path)
        self.assertEqual(dst_dir, files[0].dst_path)
        self.assertEqual(dst_ip, files[0].dst_ip)
        self.assertEqual(src_dir + "hello.xml", files[1].src_path)
        self.assertEqual(dst_dir, files[1].dst_path)
        self.assertEqual(dst_ip, files[1].dst_ip)

        dst_ip = "192.168.56.102"
        dst_dir = '/home/randomguy/testtarget'
        self.assertEqual(src_dir + "file1.txt", files[2].src_path)
        self.assertEqual(dst_dir, files[2].dst_path)
        self.assertEqual(dst_ip, files[2].dst_ip)
        self.assertEqual(src_dir + "file2.txt", files[3].src_path)
        self.assertEqual(dst_dir, files[3].dst_path)
        self.assertEqual(dst_ip, files[3].dst_ip)

        dst_ip = "192.168.56.101"
        self.assertEqual(2, len(dirs))
        self.assertEqual(src_dir, dirs[0].src_path)
        self.assertEqual(dst_dir, dirs[0].dst_path)
        self.assertEqual(dst_ip, dirs[0].dst_ip)
        self.assertEqual(22, dirs[0].dst_port)
        self.assertEqual(src_dir, dirs[1].src_path)
        self.assertEqual(dst_dir, dirs[1].dst_path)
        self.assertEqual("service1.target.example", dirs[1].dst_ip)
        self.assertEqual(22, dirs[1].dst_port)

    def test_group7(self):
        error, args, config = deploy.parse_args(["-c", "test_data/test_config.ini", "-u", "bob", "-p", "mypass", "all"])
        files, dirs = deploy.create_total_filelist(config, ["group5"])
        dst_ip = "192.168.56.101"
        src_dir = './test_data/'
        dst_dir = '/home/randomguy/testtarget/component1'
        self.assertEqual(4, len(files))

        self.assertEqual(src_dir + "file1.txt", files[0].src_path)
        self.assertEqual(dst_dir, files[0].dst_path)
        self.assertEqual(dst_ip, files[0].dst_ip)
        self.assertEqual(src_dir + "hello.xml", files[1].src_path)
        self.assertEqual(dst_dir, files[1].dst_path)
        self.assertEqual(dst_ip, files[1].dst_ip)

        dst_ip = "192.168.56.102"
        dst_dir = '/home/randomguy/testtarget'
        self.assertEqual(src_dir + "file1.txt", files[2].src_path)
        self.assertEqual(dst_dir, files[2].dst_path)
        self.assertEqual(dst_ip, files[2].dst_ip)
        self.assertEqual(src_dir + "file2.txt", files[3].src_path)
        self.assertEqual(dst_dir, files[3].dst_path)
        self.assertEqual(dst_ip, files[3].dst_ip)

        dst_ip = "192.168.56.101"
        self.assertEqual(2, len(dirs))

        self.assertEqual(src_dir, dirs[0].src_path)
        self.assertEqual(dst_dir, dirs[0].dst_path)
        self.assertEqual(dst_ip, dirs[0].dst_ip)
        self.assertEqual(22, dirs[0].dst_port)

        self.assertEqual(src_dir, dirs[1].src_path)
        self.assertEqual(dst_dir, dirs[1].dst_path)
        self.assertEqual("service1.target.example", dirs[1].dst_ip)
        self.assertEqual(22, dirs[1].dst_port)

if __name__ == '__main__':
    unittest.main()

