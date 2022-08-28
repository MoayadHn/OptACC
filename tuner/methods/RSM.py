import math
import numpy as np
from ..searchresult import SearchResult
from ..testresult import TestResult

DEFAULT_INITIAL_POINT = Point(256, 128)

def _RSM_search(objective, points):
    '''Optimizes an objective function using a grid search.
        
        Arguments:
        objective -- the objective function to optimize.  Receives a Point as input
        and returns a SearchResult.
        points -- a generator producing Points at which to evaluate the function.
        '''
    Y = []
    x1 = [64,128,256]
    x2 = [256,128,64]
    pt0 =Point(64,256)
    pt1 = Point(128,128)
    pt2 = Point(256,64)
    Y = [objective(pt0), objective(pt1), objective(pt2)]
    
    times = {}
    iterations = 0
    for pt in points:
        iterations += 1
        result = objective(pt)
        Y.append(result)
    coeffecents = model_RSM(x1, x2, Y)
         c0, c1, c2 = map(float, coeffecents)
        x,y = map(int,points[100])
    for pt in points:
         x1, x2 = map(int, pt)
         preY = c0 + c1 * x1 + c2 * x2
    best = sorted(times, keys=lambda x: times[x])[0]
    return SearchResult(best, times, iterations)

def _tune_RSM(objective, opts, mul):
    # Exhaustive search: search multiples of mul within gang/vector ranges
    def generator():
        X1 = []
        X2 = []
        gmin = int(math.ceil(opts.num_gangs_min / float(mul)))
        gmax = int(opts.num_gangs_max / mul)
        vmin = int(math.ceil(opts.vector_length_min / float(mul)))
        vmax = int(opts.vector_length_max / mul)
        for gang_mult in range(gmin, gmax+1): # +1 since range is exclusive
            for vec_mult in range(vmin, vmax+1):
                num_gangs = max(mul * gang_mult, 1)    # max(_, 1) ensures
                vector_length = max(mul * vec_mult, 1) # these are nonzero
                yield Point(num_gangs, vector_length)
    return _RSM_search(objective, generator())

def model_RSM(X1,X2, Y):
    a0 = 0;
    a1 = 0;
    a2 = 0;
         
    results = Point(a0,a1,a2)
    return results
def tune_RSM(objective, opts):
    return _tune_RSM(objective, opts, 32)