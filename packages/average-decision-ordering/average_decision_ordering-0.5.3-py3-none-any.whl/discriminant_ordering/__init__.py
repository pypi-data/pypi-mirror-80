#! /usr/bin/env python

import numpy as np

""" A few commonly used functions"""

def frange(start, stop, step):
    i = start
    while i < stop:
        yield i
        i += step

def heaviside(x):
    return 0.5 * (np.sign(x) + 1)


def filter2D(x, y, target):
    x0, y0, x1, y1 = [], [], [], []
    for i in range(len(target)):
        if target[i] == 0:
            x0.append(x[i])
            y0.append(y[i])
        elif target[i] == 1:
            x1.append(x[i])
            y1.append(y[i])
    return np.asarray(x0), np.asarray(y0), np.asarray(x1), np.asarray(y1)

''' Ordering Discriminant '''
def DO(fx, gx, target, n_data):
    data = np.vstack((fx, gx, target)).T
    np.random.seed(123)
    np.random.shuffle(data)
    fx = data[:,0]
    gx = data[:,1]
    target = data[:,2]
    fx, gx, target = fx[0:n_data], gx[0:n_data], target[0:n_data]
    fx0, gx0, fx1, gx1 = filter2D(fx, gx, target)
    heavi_sum = 0
    for idx in range(len(fx0)):
        for idy in range(len(fx1)):
            heavi_side = heaviside( (fx0[idx] - fx1[idy]) * (gx1[idy] - gx0[idx]) )
            heavi_sum = heavi_side + heavi_sum
    return 2*(np.abs((float(1.0/len(fx0)) * float(1.0/len(gx0)) * heavi_sum) - 0.5))