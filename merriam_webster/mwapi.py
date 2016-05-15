import requests
import re
from abc import ABCMeta, abstractproperty
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class MWwrapper:

    __metaclass__ = ABCMeta

    def __init__(self, key):
        self.apikey = key

    @abstractproperty
    def base_url():
        """The api endpoint"""
        pass

    def build_url(self, word):
        """Return the request url for a given word"""
        if self.apikey is None:
            raise ValueError("Absence of API key")
        qstring = "%s?key=%s" % (word, self.apikey)
        return self.base_url + qstring

    def _flatten_tree(self, root, exclude=None):
        """return the text of the root by excluding some tags. Only flatten one level"""
        res = [root.text.strip()]
        for node in root:
            if not exclude or node.tag not in exclude:
                res.append(node.text.strip())
            if node.tail:
                res.append(node.tail.strip())
        return " ".join(res).strip()

    def _parse_reponse(self, response):
        try:
            root = ET.fromstring(response.content)
        except ET.ParseError as e:
            if re.search("Invalid API key", response.content.decode("utf-8")):
                raise ValueError("Invalid API Key")
            else:
                raise e
        return root

    def _check_word_found(self, root):
        suggestion_tags = root.findall('suggestion')
        if suggestion_tags:
            suggestions = [s.text for s in suggestion_tags]
            raise ValueError("Word Not Found. Do you mean %s" % suggestions)


class CollegiateApi(MWwrapper):

    base_url = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml/"

    def __init__(self, key):
        super().__init__(key)

    def lookup(self, word):
        """look up the word"""
        url = self.build_url(word)
        response = requests.get(url)
        root = self._parse_reponse(response)
        self._check_word_found(root)
        return self.parse_xml(root, word)

    def parse_xml(self, root, word):
        """Only parse the matched word profile"""
        for entry in root.findall('entry'):
            if entry.find('ew').text == word:
                params = {}
                params['word'] = entry.find('ew').text
                params['functional_label'] = getattr(entry.find('fl'), 'text', None)
                params['definitions'] = self._get_definitions(entry)
                sound = entry.find('sound')
                if sound:
                    params['sound_lists'] = [s.text for s in sound]
                return params

    def _get_definitions(self, entry):
        df_tags = entry.find('def').findall('dt')
        return [self._flatten_tree(d, exclude=['vi','sx']) for d in df_tags]


class ThesaurusApi(MWwrapper):

    base_url = "http://www.dictionaryapi.com/api/v1/references/thesaurus/xml/"

    def __init__(self, key):
        super().__init__(key)

    def lookup(self, word):
        url = self.build_url(word)
        response = requests.get(url)
        root = self._parse_reponse(response)
        self._check_word_found(root)
        return self.parse_xml(root, word)

    def parse_xml(self, root, word):
        """Only return the matched word profile"""
        for entry in root.findall("entry"):
            term = entry.find('term')
            if term.find('hw').text == word:
                params= {}
                params['word'] = word
                params['functional_label'] = getattr(entry.find('fl'), 'text', None)
                params['senses'] = self._get_sense(entry)
                return params

    def _get_sense(self, entry):
        senses = []
        for sense_tag in entry.findall('sens'):
            sense_dict = {}
            sense_dict['meaning'] = self._flatten_tree(sense_tag.find('mc'))
            sense_dict['example'] = self._flatten_tree(sense_tag.find('vi'))
            senses.append(sense_dict)
        return senses

class LearnersApi(MWwrapper):

    base_url = "http://www.dictionaryapi.com/api/v1/references/learners/xml/"

    def __init__(self, key):
        super().__init__(key)

    def lookup(self, word):
        url = self.build_url(word)
        response = requests.get(url)
        root = self._parse_reponse(response)
        self._check_word_found(root)
        return self.parse_xml(root, word)

    def parse_xml(self, root, word):
        for entry in root.findall("entry"):
            if entry and entry.attrib['id'] == word:
                params = {}
                params["word"] = word
                params["functional_label"] = getattr(entry.find('fl'), 'text', None)
                params["senses"] = self._get_senses(entry)
                return params

    def _get_senses(self, entry):
        senses = []
        def_tag = entry.find("def")
        if not def_tag:
            return senses
        for dt_tag in def_tag.findall("dt"):
            sense = {}
            sense['definition'] = dt_tag.text.strip()
            sense['examples'] = self._get_examples(dt_tag)
            senses.append(sense)
        return senses

    def _get_examples(self, dt_tag):
        vi_tags = dt_tag.findall('vi')
        return [self._flatten_tree(vi) for vi in vi_tags]
