import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import time

class AntColony:
    def __init__(self, graph, num_ants, num_iterations, alpha, beta, evaporation_rate, Q):
        self.graph = graph
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.Q = Q
        self.pheromone = np.ones((graph.number_of_nodes(), graph.number_of_nodes())) / graph.number_of_nodes()
        self.best_route = None
        self.best_cost = float('inf')

    def run(self):
        for iteration in range(self.num_iterations):
            all_routes = []
            for ant in range(self.num_ants):
                route = self.construct_route()
                all_routes.append(route)
                route_cost = self.calculate_cost(route)
                if route_cost < self.best_cost:
                    self.best_cost = route_cost
                    self.best_route = route
            self.update_pheromones(all_routes)
        return self.best_route, self.best_cost

    def construct_route(self):
        current_node = np.random.randint(0, self.graph.number_of_nodes())
        visited = [current_node]
        while len(visited) < self.graph.number_of_nodes():
            probabilities = self.calculate_probabilities(current_node, visited)
            if np.sum(probabilities) == 0:
                break
            next_node = np.random.choice(range(self.graph.number_of_nodes()), p=probabilities)
            visited.append(next_node)
            current_node = next_node
        visited.append(visited[0])  # Замыкаем маршрут
        return visited

    def calculate_probabilities(self, current_node, visited):
        pheromone = self.pheromone[current_node]
        visibility = []
        for neighbor in range(self.graph.number_of_nodes()):
            if neighbor not in visited and self.graph.has_edge(current_node, neighbor):
                visibility.append(1 / self.graph[current_node][neighbor]['weight'])
            else:
                visibility.append(0)
        visibility = np.array(visibility)
        total = np.sum((pheromone ** self.alpha) * (visibility ** self.beta))

        if total == 0:
            return np.zeros_like(pheromone)  # Вернуть нулевые вероятности, если нет доступных путей

        return (pheromone ** self.alpha) * (visibility ** self.beta) / total

    def calculate_cost(self, route):
        cost = 0
        for i in range(len(route) - 1):
            cost += self.graph.get_edge_data(route[i], route[i + 1], default={'weight': float('inf')})['weight']
        return cost

    def update_pheromones(self, all_routes):
        self.pheromone *= (1 - self.evaporation_rate)
        for route in all_routes:
            route_cost = self.calculate_cost(route)
            if route_cost > 0:
                pheromone_delta = self.Q / route_cost
                for i in range(len(route) - 1):
                    self.pheromone[route[i], route[i + 1]] += pheromone_delta

my_graph_data = [[0, 10, 15, 20],
                 [10, 0, 35, 25],
                 [15, 35, 0, 30],
                 [20, 25, 30, 0]]

travelsman_map = nx.Graph()

for i in range(len(my_graph_data)):
    for j in range(len(my_graph_data)):
        if my_graph_data[i][j] > 0 and j > i:
            travelsman_map.add_edge(i, j, weight=my_graph_data[i][j])

start = time.perf_counter()
ant_colony = AntColony(travelsman_map, num_ants=50, num_iterations=100, alpha=1, beta=2, evaporation_rate=0.1, Q=100)
best_route, best_cost = ant_colony.run()
finish = time.perf_counter()

# Переводим индексы в метки для удобства
best_route_labels = [x + 1 for x in best_route[:-1]]  # Убираем замыкание и переводим индексы на 1
print('Лучший маршрут: ' + str(best_route_labels))  # Выводим лучший маршрут
print('Стоимость: ' + str(best_cost))  # Выводим стоимость
print('Время работы: ' + str(round((finish - start) * 1000, 5)))  # Выводим время работы программы

pos = nx.spring_layout(travelsman_map)  # Устанавливаем расположение узлов графа
ax = plt.gca()  # Получаем текущую ось для графиков
ax.set_title('Лучший маршрут: ' + str(best_route_labels) + "\n Стоимость: " + str(best_cost))  # Устанавливаем заголовок графика
nx.draw_networkx(travelsman_map, pos, with_labels=True, node_size=1500, ax=ax)  # Рисуем граф
nx.draw_networkx_edge_labels(travelsman_map, pos, edge_labels=nx.get_edge_attributes(travelsman_map, 'weight'))  # Рисуем веса рёбер
plt.show()  # Отображаем график
