import numpy as np
import math
import time
import matplotlib.pyplot as plt
from python_tsp.exact.dynamic_programming import \
    solve_tsp_dynamic_programming  # точный метод динамического программирования, вместо брут форса (полного перебора)

start = time.perf_counter()
matrix = np.array([[0, 10, 15, 20],
                   [10, 0, 35, 25],
                   [15, 35, 0, 30],
                   [20, 25, 30, 0]])

path, distance = solve_tsp_dynamic_programming(matrix)
finish = time.perf_counter()
# Для симметричной задачи делим решение на 2
print('Cложность решения комбинаторной задачи TSP для симметричной задачи = O((n!-1)/2) = ',
      int(math.factorial(((matrix.shape[1])) - 1) / 2))
print('Кратчайший путь = ', *path, sep='->')
print('Длинна данного пути равна = ', distance)
print('Время работы: ' + str(round((finish - start) * 1000, 5)))
