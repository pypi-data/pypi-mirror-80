_author__ = "Juliana Guamá"
__version__ = "0.1.0"

import typing as tp
import take_resolution as tr

from take_blipscore.data_extraction.metrics.caller import PipelineCaller

TRACKINGS = tp.Dict[str, tp.List[tp.Any]]
CATEGORY_ACTIONS = tp.List[tp.List[tp.Tuple[str, str]]]


class Resolution(PipelineCaller):
    """Class to run resolution's pipelines and get rate.

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
    def transform(trackings: TRACKINGS) -> CATEGORY_ACTIONS:
        """Transform tracking entry to category_action_groups for resolution_rate.

        :param trackings: Tracking with action list.
        :type trackings: ``dict`` from ``str`` to ``list`` to ``str``
        :return: Formatted tracking_action for resolution pipelines.
        :rtype: ``dict`` from ``list`` to ``tuple`` to ``str``
        """
        return [
            [('Category', category), ('Action', action)]
            for category, actions in trackings.items()
            for action in actions
        ]
    
    def get_rate(self) -> float:
        """Run take_resolution's pipelines to return rate.

        :return: Resolution rate.
        :rtype: ``float``
        """
        category_action_groups = self.transform(trackings=self.category_action)
        output = tr.run(
            'events',
            sql_context=self.sql_context,
            bot_identity=self.bot_identity,
            min_date=self.start_date,
            max_date=self.end_date,
            category_action_groups=category_action_groups)
        df_events_raw = output['raw']['df_events_raw']
        
        output = tr.run(
            'daus', sql_context=self.sql_context,
            query_params={'bot_identity': self.bot_identity,
                          'min_date': self.start_date,
                          'max_date': self.end_date})
        df_daus_raw = output['raw']['df_daus_raw']
        
        output = tr.run(
            'rate',
            df_daus_raw=df_daus_raw,
            df_events_raw=df_events_raw)
        
        return output['reporting']['resolution_rate']
