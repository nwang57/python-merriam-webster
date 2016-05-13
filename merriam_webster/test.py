import unittest
from mwapi import CollegiateApi


class MWbaseTestCase(unittest.TestCase):
    def setUp(self):
        """Initializes the instance of MWapi"""
        self.mwapi = CollegiateApi("08a56188-ee0a-46cb-a456-4780ace154df")


class CollegiateTests(MWbaseTestCase):
    def test_build_url(self):
        word = "python"
        expected_url = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml/%s?key=08a56188-ee0a-46cb-a456-4780ace154df" % word
        url = self.mwapi.build_url(word)
        self.assertEqual(expected_url, url)

    def test_lookup(self):
        word_gen = self.mwapi.lookup("protocol")
        word_list = list(word_gen)
        self.assertEqual(2, len(word_list))

    def test_attribute_parsing(self):
        word_gen = self.mwapi.lookup("protocol")
        word_list = list(word_gen)
        self.assertEqual(2, len(word_list))
        word = word_list[0]
        expected_def = ":a preliminary memorandum often formulated and signed by negotiators as a basis for a final convention or treaty"
        self.assertEqual(expected_def, word['definitions'][1])

    def test_word_not_found(self):
        with self.assertRaises(ValueError) as e:
            _ = self.mwapi.lookup("protoco")
        self.assertTrue(str(e.exception).startswith("Word Not Found. Do you mean"))

    def test_invalid_apikey(self):
        self.mwapi.apikey = "22abc"
        print(self.mwapi.build_url("wtx"))
        with self.assertRaises(ValueError) as e:
            _ = self.mwapi.lookup("protocol")
        self.assertEqual(str(e.exception), "Invalid API Key")



if __name__ == '__main__':
    unittest.main()
