import unittest
from mwapi import CollegiateApi, ThesaurusApi, LearnersApi


class MWbaseTestCase(unittest.TestCase):
    def setUp(self):
        """Initializes the instance of MWapi"""
        pass


class CollegiateTests(MWbaseTestCase):
    def setUp(self):
        self.mwapi = CollegiateApi("08a56188-ee0a-46cb-a456-4780ace154df")

    def test_build_url(self):
        word = "python"
        expected_url = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml/%s?key=08a56188-ee0a-46cb-a456-4780ace154df" % word
        url = self.mwapi.build_url(word)
        self.assertEqual(expected_url, url)

    def test_lookup(self):
        word = self.mwapi.lookup("protocol")
        self.assertEqual("protocol", word["word"])

    def test_attribute_parsing(self):
        word = self.mwapi.lookup("protocol")
        expected_def = ":a preliminary memorandum often formulated and signed by diplomatic negotiators as a basis for a final convention or treaty"
        self.assertEqual(expected_def, word['definitions'][1])

    def test_word_not_found(self):
        with self.assertRaises(ValueError) as e:
            _ = self.mwapi.lookup("protoco")
        self.assertTrue(str(e.exception).startswith("Word Not Found. Do you mean"))

    def test_invalid_apikey(self):
        self.mwapi.apikey = "22abc"
        with self.assertRaises(ValueError) as e:
            _ = self.mwapi.lookup("protocol")
        self.assertEqual(str(e.exception), "Invalid API Key")

class ThesaurusTests(MWbaseTestCase):
    def setUp(self):
        self.mwapi = ThesaurusApi("3a554019-ce58-4a54-99e5-d1754a6c098c")

    def test_build_url(self):
        word = "python"
        expected_url = "http://www.dictionaryapi.com/api/v1/references/thesaurus/xml/%s?key=3a554019-ce58-4a54-99e5-d1754a6c098c" % word
        self.assertEqual(expected_url, self.mwapi.build_url(word))

    def test_lookup(self):
        word = self.mwapi.lookup("preclude")
        self.assertEqual('preclude', word['word'])
        self.assertEqual(1, len(word['senses']))
        self.assertEqual('verb', word['functional_label'])

class LearnerApiTests(MWbaseTestCase):
    def setUp(self):
        self.mwapi = LearnersApi("c3b787ec-8c72-47b5-b3f5-ae989507735d")

    def test_build_url(self):
        word = "python"
        expected_url = "http://www.dictionaryapi.com/api/v1/references/learners/xml/%s?key=c3b787ec-8c72-47b5-b3f5-ae989507735d" % word
        self.assertEqual(expected_url, self.mwapi.build_url(word))

    def test_lookup(self):
        word = self.mwapi.lookup("protocol")
        self.assertEqual('protocol', word['word'])
        self.assertEqual('noun', word['functional_label'])
        self.assertEqual(4, len(word['senses']))
        self.assertEqual(':a plan for a scientific experiment or for medical treatment', word['senses'][1]['definition'])
        self.assertEqual(2, len(word['senses'][1]['examples']))


if __name__ == '__main__':
    unittest.main()
