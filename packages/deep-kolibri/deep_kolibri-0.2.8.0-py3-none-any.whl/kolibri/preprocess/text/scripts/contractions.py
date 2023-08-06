import json
import os

from tensorflow.keras.utils import get_file
from textsearch import TextSearch

from kolibri import settings as k
from kolibri.logger import get_logger

logger = get_logger(__name__)


class Contractions():
    PACKAGE = 'contractions'
    URL_MODEL = "https://www.dropbox.com/s/crpedl7j1z4qamg/contractions.tar.gz?dl=1"

    def __init__(self, language='en', user_generatesd=False, slang=False):
        """
        :param with_additional_file: Allows to load LEFFF without the additional file. (Default: True)
        :type with_additional_file: bool
        :param load_only_pos: Allows to load LEFFF with only some pos tags: WordNet pos tags [a, r, n, v]. (Default: all)
        :type load_only_pos: list
        """
        #        data_file_path = os.path.dirname(os.path.realpath(__file__))

        self.contraction_path = get_file(self.PACKAGE,
                                         self.URL_MODEL,
                                         cache_dir=k.DATA_PATH,
                                         cache_subdir='corpora',
                                         untar=True)
        with open(os.path.join(self.contraction_path, language, 'regular.json'), 'rb') as contraction_file:
            buffer = contraction_file.read()
            buffer = buffer.decode('ascii')
            self.regular_dict = json.loads(buffer)
        with open(os.path.join(self.contraction_path, language, 'user_generated.json'), 'rb') as contraction_file:
            buffer = contraction_file.read()
            buffer = buffer.decode('ascii')
            self.user_generated_dict = json.loads(buffer)
        with open(os.path.join(self.contraction_path, language, 'slang.json'), 'rb') as contraction_file:
            buffer = contraction_file.read()
            buffer = buffer.decode('ascii')
            self.slang_dict = json.loads(buffer)

        self.ts = TextSearch("ignore", "norm")
        self.ts.add(self.regular_dict)

        if user_generatesd:
            self.ts.add(self.user_generated_dict)
        if slang:
            self.ts.add(self.slang_dict)

    def fix(self, s):
        return self.ts.replace(s)

    def add_dic(self, dictionary):
        self.ts.add(dictionary)

    def add_kv(self, key, value):
        self.ts.add(key, value)


c = Contractions()
