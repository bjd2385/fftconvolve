#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test the effects of Numba upon array dotting """


from numba import jit
from time import time
from math import ceil, log, log10
from numpy.random import randn
import numpy as np


__author__ = 'Brandon Doyle'
__email__  = 'bjd2385@aperiodicity.com'


def checkarrays(f):
    """ Similar to the @accepts decorator """
    def new_f(*args, **kwd):
        assert reduce(lambda x, y: x == y, map(np.shape, args))\
        , """Array and Subarray must have same dimensions,
got %s and %s""" % (args[0].shape, args[1].shape,)
        return f(*args, **kwd)
    return new_f

@checkarrays
@jit
def dotJit(subarray, kernel):
    """ perform a simple 'dot product' between the 2 dimensional 
    image subsets. 
    """
    total = 0.0
    # This is the O(n^2) part of the algorithm
    for i in xrange(subarray.shape[0]):
        for j in xrange(subarray.shape[1]):
            total += subarray[i][j] * kernel[i][j]
    return total

@checkarrays
def dot(subarray, kernel):
    """ perform a simple 'dot product' between the 2 dimensional 
    image subsets. 
    """
    total = 0.0
    # This is the O(n^2) part of the algorithm
    for i in xrange(subarray.shape[0]):
        for j in xrange(subarray.shape[1]):
            total += subarray[i][j] * kernel[i][j]
    return total

@checkarrays
def dotNumpy(subarray, kernel):
    """ Perform the matrix dot product with NumPy functions (probably
    the fastest implementation)
    """
    return np.sum(subarray * kernel)        # entrywise

def main():
    import matplotlib.pyplot as plt
    times1, times2, times3, labels = [], [], [], []

    number = 20
    
    for i in xrange(1, number):
        numbers = ceil(log(10 ** i) / log(1.005)), \
                  ceil(log(10 ** i) / log(1.005))
        X = randn(*numbers)
        Y = randn(*numbers)
        labels.append(str(log10(numbers[0]))[:4])

        print \
    "Created X and Y for {0}, {1} numbers".format(i, numbers)
        
        _start = time()
        dotJit(X, Y)
        _end = time()
        times1.append(_end - _start)
        print "Time for jit {0}: {1}".format(i, _end - _start)

        _start = time()
        dot(X, Y)
        _end = time()
        times2.append(_end - _start)
        print "Time for dot {0}: {1}".format(i, _end - _start)

        _start = time()
        dotNumpy(X, Y)
        _end = time()
        times3.append(_end - _start)
        print "Time for NumPy {0}: {1}".format(i, _end - _start)
        print

    times1 = [log(timed) for timed in times1]
    times2 = [log(timed) for timed in times2]
    times3 = [log(timed) for timed in times3]

    plt.plot(times1, label='Jit')
    plt.plot(times2, label='Pure')
    plt.plot(times3, label='NumPy')

    plt.xlim([-0.5, len(times1) - 0.5])

    # modify xticks to represent data
    plt.xticks(range(0, number - 1), labels)

    plt.legend(fontsize=12, loc='upper left')
    plt.xlabel(r'Array Size ($\log_{10}\left(A\right)/2$)', fontsize=12)
    plt.ylabel(r'Time ($\log_{10}(s)$)', fontsize=12)
    plt.title('Comparing Numba to Pure Python', fontsize=12)
    plt.show()

if __name__ == '__main__':
    main()