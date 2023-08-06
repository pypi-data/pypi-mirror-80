#! /usr/bin/env python

import numpy as np
from __init__ import calc_ado

n_data = 5000
n_calc = 500
x = np.random.rand(n_data)
y = np.random.rand(n_data)
targets = np.random.randint(2, size=n_data)

# ADO calculated without statistics
print(calc_ado(fx=x, gx=y, target=targets))

# ADO example where you expect perfect similarity (i.e. compare x with x)
print(calc_ado(fx=x, gx=x, target=targets, n_data=n_calc))
