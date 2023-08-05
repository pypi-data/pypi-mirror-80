"""
Tokenizer Interface
"""

from kolibri.kolibri_component import Component
from kolibri.stopwords import get_stop_words


class Tokenizer(Component):
    provides = ["tokens"]
    defaults = {
        "filter-stopwords": False,
        "language": 'en',
        "lower-case": False,
        "custom-stopwords": None,
        "add-to-stopwords": None,
        "remove-from-stopwords": None

    }
    def __init__(self, config={}):
        super().__init__(config)
        self.stopwords = None
        self.remove_stopwords = self.component_config["filter-stopwords"]
        if self.remove_stopwords:
            self.stopwords = set(get_stop_words(self.component_config['language']))
            if isinstance(self.component_config["add-to-stopwords"], list):
                self.stopwords=list(self.stopwords)
                self.stopwords.extend(list(self.component_config["add-to-stopwords"]))
                self.stopwords=set(self.stopwords)
            if isinstance(self.component_config["remove-from-stopwords"], list):
                self.stopwords=set([sw for sw in list(self.stopwords) if sw not in self.component_config["remove-from-stopwords"]])
        if isinstance(self.component_config["custom-stopwords"], list):
            self.stopwords=set(self.component_config["custom-stopwords"])
        self.tokenizer = None

    def tokenize(self, text):
        raise NotImplementedError
