import numbers

import numpy as np


# pylint: disable=invalid-unary-operand-type
def pad_sentences(
        sequences: np.ndarray, max_length: int = None, padding_value: int = 0, padding_style="post"
) -> np.ndarray:
    """
    Pad input sequences up to max_length
    values are aligned to the right

    Args:
        sequences (iter): a 2D matrix (np.array) to pad
        max_length (int, optional): max length of resulting sequences
        padding_value (int, optional): padding value
        padding_style (str, optional): add padding values as prefix (use with 'pre')
            or postfix (use with 'post')

    Returns:
        input sequences padded to size 'max_length'
    """
    if isinstance(sequences, list) and len(sequences) > 0:
        try:
            sequences = np.asarray(sequences)
        except ValueError:
            print("cannot convert sequences into numpy array")
    assert hasattr(sequences, "shape")
    if len(sequences) < 1:
        return sequences
    if max_length is None:
        max_length = np.max([len(s) for s in sequences])
    elif max_length < 1:
        raise ValueError("max sequence length must be > 0")
    if max_length < 1:
        return sequences
    padded_sequences = np.ones((len(sequences), max_length), dtype=np.int32) * padding_value
    for i, sent in enumerate(sequences):
        if padding_style == "post":
            trunc = sent[-max_length:]
            padded_sequences[i, : len(trunc)] = trunc
        elif padding_style == "pre":
            trunc = sent[:max_length]
            padded_sequences[i, -trunc:] = trunc
    return padded_sequences.astype(dtype=np.int32)


def one_hot(mat: np.ndarray, num_classes: int) -> np.ndarray:
    """
    Convert a 1D matrix of ints into one-hot encoded vectors.

    Arguments:
        mat (numpy.ndarray): A 1D matrix of labels (int)
        num_classes (int): Number of all possible classes

    Returns:
        numpy.ndarray: A 2D matrix
    """
    assert len(mat.shape) < 2 or isinstance(mat.shape, int)
    vec = np.zeros((mat.shape[0], num_classes))
    for i, v in enumerate(mat):
        vec[i][v] = 1.0
    return vec


def one_hot_sentence(mat: np.ndarray, num_classes: int) -> np.ndarray:
    """
    Convert a 2D matrix of ints into one-hot encoded 3D matrix

    Arguments:
        mat (numpy.ndarray): A 2D matrix of labels (int)
        num_classes (int): Number of all possible classes

    Returns:
        numpy.ndarray: A 3D matrix
    """
    new_mat = []
    for i in range(mat.shape[0]):
        new_mat.append(one_hot(mat[i], num_classes))
    return np.asarray(new_mat)


def import_module(dotted_path):
    """
    Imports the specified module based on the
    dot notated import path for the module.
    """
    import importlib

    module_parts = dotted_path.split('.')
    module_path = '.'.join(module_parts[:-1])
    module = importlib.import_module(module_path)

    return getattr(module, module_parts[-1])

def initialize_class(data, *args, **kwargs):
    """
    :param data: A string or dictionary containing a import_path attribute.
    """
    if isinstance(data, dict):
        import_path = data.get('import_path')
        data.update(kwargs)
        Class = import_module(import_path)

        return Class(*args, **data)
    else:
        Class = import_module(data)

        return Class(*args, **kwargs)


def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def module_path_from_object(o):
    """Returns the fully qualified class path of the instantiated object."""
    return o.__class__.__module__ + "." + o.__class__.__name__


def check_random_state(seed):
    """Turn seed into a np.random.RandomState instance.

    Parameters
    ----------
    seed : None | int | instance of RandomState
        If seed is None, return the RandomState singleton used by np.random.
        If seed is an int, return a new RandomState instance seeded with seed.
        If seed is already a RandomState instance, return it.
        Otherwise raise ValueError.

    Notes
    -----
    Code from sklearn

    """
    if seed is None or seed is np.random:
        return np.random.mtrand._rand
    if isinstance(seed, (numbers.Integral, np.integer)):
        return np.random.RandomState(seed)
    if isinstance(seed, np.random.RandomState):
        return seed
    raise ValueError('{} cannot be used to seed a numpy.random.RandomState instance'.format(seed))


def class_label_statistics(y):
    unique, counts = np.unique(y, return_counts=True)
    class_stats = dict(zip(unique, counts))

    return sorted(class_stats.items(), key=lambda x: -x[1])
