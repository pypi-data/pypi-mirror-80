__author__ = 'Milo Utsch'
__version__ = '0.1.3'

import pandas as pd

from take_satisfaction.utils import weighted_mean
from take_satisfaction.utils import scale
from take_satisfaction.custom_exceptions import InvalidDataframeError
from take_satisfaction.custom_exceptions import AbsentColumnError

DF = pd.DataFrame
S = pd.Series


def calculate_satisfaction_rate(df: DF, level_column: str, quantities_column: str) -> float:
    """ Calculates the satisfaction rate based on the bot scale.

    :param df: Dataframe with satisfaction levels and its quantities.
    :type df: ``pandas.Dataframe``
    :param level_column: Satisfaction level column.
    :type level_column: ``str``
    :param quantities_column: Satisfaction level quantities column.
    :type quantities_column: ``str``
    :return: Satisfaction rate.
    :rtype: ``float``
    """
    validate_satisfaction_data(df, level_column, quantities_column)
    mean = weighted_mean(df[level_column], df[quantities_column])
    return scale(mean, min(df[level_column]), max(df[level_column]))


def validate_satisfaction_data(df: DF, level_column: str, quantities_column: str) -> None:
    """Validates if df is not empty, if it has an answer column and a quantity column.

    :param df: Dataframe with satisfaction levels and its quantities.
    :type df: ``pandas.Dataframe``
    :param level_column: Satisfaction level column.
    :type level_column: ``str``
    :param quantities_column: Satisfaction level quantities column.
    :type quantities_column: ``str``
    """
    if df.empty:
        raise InvalidDataframeError('Cannot process empty scale')
    
    if level_column not in df.columns:
        raise AbsentColumnError(f'Scale does not contain answer column {level_column}')
    
    if quantities_column not in df.columns:
        raise AbsentColumnError(f'Scale does not contain quantity column {quantities_column}')
