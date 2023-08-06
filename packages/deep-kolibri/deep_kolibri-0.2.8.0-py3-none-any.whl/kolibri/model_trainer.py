from kolibri import kolibri_component
from kolibri.logger import get_logger
from kolibri.model_loader import ModelLoader
from kolibri.persistor import persist_kolibri_model
from kolibri.pipeline import Pipeline

logger = get_logger(__name__)

MINIMUM_COMPATIBLE_VERSION = "0.0.1"


class ModelTrainer(object):
    """Trainer will load the texts and train all components.

    Requires a pipeline specification and configuration to use for
    the training."""

    SUPPORTED_LANGUAGES = ["de", "en"]

    def __init__(self, cfg, component_builder=None, skip_validation=False):

        self.config = cfg
        self.skip_validation = skip_validation
        self.training_data = None

        if component_builder is None:
            # If no builder is passed, every interpreter creation will result in
            # a new builder. hence, no components are reused.
            component_builder = kolibri_component.ComponentBuilder()

        # Before instantiating the component classes, lets check if all
        # required packages are available
        if not self.skip_validation:
            kolibri_component.validate_requirements(cfg.component_names)

        # build pipeline
        self.pipeline = self._build_pipeline(cfg, component_builder)

    @staticmethod
    def _build_pipeline(cfg, component_builder):
        """Transform the passed names of the pipeline components into classes"""

        steps = []
        # Transform the passed names of the pipeline components into classes
        for component_name in cfg.component_names:
            component = component_builder.create_component(
                component_name, cfg)
            steps.append((component_name, component))

        return Pipeline(steps)

    def fit(self, X, y, X_val=None, y_val=None):
        """Trains the underlying pipeline using the provided training texts."""

        self.pipeline.fit(X, y, X_val, y_val)

        return ModelLoader(self.pipeline, {})

    def train(self, data, **kwargs):
        """Trains the underlying pipeline using the provided training texts."""

        self.training_data = data

        context = kwargs

        for component in self.pipeline.components:
            updates = component[1].provide_context()
            if updates:
                context.update(updates)

        self.pipeline.train(data, **kwargs)

        return ModelLoader(self.pipeline, context)

    def persist(self, path, fixed_model_name=None):
        """Persist all components of the pipeline to the passed path.

        Returns the directory of the persisted model."""
        return persist_kolibri_model(path, self.pipeline, fixed_model_name)
