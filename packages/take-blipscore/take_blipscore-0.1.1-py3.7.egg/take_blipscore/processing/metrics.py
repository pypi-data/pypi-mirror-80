__author__ = "Juliana Guamá"
__version__ = "0.1.1"
__all__ = [
    "blip_metric"
]

from take_blipscore.utils.metrics import ARRAY, FLOAT, weighted_gmean


def blip_metric(weight: ARRAY, x: ARRAY) -> FLOAT:
    """Calculate BLiP Score.
    
    BLiP Score is defined as weighted geometric mean of resolution and satisfaction score.
    
    :param weight: Weight for each score.
    :type weight: ``numpy.ndarray``
    :param x: Variable array.
    :type x: ``numpy.ndarray``
    :return: Geometric meam of weighted metrics.
    :rtype: ``numpy.float64``
    """
    return weighted_gmean(weight=weight, x=x)
