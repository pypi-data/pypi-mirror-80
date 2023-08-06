__author__ = 'Milo Utsch and Gabriel Salgado'
__version__ = '0.2.4'
__all__ = [
    'verify_answer_is_numeric',
    'convert_numeric_answer_column',
    'convert_answer',
    'convert_scale_to_indexes',
    'convert_scale'
]

import typing as tp

import unidecode as uni
import emoji
import pandas as pd
from fuzzywuzzy import fuzz

from take_satisfaction.custom_exceptions import *

DF = pd.DataFrame
SR = pd.Series


def verify_answer_is_numeric(df: DF, column: str) -> bool:
    """Validates whether the answers in the target column of the df are numeric.
    
    Returns True if the column's items are numeric.
    
    :param df: Dataframe with answers.
    :type df: ``pandas.Dataframe``
    :param column: Column with answers on dataframe.
    :type column: ``str``
    :return: Boolean indicating whether the column is numeric or not.
    :rtype: ``bool``
    """
    return pd.to_numeric(df[column], errors='coerce').notnull().all()


def convert_numeric_answer_column(df: DF, column: str) -> DF:
    """Converts the target column's answers to integers by casting.
    
    :param df: Dataframe with numeric answers.
    :type df: ``pandas.Dataframe``
    :param column: Column with answers on dataframe.
    :type column: ``str``
    :return: Dataframe with the target column's answers converted into integers.
    :rtype: ``pandas.Dataframe``
    """
    df.loc[:, column] = pd.to_numeric(df[column])
    return df


def convert_answer(answer: str, reference: tp.List[str], threshold: int) -> int:
    """Converts answer to the index of its best match on the reference scale.

    Answer is like "Gostei", "Muito ruim"...
    And index range from negative to positive as they appear on the reference.
    Raises an exception if there is no reference similar enough.

    :param answer: String with scale answer.
    :type answer: ``str``
    :param reference: List with answer variations appearing from negative to positive.
    :type reference: ``list`` from ``str``
    :param threshold: Minimum similarity for str matching.
    :type threshold: ``int``
    :return: Index of the best match on the reference scale.
    :rtype: ``int``
    """
    answer = emoji.demojize(answer)
    similarity = [
        (fuzz.ratio(uni.unidecode(answer.lower()), uni.unidecode(value.lower())), idx)
        for idx, value in enumerate(reference)
    ]
    
    max_similarity, position = max(similarity)
    
    if max_similarity >= threshold:
        return position
    raise NoSuitableTranslationError(f'Scale not found for {answer}.')
    

def convert_scale_to_indexes(df: DF, column: str, reference: tp.List[str], threshold: int) -> DF:
    """Converts df column answers to the index of its best match on the reference scale.

    Raises an exception if the conversion fails.

    :param df: Dataframe with answers containing expressions.
    :type df: ``pandas.Dataframe``
    :param reference: List with answer variations appearing from negative to positive.
    :type reference: ``list`` from ``str``
    :param threshold: Minimum similarity for str matching.
    :type threshold: ``int``
    :param column: Column with answers on dataframe.
    :type column: ``str``
    :return: Dataframe with answer column converted to satisfaction level.
    :rtype: ``pandas.Dataframe`
    """
    df_converted_to_matches = df.copy()
    df_converted_to_matches.loc[:, column] = df[column].apply(convert_answer, args=(reference, threshold))
    return df_converted_to_matches


def normalizes_scale_answers(df: DF, column: str) -> DF:
    """Normalizes df column answers to an integer scale with a step of one.
    
    :param df: Dataframe with answers containing expressions.
    :type df: ``pandas.Dataframe``
    :param column: Column with answers on dataframe.
    :type column: ``str``
    :return: Dataframe with answer column converted to satisfaction level.
    :rtype: ``pandas.Dataframe`
    """
    sorted_df = df.sort_values(by=column, axis=0)
    sorted_df.loc[:, column] = [i for i in range(len(sorted_df))]
    return sorted_df
    
    
def validate_conversion_data(df: DF, column: str) -> None:
    """Validates if df is not empty, if it has an answer column and a quantity column.

    :param df: Dataframe with answers.
    :type df: ``pandas.Dataframe``
    :param column: Column with answers on dataframe.
    :type column: ``str```
    """
    if df.empty:
        raise InvalidDataframeError('Cannot process empty scale')
    
    if column not in df.columns:
        raise AbsentColumnError(f'Scale does not contain answer column {column}')


def convert_scale(df: DF, column: str, reference: tp.List[str], threshold: int) -> DF:
    """Converts df column answers to its satisfaction levels.

    :param df: Dataframe with answers.
    :type df: ``pandas.Dataframe``
    :param reference: List with answer variations appearing from negative to positive.
    :type reference: ``list`` from ``str``
    :param threshold: Minimum similarity for str matching.
    :type threshold: ``int``
    :param column: Column with answers on dataframe.
    :type column: ``str``
    :return: Dataframe with answer column converted to satisfaction level.
    :rtype: ``pandas.Dataframe``
    """
    validate_conversion_data(df, column)
    
    if verify_answer_is_numeric(df, column):
        return convert_numeric_answer_column(df, column).sort_values(by=column, axis=0).reset_index(drop=True)
    
    converted_scale = convert_scale_to_indexes(df, column, reference, threshold)
    return normalizes_scale_answers(converted_scale, column)
