from kolibri.classical.tasks.classification.estimator import Estimator

from kolibri.logger import get_logger

logger = get_logger(__name__)

KOLIBRI_MODEL_FILE_NAME = "classifier_kolibri.pkl"


class SklearnEstimator(Estimator):
    """classifier using the sklearn framework"""

    name = 'sklearn_classifier'

    def __init__(self, component_config=None, classifier=None, indexer=None):
        """Construct a new class classifier using the sklearn framework."""
        super().__init__(component_config=component_config, classifier=classifier, indexer=indexer)

    def fit(self, X, y, X_val=None, y_val=None):

        self.indexer.build_vocab(None, y)
        y = self.indexer.transform(y)
        #        if y_val is not None:
        #            y_val = self.indexer.transform(y_val)

        super(SklearnEstimator, self).fit(X, y)
        if self.component_config['priors-thresolding']:
            self.compute_priors(y)

        if self.sampler:

            Xt, yt = self.sampler.fit_resample(X, y)

            self.clf.fit(Xt, yt)
        else:
            self.clf.fit(X, y)

        if not self.component_config['evaluate_first'] and X_val is not None and y_val is not None:
            self.evaluate(X_val, y_val)
