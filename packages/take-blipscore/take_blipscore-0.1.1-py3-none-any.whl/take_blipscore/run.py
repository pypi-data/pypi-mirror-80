__author__ = "Gabriel Salgado and Juliana Guamá"
__version__ = "0.2.1"

import typing as tp
import numpy as np

from take_blipscore.utils.sparksql_ops import CONTEXT
from take_blipscore.utils.load_conf import load_params
from take_blipscore.data_extraction.get_rates import get_rates
from take_blipscore.processing.metrics import blip_metric

MapData = tp.Dict[str, tp.Any]
Output = tp.Dict[str, MapData]


def transform(params: tp.Dict[str, str], rates: tp.Dict[str, float]) -> tp.Tuple[np.ndarray, np.ndarray]:
    """Transform params and rates into arrays.
    
    :param params: Project params.
    :type params: ``dict`` from ``str`` to ``str``
    :param rates: Metrics rates.
    :type rates: ``dict`` from ``str`` to ``float``
    :return: Weight and rate arrays.
    :rtype: ``list`` from ``numpy.ndarray``
    """
    w_list = list()
    x_list = list()
    for metric_name, metric_param in params["metrics"].values():
        w_list.append(metric_param["weight"])
        x_list.append(rates[metric_name])
    return np.array(w_list), np.array(x_list)


def run(sql_context: CONTEXT, bot_identity: str, start_date: str, end_date: str,
        category_action: tp.Dict[str, tp.List[str]], **kwargs: tp.Any) -> Output:
    """Run BLiP Score.
    
    :param sql_context: Pyspark SQL context to connect to database and table.
    :type  sql_context: ``pyspark.SQLContext``
    :param bot_identity: Bot identity on database.
    :type bot_identity: ``str``
    :param start_date: Beginning date to filter ("yyyy-mm-dd").
    :type start_date: ``str``
    :param end_date: Ending date to filter ("yyyy-mm-dd").
    :type end_date: ``str``
    :param category_action: List of action for each category on eventtracks table.
    :type category_action: ``dict`` from ``str`` to ``list`` of ``str``
    :param kwargs: Parameters to overwrite configuration parameters.
    :type kwargs: ``any``
    :return: The bot blip_score.
    :rtype: ``dict`` from ``str`` to ``dict`` from ``str`` to ``any``
    """
    params = load_params()
    params.update(kwargs)
    
    rates = get_rates(metrics=params["metrics"],
                      sql_context=sql_context,
                      bot_identity=bot_identity,
                      start_date=start_date,
                      end_date=end_date,
                      category_action=category_action)
    
    w_list, x_list = transform(params=params, rates=rates)
    blip_score = blip_metric(weight=w_list, x=x_list)
    
    return {
        "params": params,
        "results": {
            "features": {
                "scores": rates
            },
            "reporting": {
                "blip_score": blip_score
            }
        }
    }
