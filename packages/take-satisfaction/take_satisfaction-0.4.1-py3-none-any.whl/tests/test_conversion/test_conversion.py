__author__ = 'Milo Utsch'
__version__ = '0.2.2'

import emoji
import pandas as pd
import pytest

from take_satisfaction.conversion import *
from take_satisfaction.custom_exceptions import *


def test_convert_emojis():
    input_string = '😢'
    converted_string = emoji.demojize(input_string)
    
    assert converted_string not in emoji.UNICODE_EMOJI


def test_verify_answer_type_is_numeric_from_str():
    mock_df = pd.DataFrame([{'Action': '0', 'qtd': 200},
                            {'Action': '1', 'qtd': 160}
                            ])
    mock_column = 'Action'
    
    result = verify_answer_is_numeric(mock_df, mock_column)
    
    assert result


def test_verify_answer_type_is_numeric_from_int():
    mock_df = pd.DataFrame([{'Action': 0, 'qtd': 200},
                            {'Action': 1, 'qtd': 160}
                            ])
    mock_column = 'Action'
    
    result = verify_answer_is_numeric(mock_df, mock_column)
    
    assert result


def test_verify_answer_type_is_numeric_fail():
    mock_df = pd.DataFrame([{'Action': 'Nao Ajudou', 'qtd': 200},
                            {'Action': 'Ajudou', 'qtd': 160}
                            ])
    mock_column = 'Action'
    
    result = verify_answer_is_numeric(mock_df, mock_column)
    
    assert not result


def test_convert_numeric_answer_column():
    mock_df = pd.DataFrame([{'Action': '0', 'qtd': 200},
                            {'Action': '1', 'qtd': 160}
                            ])
    mock_column = 'Action'
    
    result = convert_numeric_answer_column(mock_df, mock_column)
    
    expected_result = pd.DataFrame([{'Action': 0, 'qtd': 200},
                                    {'Action': 1, 'qtd': 160}
                                    ])
    
    pd.testing.assert_frame_equal(result, expected_result)


def test_find_answer_match():
    mock_answer = 'Nao Ajudou'
    mock_scale_translations = [
        'Pessimo',
        'Nao Ajudou',
        'Neuro',
        'Ajudou',
        'Amei'
    ]
    mock_similarity_threshold = 83
    
    result = convert_answer(mock_answer, mock_scale_translations, mock_similarity_threshold)
    
    expected_result = 1
    
    assert result is expected_result
    
    
def test_convert_scale_to_indexes():
    mock_df = pd.DataFrame([{'Action': 'Nao Ajudou', 'qtd': 200},
                            {'Action': 'Ajudou', 'qtd': 160}
                            ])
    mock_column = 'Action'
    mock_scale_translations = [
        'Pessimo',
        'Nao Ajudou',
        'Neuro',
        'Ajudou',
        'Amei'
    ]
    mock_similarity_threshold = 83
    
    result = convert_scale_to_indexes(mock_df, mock_column, mock_scale_translations, mock_similarity_threshold)
    
    expected_result = pd.DataFrame(
        [{'Action': 1, 'qtd': 200},
         {'Action': 3, 'qtd': 160}]
    )

    pd.testing.assert_frame_equal(result, expected_result)


def test_convert_scale_expressions():
    mock_df = pd.DataFrame([{'Action': 'Nao Ajudou', 'qtd': 200},
                            {'Action': 'Ajudou', 'qtd': 160}
                            ])
    mock_column = 'Action'
    mock_scale_translations = [
        'Pessimo',
        'Nao Ajudou',
        'Neuro',
        'Ajudou',
        'Amei'
    ]
    mock_similarity_threshold = 83

    result = convert_scale(mock_df, mock_column, mock_scale_translations, mock_similarity_threshold)

    expected_result = pd.DataFrame(
        [{'Action': 0, 'qtd': 200},
         {'Action': 1, 'qtd': 160}]
    )

    pd.testing.assert_frame_equal(result, expected_result)
    
    
def test_convert_scale_integers_from_str():
    mock_df = pd.DataFrame([{'Action': '1', 'qtd': 200},
                            {'Action': '0', 'qtd': 160}
                            ])
    mock_column = 'Action'
    mock_scale_translations = [
        'Pessimo',
        'Nao Ajudou',
        'Neuro',
        'Ajudou',
        'Amei'
    ]
    mock_similarity_threshold = 83

    result = convert_scale(mock_df, mock_column, mock_scale_translations, mock_similarity_threshold)

    expected_result = pd.DataFrame(
        [{'Action': 0, 'qtd': 160},
         {'Action': 1, 'qtd': 200}]
    )

    pd.testing.assert_frame_equal(result, expected_result)
    
    
def test_convert_scale_integers():
    mock_df = pd.DataFrame([{'Action': 1, 'qtd': 200},
                            {'Action': 0, 'qtd': 160}
                            ])
    mock_column = 'Action'
    mock_scale_translations = [
        'Pessimo',
        'Nao Ajudou',
        'Neuro',
        'Ajudou',
        'Amei'
    ]
    mock_similarity_threshold = 83

    result = convert_scale(mock_df, mock_column, mock_scale_translations, mock_similarity_threshold)

    expected_result = pd.DataFrame(
        [{'Action': 0, 'qtd': 160},
         {'Action': 1, 'qtd': 200}]
    )

    pd.testing.assert_frame_equal(result, expected_result)


def test_convert_scale_empty_df():
    mock_df = pd.DataFrame(columns=['Action', 'qtd'])
    mock_similarity = 85
    mock_column = 'Action'
    mock_scale_translations = [
        'Pessimo',
        'Nao Ajudou',
        'Neuro',
        'Ajudou',
        'Amei'
    ]
    
    with pytest.raises(InvalidDataframeError, match='Cannot process empty scale'):
        convert_scale(mock_df, mock_column, mock_scale_translations, mock_similarity)


def test_convert_scale_missing_column():
    mock_df = pd.DataFrame(
        [{'qtd': 200},
         {'qtd': 160}]
    )
    mock_similarity = 85
    mock_column = 'Action'
    mock_scale_translations = [
        'Pessimo',
        'Nao Ajudou',
        'Neuro',
        'Ajudou',
        'Amei'
    ]
    
    with pytest.raises(AbsentColumnError, match=r'.*Scale does not contain answer column.*'):
        convert_scale(mock_df, mock_column, mock_scale_translations, mock_similarity)


def test_convert_scale_no_suitable_translation():
    mock_df = pd.DataFrame([{'Action': 'Nao Ajudou', 'qtd': 200},
                            {'Action': 'Ajudou', 'qtd': 160}
                            ])
    mock_column = 'Action'
    mock_scale_translations = [
        'Pessimo',
        'Neuro',
        'Amei'
    ]
    mock_similarity = 83
    
    with pytest.raises(NoSuitableTranslationError, match=r'.*Scale not found for *'):
        convert_scale(mock_df, mock_column, mock_scale_translations, mock_similarity)
