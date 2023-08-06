__author__ = 'Milo Utsch'
__version__ = '0.1.3'

import numpy as np
import pandas as pd
import pytest

from take_satisfaction.utils import load_params
from take_satisfaction.preprocess import match_manual
from take_satisfaction.preprocess import remove_manual
from take_satisfaction.custom_exceptions import InvalidDataframeError
from take_satisfaction.custom_exceptions import AbsentColumnError


def test_get_manual_entries_success_two_items():
    mock_df = pd.DataFrame(
        [{'Action': 'Nao Ajudou', 'qtd': 200},
         {'Action': 'Ajudou', 'qtd': 160},
         {'Action': 'Entrada Manual', 'qtd': 5}]
    )
    mock_similarity = 85
    params = load_params()
    scale_manual = params['scale_manual']
    mock_column = 'Action'
    
    manual_entries = match_manual(mock_df[mock_column], scale_manual, mock_similarity)
    
    assert isinstance(manual_entries, np.ndarray)
    expected_result = np.array([False, False, True])
    assert all(manual_entries == expected_result)


def test_remove_manual_entries_success_two_items():
    mock_df = pd.DataFrame(
        [{'Action': 'Nao Ajudou', 'qtd': 200},
         {'Action': 'Ajudou', 'qtd': 160},
         {'Action': 'Entrada Manual', 'qtd': 5}]
    )
    mock_similarity = 85
    params = load_params()
    scale_manual = params['scale_manual']
    mock_column = 'Action'
    
    result = remove_manual(mock_df, scale_manual, mock_similarity, mock_column)
    expected_result = pd.DataFrame(
        [{'Action': 'Nao Ajudou', 'qtd': 200},
         {'Action': 'Ajudou', 'qtd': 160}]
    )
    
    pd.testing.assert_frame_equal(result, expected_result)


def test_remove_manual_entries_success_five_items():
    mock_df = pd.DataFrame(
        [{'Action': 'muito_bom', 'qtd': 8313},
         {'Action': 'entrada manual', 'qtd': 2903},
         {'Action': 'nao_ajudou', 'qtd': 3642},
         {'Action': 'confuso', 'qtd': 1794},
         {'Action': 'lento', 'qtd': 581},
         {'Action': 'amei', 'qtd': 3465}]
    )
    mock_similarity = 85
    params = load_params()
    scale_manual = params['scale_manual']
    mock_column = 'Action'
    
    result = remove_manual(mock_df, scale_manual, mock_similarity, mock_column)
    
    expected_result = pd.DataFrame(
        [{'Action': 'muito_bom', 'qtd': 8313},
         {'Action': 'nao_ajudou', 'qtd': 3642},
         {'Action': 'confuso', 'qtd': 1794},
         {'Action': 'lento', 'qtd': 581},
         {'Action': 'amei', 'qtd': 3465}]
    )
    
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_result)


def test_remove_manual_entries_success_ten_items():
    mock_df = pd.DataFrame([
        {'Action': 1, 'qtd': 8313},
        {'Action': 2, 'qtd': 2903},
        {'Action': 3, 'qtd': 3642},
        {'Action': 4, 'qtd': 1794},
        {'Action': 5, 'qtd': 581},
        {'Action': 6, 'qtd': 3465},
        {'Action': 7, 'qtd': 3642},
        {'Action': 8, 'qtd': 1794},
        {'Action': 9, 'qtd': 581},
        {'Action': 10, 'qtd': 3465}]
    )
    
    mock_similarity = 85
    params = load_params()
    scale_manual = params['scale_manual']
    mock_column = 'Action'
    
    result = remove_manual(mock_df, scale_manual, mock_similarity, mock_column)
    
    expected_result = pd.DataFrame(
        [{'Action': 1, 'qtd': 8313},
         {'Action': 2, 'qtd': 2903},
         {'Action': 3, 'qtd': 3642},
         {'Action': 4, 'qtd': 1794},
         {'Action': 5, 'qtd': 581},
         {'Action': 6, 'qtd': 3465},
         {'Action': 7, 'qtd': 3642},
         {'Action': 8, 'qtd': 1794},
         {'Action': 9, 'qtd': 581},
         {'Action': 10, 'qtd': 3465}]
    )
    
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_result)


