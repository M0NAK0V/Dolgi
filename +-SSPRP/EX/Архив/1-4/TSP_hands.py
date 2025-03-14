import itertools
import time as time

import numpy as np

start = time.perf_counter()


def tsp_bruteforce(graph):
    n = len(graph)
    min_cost = float('inf')
    min_path = None

    for path in itertools.permutations(range(1, n)):  # переборка всех вариантов по n вершин
        cost = graph[0][path[0]]  # стоимость пути
        for i in range(n - 2):
            cost += graph[path[i]][path[i + 1]]
        cost += graph[path[-1]][0]

        if cost < min_cost:  # поиск минимума
            min_cost = cost  # длина кратчайшего пути
            min_path = [0] + list(path) # кратчайший путь + 0

    return min_path, min_cost


finish = time.perf_counter()
# Пример графа (матрица смежности)
matrix = np.array([[0, 10, 15, 20],
                   [10, 0, 35, 25],
                   [15, 35, 0, 30],
                   [20, 25, 30, 0]])

path, cost = tsp_bruteforce(matrix)
print("Минимальный путь:", *path, sep='->')
print("Длинна пути:", cost)
print('Время работы: ' + str(round((finish - start) * 1000, 5)))
