import datetime
import os
from pathlib import Path

from kolibri.logger import get_logger
from kolibri.metadata import Metadata
from kolibri.utils import create_dir
from kolibri.utils import module_path_from_object

logger = get_logger(__name__)


def persist_kolibri_model(path, pipeline, fixed_model_name=None):
    """Persist all components of the pipeline to the passed path.

    Returns the directory of the persisted model."""

    timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    metadata = {
        "pipeline": [],
    }

    if fixed_model_name:
        model_name = fixed_model_name
    else:
        model_name = "model_" + timestamp

    path = Path(path).resolve()
    dir_name = os.path.join(path, model_name)

    create_dir(dir_name)

    #        if self.training_data:
    #            metadata.update(self.training_data.persist(dir_name))

    for component in pipeline.components:
        update = component[1].persist(dir_name)
        component_meta = component[1].component_config
        if update:
            component_meta.update(update)
        component_meta["label"] = module_path_from_object(component[1])

        metadata["pipeline"].append(component_meta)

    Metadata(metadata, dir_name).persist(dir_name)

    logger.info("Successfully saved model into "
                "'{}'".format(os.path.abspath(dir_name)))
    return dir_name
