__author__ = 'Gabriel Salgado, Juliana Guamá, Milo Utsch e Rogers Damas'
__version__ = '0.4.1'

import typing as tp

from take_satisfaction.utils import CONTEXT
from take_satisfaction.utils import load_params
from take_satisfaction.utils import iterable_to_tuple
from take_satisfaction.utils import get_default
from take_satisfaction.utils import load_query
from take_satisfaction.utils import format_text
from take_satisfaction.utils import query_df
from take_satisfaction.utils import spark_to_pandas
from take_satisfaction.preprocess import complete_scale
from take_satisfaction.preprocess import remove_manual
from take_satisfaction.conversion import convert_scale
from take_satisfaction.calculation import calculate_satisfaction_rate


def run(sql_context: CONTEXT, query_parameters: tp.Dict[str, tp.Any], query_type: str = 'db_simple_query',
        **kwargs) -> tp.Dict[str, tp.Any]:
    """Run Take Satisfaction
    
    :param sql_context: Context for spark.
    :type sql_context: ``pyspark.sql.HiveContext``
    :param query_parameters: Dictionary containing parameters to be formatted into the survey query.
    :type query_parameters: ``dict`` from ``str`` to ``any``
    :param query_type: Type of the query to be used. Can be either 'db_simple_query' or 'db_actions_query'.
    :type query_type: ``str``
    :param kwargs: Parameters to overwrite configuration parameters.
    :type kwargs: ``any``
    :return: Parameters and results for MLFlow register.
    :rtype: ``dict`` from ``str`` to ``any``
    """
    params = load_params()
    params.update(kwargs)
    
    params_answers = params['answers']
    answers = get_default(query_parameters, 'answers', params_answers)
    answers_tuple = iterable_to_tuple(answers)
    query_parameters['answers'] = answers_tuple
    
    query_file = get_default(params, query_type, 'db_simple_query')
    
    bot_events_answer_column = params['bot_events_answer_column']
    bot_events_quantities_column = params['bot_events_quantities_column']
    
    query_parameters['answer'] = bot_events_answer_column
    query_parameters['quantities'] = bot_events_quantities_column
    
    loaded_query = load_query(query_file)
    query = format_text(loaded_query, query_parameters)
    
    sp_df = query_df(sql_context=sql_context, query=query)
    
    scale_raw_df = spark_to_pandas(df=sp_df)
    
    scale_manual = params['scale_manual']
    similarity_threshold = params['similarity_threshold']
    preprocessed_df = remove_manual(df=scale_raw_df,
                                    manual_entries=scale_manual,
                                    threshold=similarity_threshold,
                                    column=bot_events_answer_column)
    
    missing_quantity = params['missing_quantity']
    preprocessed_completed_df = complete_scale(preprocessed_df,
                                               bot_events_answer_column,
                                               bot_events_quantities_column,
                                               answers_tuple,
                                               missing_quantity)
    
    scale_translations = params['scale_translations']
    converted_df = convert_scale(df=preprocessed_completed_df,
                                 column=bot_events_answer_column,
                                 reference=scale_translations,
                                 threshold=similarity_threshold)
    
    satisfaction_rate = calculate_satisfaction_rate(df=converted_df,
                                                    level_column=bot_events_answer_column,
                                                    quantities_column=bot_events_quantities_column)
    
    return {
        'params': params,
        'result': {
            'raw': {
                'scale': scale_raw_df
            },
            'primary': {
                'preprocessed': preprocessed_completed_df
            },
            'features': {
                'converted': converted_df
            },
            'model_input': {
                'satisfaction_rate': satisfaction_rate
            },
        }
    }
