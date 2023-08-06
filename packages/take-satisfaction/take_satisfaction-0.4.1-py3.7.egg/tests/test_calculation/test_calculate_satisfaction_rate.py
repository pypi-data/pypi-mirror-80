__author__ = 'Milo Utsch'
__version__ = '0.1.2'

import pandas as pd
import pytest

from take_satisfaction.calculation import calculate_satisfaction_rate
from take_satisfaction.custom_exceptions import InvalidDataframeError
from take_satisfaction.custom_exceptions import AbsentColumnError


def test_calculate_satisfaction_rate():
    mock_df = pd.DataFrame([{'Action': 1, 'qtd': 119964},
                            {'Action': 0, 'qtd': 92767}
                            ])
    mock_level_column = 'Action'
    mock_quantities_column = 'qtd'
    
    satisfaction_rate = calculate_satisfaction_rate(mock_df, mock_level_column, mock_quantities_column)
    
    assert isinstance(satisfaction_rate, float)
    assert satisfaction_rate == 0.563923452623266


def test_convert_scale_empty_df():
    mock_df = pd.DataFrame(columns=['Action', 'qtd'])
    mock_level_column = 'Action'
    mock_quantities_column = 'qtd'
    
    with pytest.raises(InvalidDataframeError, match='Cannot process empty scale'):
        calculate_satisfaction_rate(mock_df, mock_level_column, mock_quantities_column)


def test_convert_scale_missing_quantity_column():
    mock_df = pd.DataFrame(
        [{'Action': 1},
         {'Action': 0}]
    )
    mock_level_column = 'Action'
    mock_quantities_column = 'qtd'
    
    with pytest.raises(AbsentColumnError, match=r'.*Scale does not contain quantity column.*'):
        calculate_satisfaction_rate(mock_df, mock_level_column, mock_quantities_column)


def test_convert_scale_missing_answer_column():
    mock_df = pd.DataFrame(
        [{'qtd': 200},
         {'qtd': 160}]
    )
    mock_level_column = 'Action'
    mock_quantities_column = 'qtd'
    
    with pytest.raises(AbsentColumnError, match=r'.*Scale does not contain answer column.*'):
        calculate_satisfaction_rate(mock_df, mock_level_column, mock_quantities_column)
