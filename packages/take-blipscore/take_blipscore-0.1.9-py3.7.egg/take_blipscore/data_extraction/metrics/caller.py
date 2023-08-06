_author__ = "Juliana Guamá"
__version__ = "0.1.0"

import abc


class PipelineCaller(object, metaclass=abc.ABCMeta):
    """Abstract class to run pipelines and get rates.
    
    :keyword sql_context: Pyspark SQL context to connect to database and table.
    :type sql_context: ``pyspark.SQLContext``
    :keyword bot_identity: Bot identity on database.
    :type bot_identity: ``str``
    :keyword start_date: Beginning date to filter ("yyyy-mm-dd").
    :type start_date: ``str``
    :keyword end_date: Ending date to filter ("yyyy-mm-dd").
    :type end_date: ``str``
    :keyword category_action: List of action for each category on eventtracks table.
    :type category_action: ``dict`` from ``str`` to ``list`` of ``str``
    """
    
    def __init__(self, **kwargs):
        self.sql_context = kwargs.get("sql_context")
        self.bot_identity = kwargs.get("bot_identity")
        self.start_date = kwargs.get("start_date")
        self.end_date = kwargs.get("end_date")
        self.category_action = kwargs.get("category_action")
    
    @abc.abstractmethod
    def get_rate(self) -> float:
        """Run take's metric pipeline to return rate.
        
        :return: Metric rate.
        :rtype: ``float``
        """
        raise NotImplementedError()
