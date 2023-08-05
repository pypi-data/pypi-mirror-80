__author__ = "Juliana Guamá"
__version__ = "0.1.0"
__all__ = [
    "ARRAY",
    "FLOAT",
    "ln",
    "weighted_gmean"
]

import numpy as np

ARRAY = np.ndarray
FLOAT = np.float64
ln = np.log


def weighted_gmean(weight: ARRAY, x: ARRAY) -> FLOAT:
    """Weighted geometric mean.

    :math:
    \\exp(\\sum^(n)_(i=0)wi*\\ln(xi) \\(1/\\sum^(n)_(i=0)wi)), \n
    for w as weight
    
    :param weight: Weight for each `xi`.
    :type weight: ``numpy.ndarray``
    :param x: Variable array.
    :type x: ``numpy.ndarray``
    :return: Weighted geometric mean.
    :rtype: ``numpy.float64``
    """
    return np.exp(np.vdot(a=weight, b=ln(x)) /
                  sum(weight))
