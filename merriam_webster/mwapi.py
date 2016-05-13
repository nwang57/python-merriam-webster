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
            if not exclude and node.tag not in exclude:
                res.append(node.text.strip())
            if node.tail:
                res.append(node.tail.strip())
        return " ".join(res).strip()


class CollegiateApi(MWwrapper):

    base_url = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml/"

    def __init__(self, key):
        super().__init__(key)

    def lookup(self, word):
        """return a generator of the related words"""
        url = self.build_url(word)
        response = requests.get(url)
        try:
            root = ET.fromstring(response.content)
        except ET.ParseError as e:
            if re.search("Invalid API key", response.content.decode("utf-8")):
                raise ValueError("Invalid API Key")
            else:
                raise e
        suggestion_tags = root.findall('suggestion')
        if suggestion_tags:
            suggestions = [s.text for s in suggestion_tags]
            raise ValueError("Word Not Found. Do you mean %s" % suggestions)
        return self.parse_xml(root)

    def parse_xml(self, root):
        for entry in root.findall('entry'):
            params = {}
            params['word'] = entry.find('ew').text
            params['functional label'] = getattr(entry.find('fl'), 'text', None)
            params['definitions'] = self._get_definitions(entry)
            sound = entry.find('sound')
            if sound:
                params['sound_lists'] = [s.text for s in sound]
            yield params

    def _get_definitions(self, entry):
        df_tags = entry.find('def').findall('dt')
        return [self._flatten_tree(d, exclude=['vi','sx']) for d in df_tags]


