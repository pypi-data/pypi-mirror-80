from kolibri import Component
from kolibri.preprocess.text.scripts.cleaning_scripts import clean_email


class EmailCleaner(Component):
    name = "email_cleaner"

    provides = ["clean"]

    def train(self, training_data, config, **kwargs):

        for example in training_data.training_examples:
            example.clean = self.clean(example.text)

    def process(self, document, **kwargs):

        document.clean = self.clean(document.text)

    def clean(self, text):
        cleaned = clean_email(text)
        return cleaned

