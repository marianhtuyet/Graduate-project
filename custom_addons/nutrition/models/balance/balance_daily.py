
from __future__ import division
import math
import random

from itertools import repeat

from urllib3.connectionpool import xrange

try:
    from collections.abc import Sequence
except ImportError:
    from collections import Sequence




def mutUniformInt(individual, low, up, indpb, meals1_indexes = 10, meals2_indexes = 20,
                  meals3_indexes=30, meals4_indexes=40, meals5_indexes=50):
    """Mutate an individual by replacing attributes, with probability *indpb*,
    by a integer uniformly drawn between *low* and *up* inclusively.
    :param individual: :term:`Sequence <sequence>` individual to be mutated.
    :param low: The lower bound or a :term:`python:sequence` of
                of lower bounds of the range from which to draw the new
                integer.
    :param up: The upper bound or a :term:`python:sequence` of
               of upper bounds of the range from which to draw the new
               integer.
    :param indpb: Independent probability for each attribute to be mutated.
    :returns: A tuple of one individual.
    """
    size = len(individual)
    low = list(repeat(0, size))
    up = list(repeat(0, size))
    # Tạo các phần tử Sáng, xế, canh mặn xào trong 1 khoảng xác định. tương tự như individual
    for index, x in enumerate(low):
        if index % 5 == 0:
            low[index] = 0
        if index % 5 == 1:
            low[index] = meals1_indexes + 1
        if index % 5 == 2:
            low[index] = meals2_indexes + 1
        if index % 5 == 3:
            low[index] = meals3_indexes + 1
        if index % 5 == 4:
            low[index] = meals4_indexes + 1
    for index, x in enumerate(up):
        if index % 5 == 0:
            up[index] = meals1_indexes
        if index % 5 == 1:
            up[index] = meals2_indexes
        if index % 5 == 2:
            up[index] = meals3_indexes
        if index % 5 == 3:
            up[index] = meals4_indexes
        if index % 5 == 4:
            up[index] = meals5_indexes

    for i, xl, xu in zip(xrange(size), low, up):
        if random.random() < indpb:
            individual[i] = random.randint(xl, xu)
    return individual,

mutUniformInt([3, 21, 31, 56, 72, 0, 19, 30, 55, 74, 0, 20, 42, 50, 76, 0, 19, 42,
               50, 79, 1, 26, 32, 60, 69, 1, 23, 37, 51, 70, 0, 23, 37, 64, 68, 9,
               20, 38, 47, 72, 0, 19, 36, 48, 79, 15, 20, 33, 48, 75] ,
              1, 1 , 0.1, 10, 20, 30, 40, 50
              )