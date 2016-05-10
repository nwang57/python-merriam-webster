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
        self.assertEquals(expected_url, url)

    def test_lookup(self):
        pass

    def parse_response(self):
        pass


if __name__ == '__main__':
    unittest.main()
