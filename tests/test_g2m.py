import unittest
from g2m import find_gradle_files
from tests import gradle_files


class TestG2M(unittest.TestCase):

    def test_find_gradle_files(self):
        found_files = find_gradle_files(".")
        self.assertEqual(gradle_files, found_files)
