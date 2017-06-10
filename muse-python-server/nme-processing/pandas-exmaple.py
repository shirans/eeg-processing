from glob import glob
import pandas as pd
import numpy as np
import logging

logger = logging.Logger('catch_all')

# from the pandas tutorial: http://pandas.pydata.org/pandas-docs/stable/dsintro.html#dsintro

# Series is a one-dimensional labeled array capable of holding any data type
# data from ndarray: indexes must be the same size
from pandas.core.indexes.base import InvalidIndexError

s = pd.Series(np.random.randn(5), index=['a', 'b', 'c', 'd', 'e'])
print(s)
# from dict
d = {'a': 0., 'b': 1., 'c': 2.}
print(d)
# From scalar value
scalar = pd.Series(5., index=['a', 'b', 'c', 'd', 'e'])
print(scalar)

# Series is ndarray-like
print(s[0])
print(s[:3])
print(s[s > s.median()])
print(np.exp(s))

# A Series is like a fixed-size dict in that you can get and set values by index label:
print(s['a'])

# .get returns nun, vs dict like which throws exception
try:
    s['f']
except KeyError as e:
    print(e)

print(s.get('f'))
print(s.get('f'), np.nan)

# vector operations like numpy
newb = s + s

# DataFrame is a 2-dimensional labeled data structure with columns of potentially different types
d = {'one': pd.Series([1., 2., 3.], index=['a', 'b', 'c']),
     'two': pd.Series([1., 2., 3., 4.], index=['a', 'b', 'c', 'd'])}

df = pd.DataFrame(d)
print(df)
df = pd.DataFrame(d, index=['d', 'b', 'a'])
print(df)
df = pd.DataFrame(d, index=['a', 'b'], columns=['one', 'three'])
print(df)
subject = '1'
session = '1'

# from file
iris = pd.read_csv('data/iris.data')