__author__ = 'teemu kanstren'

import deploy
import unittest

class FileNameParserTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_jar_none(self):
        error, filename = deploy.find_files_from_list(".", ['john.jar'], "pre_bob", "post_bob")
        self.assertEqual("Could not find file starting with 'pre_bob' and ending with 'post_bob' in path '.'.", error)
        self.assertIsNone(filename)

    def test_single_postfix(self):
        error, filename = deploy.find_files_from_list(".", ['bob.jar'], None, ".jar")
        self.assertIsNone(error)
        self.assertEqual(["bob.jar"], filename)

    def test_two_postfix_mismatch(self):
        error, filename = deploy.find_files_from_list(".", ['bob-1.0.0.jar', 'bob.jar'], None, "bob")
        self.assertEqual("Could not find file ending with 'bob' in path '.'.", error)
        self.assertIsNone(filename)

    def test_many_postfix(self):
        error, filename = deploy.find_files_from_list(".", ['john.jar', 'bob-1.0.0.jar', 'john2.jar'], None, "jar")
        self.assertIsNone(error)
        self.assertEqual(['john.jar', 'bob-1.0.0.jar', 'john2.jar'], filename)

    def test_many_postfix2(self):
        error, filename = deploy.find_files_from_list(".", ['john.jar', 'bob-1.0.0.jar', 'john2.rar'], None, "jar")
        self.assertIsNone(error)
        self.assertEqual(['john.jar', 'bob-1.0.0.jar'], filename)

    def test_single_prefix(self):
        error, filename = deploy.find_files_from_list(".", ['bob-1.0.0.jar'], "bob", None)
        self.assertIsNone(error)
        self.assertEqual(["bob-1.0.0.jar"], filename)

    def test_many_prefix(self):
        error, filename = deploy.find_files_from_list(".", ['john.jar', 'bob-1.0.0.jar', 'john2.jar'], "bob", None)
        self.assertIsNone(error)
        self.assertEqual(["bob-1.0.0.jar"], filename)

    def test_many_prefix2(self):
        error, filename = deploy.find_files_from_list(".", ['john.jar', 'bob-1.0.0.jar', 'john2.jar'], "john", None)
        self.assertIsNone(error)
        self.assertEqual(['john.jar', 'john2.jar'], filename)



if __name__ == '__main__':
    unittest.main()

