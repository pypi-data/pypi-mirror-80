#!/usr/bin/env python
# ------------------------------------------------------------------------------------------------------%
# Created by "Thieu Nguyen" at 20:02, 27/09/2020                                                        %
#                                                                                                       %
#       Email:      nguyenthieu2102@gmail.com                                                           %
#       Homepage:   https://www.researchgate.net/profile/Thieu_Nguyen6                                  %
#       Github:     https://github.com/thieu1995                                                        %
# -------------------------------------------------------------------------------------------------------%

import numpy as np
import matplotlib.pyplot as plt
from opfunu.dimension_based.benchmarknd import Functions

size = 100
ranges = np.linspace(-4, 4, size)
X, Y = np.meshgrid(ranges, ranges)

Z = np.empty((size, size))

# for i in range(size):
#     for j in range(size):
#         solution = np.array([X[i, j], Y[i, j]])
#         Z[i, j] = Functions._ackley__(solution)
#
# plt.contourf(X, Y, Z)

temp = Functions._ackley__(np.ones(3))
