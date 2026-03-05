import unittest
from main import clean_iota, split_file

class TestCleanIota(unittest.TestCase):
    def test_trim_trailing_whitespace(self):
        self.assertEqual("wawa", clean_iota("wawa   "))

    def test_trim_leading_whitespace(self):
        self.assertEqual("wawa", clean_iota("   wawa"))

    def test_trim_internal_whitespace(self):
        self.assertEqual("wawa", clean_iota("wa  wa"))

    def test_lowercase(self):
        self.assertEqual("wawa", clean_iota("WaWa"))

    def test_trim_apostropha(self):
        self.assertEqual("wawa", clean_iota("wa'wa"))

    def test_all(self):
        self.assertEqual("mindsbingus", clean_iota(" Mind's Bingus \n "))

class TestSplitFile(unittest.TestCase):
    def test_one_pattern(self):
        self.assertEqual(["mindsreflection"], split_file("testdata/single_pattern"))

    def test_pattern_list(self):
        self.assertEqual(["mindsreflection", "compasspurification", "mindsreflection", "alidadespurification", "archersdistillation"], split_file("testdata/pattern_list"))
    def test_one_pattern(self):
        self.assertEqual(["introspection", "mindsreflection", "retrospection"], split_file("testdata/intro_retro_words"))
    def test_one_pattern(self):
        self.assertEqual(["introspection", "mindsreflection", "retrospection"], split_file("testdata/intro_retro_brackets"))



if __name__ == "__main__":
    unittest.main()
