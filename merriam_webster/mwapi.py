import requests
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
