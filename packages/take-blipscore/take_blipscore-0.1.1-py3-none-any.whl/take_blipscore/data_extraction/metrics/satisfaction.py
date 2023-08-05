_author__ = "Juliana Guamá"
__version__ = "0.1.0"

import typing as tp
from statistics import mean
import take_satisfaction as ts

from take_blipscore.data_extraction.metrics.caller import PipelineCaller


class Satisfaction(PipelineCaller):
    """Class to run satisfaction's pipelines and get rate.

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
    
    def __int__(self, **kwargs):
        super().__init__(**kwargs)
    
    @staticmethod
    def transform_action(action_list: tp.List[tp.Any]) -> tp.List[str]:
        """Transform action list entry for satisfaction_rate.

        :param action_list: Action list.
        :type action_list: ``list`` to ``str``
        :return: Formatted action for satisfaction pipelines.
        :rtype: ``dict`` from ``list`` to ``list`` from ``str``
        """
        return list(map(str, action_list))
    
    def create_query_params(self, category: str, actions: tp.List[str]):
        """Create `query_params` input for satisfaction pipeline.
        
        :param category: Category from eventtrack table.
        :type category: ``str``
        :param actions: Action list.
        :type actions: ``dict`` from ``list`` to ``list`` from ``str``
        :return:
        """
        return {
            "bot_identity": self.bot_identity,
            "category": category,
            "answers": self.transform_action(action_list=actions),
            "start_date": self.start_date,
            "end_date": self.end_date
        }

    def get_rate(self) -> float:
        """Run take_satisfaction's pipeline to return rate.

        :return: Satisfaction rate.
        :rtype: ``float``
        """
        ts_score = list()
        
        for category, actions in self.category_action.items():
            query_params = self.create_query_params(category=category, actions=actions)
            ts_score.append(ts.run(
                sql_context=self.sql_context,
                query_parameters=query_params,
                query_type="db_actions_query"))
        
        return float(mean(ts_score))
