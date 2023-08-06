from kolibri.dnn.tensorflow.autoencoder import Autoencoder
from kolibri.dnn.tensorflow.autoencoder import Conv1DAutoencoder
from kolibri.dnn.tensorflow.autoencoder import DeepAutoencoder
from kolibri.dnn.tensorflow.autoencoder.variational_autoencoder import VariationalAutoencoder


def get_model(model_type, hyper_parameters=None):
    return {
        'mlp': Autoencoder(hyper_parameters=hyper_parameters),
        'conv': Conv1DAutoencoder(hyper_parameters=hyper_parameters),
        'deep': DeepAutoencoder(hyper_parameters=hyper_parameters),
        'variational': VariationalAutoencoder(hyper_parameters=hyper_parameters)
    }.get(model_type.lower(), None)
