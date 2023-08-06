__author__ = 'Gabriel Salgado and Milo Utsch'
__version__ = '0.1.3'

from take_satisfaction.utils import load_params


def test_load_params():
    params = load_params()
    assert isinstance(params, dict)
    assert 'bot_events_answer_column' in params
    assert 'bot_events_quantities_column' in params
    assert 'db_simple_query' in params
    assert 'db_actions_query' in params
    assert 'similarity_threshold' in params
    assert 'scale_manual' in params
    assert 'scale_translations' in params
    
    
def test_load_scale_translations():
    params = load_params()
    scale_translations = params['scale_translations']
    
    assert isinstance(scale_translations, list)

