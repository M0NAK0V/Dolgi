import random

class AntColonyKnapsack:
    def __init__(self, weights, values, capacity, max_iter=100, num_ants=10, alpha=1, beta=2, evaporation_rate=0.5):
        self.weights = weights
        self.values = values
        self.capacity = capacity
        self.max_iter = max_iter
        self.num_ants = num_ants
        self.alpha = alpha  # Влияние феромонов
        self.beta = beta    # Влияние эвристической информации
        self.evaporation_rate = evaporation_rate
        self.num_items = len(weights)
        self.pheromones = [1.0] * self.num_items  # Инициализация феромонов

    def heuristic(self, item):
        # Эвристическая информация: соотношение ценности к весу
        return self.values[item] / self.weights[item]

    def select_item(self, available_items, remaining_capacity):
        # Выбор предмета на основе феромонов и эвристической информации
        probabilities = []
        total = 0
        for item in available_items:
            if self.weights[item] <= remaining_capacity:
                pheromone = self.pheromones[item] ** self.alpha
                heuristic = self.heuristic(item) ** self.beta
                probabilities.append((item, pheromone * heuristic))
                total += pheromone * heuristic
        if total == 0:
            return None
        # Нормализация вероятностей
        probabilities = [(item, prob / total) for item, prob in probabilities]
        # Выбор предмета на основе вероятностей
        r = random.random()
        cumulative = 0
        for item, prob in probabilities:
            cumulative += prob
            if r <= cumulative:
                return item
        return None

    def construct_solution(self):
        solution = []
        remaining_capacity = self.capacity
        while True:
            item = self.select_item(list(range(self.num_items)), remaining_capacity)
            if item is None:
                break
            solution.append(item)
            remaining_capacity -= self.weights[item]
            if remaining_capacity <= 0:
                break
        return solution

    def evaluate_solution(self, solution):
        # Оценка решения (суммарная ценность)
        total_value = sum(self.values[item] for item in solution)
        total_weight = sum(self.weights[item] for item in solution)
        if total_weight > self.capacity:
            return 0  # Недопустимое решение
        return total_value

    def update_pheromones(self, solutions):
        # Испарение феромонов
        for i in range(self.num_items):
            self.pheromones[i] *= (1 - self.evaporation_rate)
        # Обновление феромонов на основе лучших решений
        for solution in solutions:
            solution_value = self.evaluate_solution(solution)
            for item in solution:
                self.pheromones[item] += solution_value

    def solve(self):
        best_solution = []
        best_value = 0
        for iteration in range(self.max_iter):
            solutions = []
            for _ in range(self.num_ants):
                solution = self.construct_solution()
                solutions.append(solution)
                solution_value = self.evaluate_solution(solution)
                if solution_value > best_value:
                    best_value = solution_value
                    best_solution = solution
            self.update_pheromones(solutions)
        
        # Вывод результатов
        total_weight = sum(self.weights[item] for item in best_solution)
        total_value = sum(self.values[item] for item in best_solution)
        print("Max value:", total_value)
        print("Total weight:", total_weight)
        print("Packed items:")
        for item in best_solution:
            print(f"Item {item}: Weight = {self.weights[item]}, Value = {self.values[item]}")
        
        return best_solution, best_value

# Пример использования:
weights = [2, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 3, 1, 3, 2, 1, 2, 1, 3, 1, 2, 1, 2, 3, 1, 2, 1, 3, 2, 3, 2, 3, 1, 1, 2, 3, 2, 1, 2, 3, 2, 3, 3, 2, 3, 2, 1, 3, 3, 1, 2, 1, 1, 1, 1, 2, 1, 3, 3, 2, 1, 2, 1, 1, 3, 2, 1, 3, 3, 2, 1, 3, 2, 1, 3, 1, 1, 1, 3, 2, 1, 1, 2, 2, 3, 3, 2, 2, 3, 2, 2, 2, 3, 1, 3, 3, 3, 2, 3, 3, 2, 2, 1, 3, 2, 2, 2, 2, 2, 3, 3, 3, 2, 2, 2, 3, 1, 2, 1, 1, 1, 1, 1, 3, 2, 2, 1, 1, 1, 1, 2, 1, 2, 1, 2, 3, 3, 2, 2, 2, 1, 2, 3, 1, 1, 3, 3, 3, 1, 3, 3, 3, 3, 2, 1, 1, 3, 2, 1, 1, 3, 1, 1, 1, 1, 2, 2, 3, 3, 3, 1, 1, 1, 3, 1, 1, 2, 2, 1, 1, 2, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2]
values = [499, 30, 263, 139, 224, 31, 13, 70, 273, 123, 405, 349, 23, 476, 82, 301, 169, 260, 168, 255, 83, 298, 107, 217, 95, 47, 381, 408, 260, 498, 368, 50, 388, 79, 255, 406, 288, 97, 82, 159, 244, 35, 38, 266, 422, 395, 191, 71, 67, 243, 82, 18, 98, 416, 126, 375, 192, 443, 450, 66, 30, 336, 357, 100, 468, 237, 371, 26, 334, 245, 241, 486, 122, 497, 91, 13, 294, 142, 380, 179, 268, 428, 168, 272, 465, 309, 416, 448, 99, 118, 402, 413, 137, 451, 303, 283, 82, 245, 238, 157, 187, 395, 223, 404, 420, 422, 333, 121, 354, 169, 437, 238, 98, 129, 173, 336, 330, 335, 20, 405, 268, 289, 202, 144, 409, 308, 255, 444, 456, 400, 64, 237, 151, 178, 230, 111, 417, 375, 393, 147, 304, 323, 112, 121, 25, 322, 69, 438, 433, 401, 485, 423, 181, 404, 64, 477, 381, 424, 340, 140, 137, 303, 383, 185, 241, 285, 333, 300, 345, 197, 113, 448, 63, 400, 377, 246, 232, 309, 41, 158, 65, 454, 15, 458, 370, 470, 281, 144, 24, 430, 54, 459, 372, 296, 153, 259, 482, 469, 320, 417]
capacity = 28
aco = AntColonyKnapsack(weights, values, capacity)
best_solution, best_value = aco.solve()