__author__ = 'Moises Mendes'
__version__ = '0.1.1'
__all__ = [
    'format_text'
]

import typing as tp


def format_text(text: str, params: tp.Dict[str, tp.Any]) -> str:
    """Format string replacing placeholders by parameters.

    :param text: Text containing named placeholders.
    :type text: ``str``
    :param params: Parameters to replace placeholders.
    :type params: ``dict`` from ``str`` to ``any``
    :return: Formatted text.
    :rtype: ``str``
    """
    return text.format(**params)
