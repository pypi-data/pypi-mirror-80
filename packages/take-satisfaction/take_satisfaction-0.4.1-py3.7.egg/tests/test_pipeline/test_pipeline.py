__author__ = 'Milo Utsch'
__version__ = '0.1.2'

import pandas as pd

from take_satisfaction.utils import load_params
from take_satisfaction.preprocess import remove_manual
from take_satisfaction.preprocess import complete_scale
from take_satisfaction.conversion import convert_scale
from take_satisfaction.calculation import calculate_satisfaction_rate


def test_pipeline_expressions():
    mock_df = pd.DataFrame([{'Action': 'Pessimo', 'qtd': 93},
                            {'Action': 'Adorei', 'qtd': 282},
                            {'Action': 'Gostei', 'qtd': 236},
                            {'Action': 'input inesperado', 'qtd': 48},
                            {'Action': 'Nao sei', 'qtd': 33},
                            {'Action': 'Nao gostei', 'qtd': 39}
                            ])
    mock_actions = ''
    mock_column = 'Action'
    mock_missing_quantity = 0
    
    params = load_params()
    scale_manual = params['scale_manual']
    similarity_threshold = params['similarity_threshold']
    answer_column = params['bot_events_answer_column']
    quantities_column = params['bot_events_quantities_column']
    
    completed_df = complete_scale(mock_df, answer_column, quantities_column, mock_actions, mock_missing_quantity)
    preprocessed_df = remove_manual(completed_df, scale_manual, similarity_threshold, mock_column)
    
    expected_preprocess = pd.DataFrame([{'Action': 'Pessimo', 'qtd': 93},
                                        {'Action': 'Adorei', 'qtd': 282},
                                        {'Action': 'Gostei', 'qtd': 236},
                                        {'Action': 'Nao sei', 'qtd': 33},
                                        {'Action': 'Nao gostei', 'qtd': 39}
                                        ])
    
    pd.testing.assert_frame_equal(preprocessed_df.reset_index(drop=True), expected_preprocess)
    
    scale_translations = params['scale_translations']
    converted_df = convert_scale(preprocessed_df, mock_column, scale_translations, similarity_threshold)
    
    expected_converted = pd.DataFrame([{'Action': 0, 'qtd': 93},
                                       {'Action': 1, 'qtd': 39},
                                       {'Action': 2, 'qtd': 33},
                                       {'Action': 3, 'qtd': 236},
                                       {'Action': 4, 'qtd': 282}
                                       ])
    
    pd.testing.assert_frame_equal(converted_df.reset_index(drop=True), expected_converted)
    
    satisfaction_rate = calculate_satisfaction_rate(converted_df, answer_column, quantities_column)
    
    expected_satisfaction = 0.7104685212298683
    assert satisfaction_rate == expected_satisfaction


def test_pipeline_numeric():
    mock_df = pd.DataFrame([{'Action': 3, 'qtd': 10},
                            {'Action': 5, 'qtd': 763},
                            {'Action': 1, 'qtd': 9},
                            {'Action': 10, 'qtd': 1},
                            {'Action': 4, 'qtd': 49},
                            {'Action': 'Outro', 'qtd': 101},
                            {'Action': 2, 'qtd': 1}
                            ])
    mock_column = 'Action'
    mock_actions = ''
    mock_missing_quantity = 0
    
    params = load_params()
    scale_manual = params['scale_manual']
    similarity_threshold = params['similarity_threshold']
    answer_column = params['bot_events_answer_column']
    quantities_column = params['bot_events_quantities_column']

    completed_df = complete_scale(mock_df, answer_column, quantities_column, mock_actions, mock_missing_quantity)
    preprocessed_df = remove_manual(completed_df, scale_manual, similarity_threshold, mock_column)
    
    expected_preprocess = pd.DataFrame([{'Action': 3, 'qtd': 10},
                                        {'Action': 5, 'qtd': 763},
                                        {'Action': 1, 'qtd': 9},
                                        {'Action': 10, 'qtd': 1},
                                        {'Action': 4, 'qtd': 49},
                                        {'Action': 2, 'qtd': 1}
                                        ])

    pd.testing.assert_frame_equal(preprocessed_df.reset_index(drop=True), expected_preprocess, check_dtype=False)
    
    scale_translations = params['scale_translations']
    converted_df = convert_scale(preprocessed_df, mock_column, scale_translations, similarity_threshold)
    
    expected_converted = pd.DataFrame([{'Action': 1, 'qtd': 9},
                                       {'Action': 2, 'qtd': 1},
                                       {'Action': 3, 'qtd': 10},
                                       {'Action': 4, 'qtd': 49},
                                       {'Action': 5, 'qtd': 763},
                                       {'Action': 10, 'qtd': 1}
                                       ])
    
    pd.testing.assert_frame_equal(converted_df.reset_index(drop=True), expected_converted)
    
    satisfaction_rate = calculate_satisfaction_rate(converted_df, answer_column, quantities_column)
    
    expected_satisfaction = 0.43070561557956516
    assert satisfaction_rate == expected_satisfaction


def test_pipeline_expressions_missint_item():
    mock_df = pd.DataFrame([{'Action': 'Pessimo', 'qtd': 93},
                            {'Action': 'Adorei', 'qtd': 282},
                            {'Action': 'Gostei', 'qtd': 236},
                            {'Action': 'input inesperado', 'qtd': 48},
                            {'Action': 'Nao gostei', 'qtd': 39}
                            ])
    mock_actions = ['Pessimo', 'Adorei', 'Gostei', 'Nao sei', 'Nao gostei']
    mock_column = 'Action'
    mock_missing_quantity = 0
    
    params = load_params()
    scale_manual = params['scale_manual']
    similarity_threshold = params['similarity_threshold']
    answer_column = params['bot_events_answer_column']
    quantities_column = params['bot_events_quantities_column']
    
    completed_df = complete_scale(mock_df, answer_column, quantities_column, mock_actions, mock_missing_quantity)
    preprocessed_df = remove_manual(completed_df, scale_manual, similarity_threshold, mock_column)
    
    expected_preprocess = pd.DataFrame([{'Action': 'Pessimo', 'qtd': 93},
                                        {'Action': 'Adorei', 'qtd': 282},
                                        {'Action': 'Gostei', 'qtd': 236},
                                        {'Action': 'Nao gostei', 'qtd': 39},
                                        {'Action': 'Nao sei', 'qtd': 0}
                                        ])
    
    pd.testing.assert_frame_equal(preprocessed_df.reset_index(drop=True), expected_preprocess)
    
    scale_translations = params['scale_translations']
    converted_df = convert_scale(preprocessed_df, mock_column, scale_translations, similarity_threshold)
    
    expected_converted = pd.DataFrame([{'Action': 0, 'qtd': 93},
                                       {'Action': 1, 'qtd': 39},
                                       {'Action': 2, 'qtd': 0},
                                       {'Action': 3, 'qtd': 236},
                                       {'Action': 4, 'qtd': 282}
                                       ])
    
    pd.testing.assert_frame_equal(converted_df.reset_index(drop=True), expected_converted)
    
    satisfaction_rate = calculate_satisfaction_rate(converted_df, answer_column, quantities_column)
    
    expected_satisfaction = 0.7211538461538461
    assert satisfaction_rate == expected_satisfaction
