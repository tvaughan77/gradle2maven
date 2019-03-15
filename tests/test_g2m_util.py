import unittest
from g2m_util import load_file, get_root_level_gradle_file
from tests import gradle_files

class TestG2MUtil(unittest.TestCase):

    def test_load_file(self):
        tuple = ('./tests/my-fake-project', 'foo.txt')
        self.assertEqual(['a\n', 'b\n', 'c\n'], load_file(tuple))


    def test_get_root_level_gradle_file(self):
        self.assertEqual(gradle_files[0], get_root_level_gradle_file(gradle_files))