def test_remove_manual_entries_success_two_entries():
    mock_df = pd.DataFrame(
        [{'Action': 'Nao Ajudou', 'qtd': 200},
         {'Action': 'Ajudou', 'qtd': 160},
         {'Action': 'Entrada Manual', 'qtd': 5},
         {'Action': 'input inesperado', 'qtd': 5}]
    )
    mock_similarity = 85
    params = load_params()
    scale_manual = params['scale_manual']
    mock_column = 'Action'
    
    result = remove_manual(mock_df, scale_manual, mock_similarity, mock_column)
    
    expected_result = pd.DataFrame(
        [{'Action': 'Nao Ajudou', 'qtd': 200},
         {'Action': 'Ajudou', 'qtd': 160}]
    )
    
    pd.testing.assert_frame_equal(result, expected_result)


def test_remove_manual_entries_success_no_entries():
    mock_df = pd.DataFrame(
        [{'Action': 'Nao Ajudou', 'qtd': 200},
         {'Action': 'Ajudou', 'qtd': 160}]
    )
    mock_similarity = 85
    params = load_params()
    scale_manual = params['scale_manual']
    mock_column = 'Action'
    
    result = remove_manual(mock_df, scale_manual, mock_similarity, mock_column)
    
    expected_result = pd.DataFrame(
        [{'Action': 'Nao Ajudou', 'qtd': 200},
         {'Action': 'Ajudou', 'qtd': 160}]
    )
    
    pd.testing.assert_frame_equal(result, expected_result)


def test_remove_manual_numeric():
    mock_df = pd.DataFrame([{'Action': 3, 'qtd': 10},
                            {'Action': 5, 'qtd': 763},
                            {'Action': 1, 'qtd': 9},
                            {'Action': 10, 'qtd': 1},
                            {'Action': 4, 'qtd': 49},
                            {'Action': 'Outro', 'qtd': 101},
                            {'Action': 2, 'qtd': 1}
                            ])
    mock_similarity = 85
    params = load_params()
    scale_manual = params['scale_manual']
    mock_column = 'Action'
    
    result = remove_manual(mock_df, scale_manual, mock_similarity, mock_column)
    
    expected_result = pd.DataFrame([{'Action': 3, 'qtd': 10},
                                    {'Action': 5, 'qtd': 763},
                                    {'Action': 1, 'qtd': 9},
                                    {'Action': 10, 'qtd': 1},
                                    {'Action': 4, 'qtd': 49},
                                    {'Action': 2, 'qtd': 1}
                                    ])
    
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_result, check_dtype=False)


def test_remove_manual_empty_df():
    mock_df = pd.DataFrame(columns=['Action', 'qtd'])
    mock_similarity = 85
    params = load_params()
    scale_manual = params['scale_manual']
    mock_column = 'Action'
    
    with pytest.raises(InvalidDataframeError, match='Cannot process empty scale'):
        remove_manual(mock_df, scale_manual, mock_similarity, mock_column)


def test_remove_manual_missing_column():
    mock_df = pd.DataFrame(
        [{'qtd': 200},
         {'qtd': 160}]
    )
    mock_similarity = 85
    params = load_params()
    scale_manual = params['scale_manual']
    mock_column = 'Action'
    
    with pytest.raises(AbsentColumnError, match=r'.*Scale does not contain answer column.*'):
        remove_manual(mock_df, scale_manual, mock_similarity, mock_column)


def test_get_manual_entries_only_manual_entries():
    mock_df = pd.DataFrame(
        [{'Action': 'Entrada Manual', 'qtd': 5}]
    )
    mock_similarity = 85
    params = load_params()
    scale_manual = params['scale_manual']
    mock_column = 'Action'

    result = remove_manual(mock_df, scale_manual, mock_similarity, mock_column)
    expected_result = pd.DataFrame(columns=['Action', 'qtd'])

    pd.testing.assert_frame_equal(result, expected_result, check_like=True, check_dtype=False)
