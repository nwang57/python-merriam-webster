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
        self.key = key

    @abstractproperty
    def base_url():
        """The api endpoint"""
        pass

    def build_url(self, word):
        """Return the request url for a given word"""
        if self.key is None:
            raise ValueError("Absence of API key")
        qstring = "%s?key=%s" % (word, self.key)
        return self.base_url + qstring


class CollegiateApi(MWwrapper):

    base_url = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml/"

    def __init__(self, key):
        super().__init__(key)

    def lookup(self, word):
        """return a generator of the related words"""
        url = self.build_url(word)
        response = requests.get(url)
        #parse_error_code(response.status_code)
        try:
            root = ET.fromstring(response.content)
        except ET.ParseError:
            if re.search("Invalid API Key", response.content):
                raise ValueError("Invalid API Key")
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
        df_tags = entry.find('def').findall('df')
        return [d.text for d in df_tags]




