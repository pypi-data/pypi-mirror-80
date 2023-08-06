__author__ = 'Milo Utsch'
__version__ = '0.1.0'
__all__ = [
    'iterable_to_tuple',
    'get_default'
]

import typing as tp


def iterable_to_tuple(iterable: tp.Iterable[tp.Any]) -> tuple:
    """Transforms a iterable to tuple.
    
    :param iterable: Iterable to transformed to tuple.
    :type iterable: ``iterable`` of ``any``
    :return: Tuple transformed from iterable.
    :rtype: ``tuple``
    """
    return tuple(iterable)


def get_default(dictionary: tp.Dict[str, tp.Any], key: str, default: tp.Any) -> tp.Any:
    """Tries to retrieve a value from a dictionary and returns a default value if it does not exist.
    
    :param dictionary: Dictionary to be searched for key.
    :type dictionary: ``dict`` from ``str`` to ``any``
    :param key: Key to be searched in the dictionary.
    :type key: ``str``
    :param default: Value to default to when key not found.
    :type default: ``any``
    :return: Value for key on the dictionary or the default.
    :rtype: ``any``
    """
    return dictionary.get(key, default)

