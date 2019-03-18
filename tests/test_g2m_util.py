import unittest
from g2m_util import load_file, get_root_level_gradle_file, get_module_name, get_module_element
from tests import gradle_files


class TestG2MUtil(unittest.TestCase):

    def test_load_file(self):
        gradle_tuple = ('./tests/my-fake-project', 'foo.txt')
        self.assertEqual(['a\n', 'b\n', 'c\n'], load_file(gradle_tuple))

    def test_get_root_level_gradle_file(self):
        self.assertEqual(gradle_files[0], get_root_level_gradle_file(gradle_files))

    def test_get_module_element(self):
        self.assertEqual('sub-project-a',
                         get_module_element(('./tests/my-fake-project/sub-project-a', 'build.gradle')).text)

    def test_get_module_name(self):
        self.assertEqual('sub-project-a',
                         get_module_name(('./tests/my-fake-project/sub-project-a', 'build.gradle')))
