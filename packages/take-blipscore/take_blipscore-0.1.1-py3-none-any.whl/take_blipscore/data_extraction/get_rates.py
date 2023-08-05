_author__ = "Juliana Guamá"
__version__ = "0.1.0"

import typing as tp
import importlib as il
from warnings import warn

import take_blipscore.data_extraction.metrics as m
from take_blipscore.utils.git_ops import access_repository


def load(path: str) -> tp.Type[m.PipelineCaller]:
    """Load a function by import for node.

    :param path: Path with package, module and function name.
    :type path: ``str``
    :return: Imported class.
    :rtype: ``type``
    """
    module_name, name = path.rsplit('.', 1)
    module = il.import_module(module_name)
    return getattr(module, name)


def get_rates(metrics: dict, **kwargs):
    """Run all metrics pipelines and return rates.
    
    :param metrics: Metrics by name with parameters.
    :type metrics: ``dict`` to ``str``
    :return: Rates by metric name.
    :rtype: ``dict`` to ``str``
    """
    user = kwargs["user_access"]
    out = {"error": dict()}
    for metric_name, metric_params in metrics.items():
        try:
            access_repository(user=user[metric_name]["user"], password=user[metric_name]["password"],
                              repository=user[metric_name]["repository"], chdir=metric_params[metric_name]["chdir"],
                              branch=user[metric_name]["branch"])
        except Exception as e:
            Exception(f"Error accessing `{metric_name}` repository:\n")
            raise e
        
        rate_class = load(metric_params["class_path"])
        try:
            out[metric_name] = rate_class(**kwargs).get_rate()
        except Exception as e:
            out[metric_name] = 0
            out["error"][metric_name] = e
            warn(f"Pipeline processing error on {metric_name}:\n{e}")
            
    return out
