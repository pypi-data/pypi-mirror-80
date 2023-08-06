__author__ = "Gabriel Salgado, Juliana Guamá and Milo Utsch"
__version__ = "0.1.2"
__all__ = [
    "SDF",
    "CONTEXT"
]

import warnings as wn

with wn.catch_warnings():
    wn.simplefilter("ignore")
    import pyspark as ps

SDF = ps.sql.DataFrame
CONTEXT = ps.sql.HiveContext
