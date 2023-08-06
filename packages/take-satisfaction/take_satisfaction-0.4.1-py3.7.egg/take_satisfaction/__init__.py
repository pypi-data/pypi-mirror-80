"""
This project is on POC.

Project configuration param:

:param bot_events_answer_column: column ALIAS for eventtracks.Action. Default value is "Action"
:type bot_events_answer_column: str
:param bot_events_quantities_column:  column ALIAS for eventtracks.Action count. Default value is "qtd",
:type bot_events_answer_column: str
:param similarity_threshold: threshold for string matching for scale identification. Default value 83.
:type similarity_threshold: int
:param databricks_query: query that extract satisfaction scale and count per item. Default value:
    "SELECT {bot_events_answer_column}
            ,COUNT(*) AS {bot_events_quantities_column}
    FROM {databale}.eventtracks
    WHERE
    AND StorageDateDayBR >= '{start_date}'
    AND StorageDateDayBR < '{end_date}'
    AND OwnerIdentity = '{bot_identity}'
    AND Category = '{category}'
    GROUP BY Action"
:type databricks_query: str
"""


__author__ = 'Gabriel Salgado, Juliana Guamá, Milo Utsch and Rogers Damas'
__version__ = '0.4.1'
__description__ = 'This project calculates the satisfaction score for BLiP chatbots.'

from .run import run
