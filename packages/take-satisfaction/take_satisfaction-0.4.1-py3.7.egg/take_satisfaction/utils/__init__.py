__author__ = 'Gabriel Salgado, Juliana Guamá, Milo Utsch, Moises Mendes and Rogers Damas'
__version__ = '0.2.0'

from .load_params import load_params, load_query
from .sparksql_ops import *
from .formatting import format_text
from .iterable_ops import iterable_to_tuple, get_default

from .mathematical_utils import weighted_mean, scale
