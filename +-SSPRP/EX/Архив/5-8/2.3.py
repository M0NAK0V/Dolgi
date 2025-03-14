import time
def unbounded_knapsack(weights, values, capacity):
    start_time = time.perf_counter()
    n = len(weights)
    dp = [0] * (capacity + 1)
    counts = [{} for _ in range(capacity + 1)]  # Для хранения количества предметов

    for i in range(n):
        for j in range(weights[i], capacity + 1):
            if dp[j - weights[i]] + values[i] > dp[j]:
                dp[j] = dp[j - weights[i]] + values[i]
                counts[j] = counts[j - weights[i]].copy()
                counts[j][i] = counts[j].get(i, 0) + 1

    # Восстановление выбранных предметов
    packed_items = {}
    for item_index, count in counts[capacity].items():
        packed_items[item_index] = {
            "weight": weights[item_index],
            "value": values[item_index],
            "count": count
        }

    # Вывод результатов
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print("Max value:", dp[capacity])
    print("Packed items:")
    for item_index, details in packed_items.items():
        print(f"Item {item_index}: Weight = {details['weight']}, Value = {details['value']}, Count = {details['count']}")
    print(f"Время выполнения алгоритма: {elapsed_time:.2f} секунд")


def unbounded_knapsack_brute_force(weights, values, capacity):
    start_time = time.perf_counter()
    n = len(weights)
    max_value = 0
    from itertools import product

    # Ограничиваем максимальное количество каждого предмета
    max_counts = [capacity // w for w in weights]

    # Перебор всех возможных комбинаций
    for counts in product(*[range(c + 1) for c in max_counts]):
        weight = sum(counts[i] * weights[i] for i in range(n))
        value = sum(counts[i] * values[i] for i in range(n))
        if weight <= capacity and value > max_value:
            max_value = value
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print("Max value:", max_value)
    print(f"Время выполнения алгоритма: {elapsed_time:.2f} секунд")


def unbounded_knapsack_meet_in_the_middle(weights, values, capacity):
    start_time = time.perf_counter()
    n = len(weights)
    half = n // 2

    # Генерация всех комбинаций для первой половины
    left = []
    from itertools import combinations_with_replacement
    for r in range(0, capacity // min(weights[:half]) + 1):
        for combo in combinations_with_replacement(range(half), r):
            weight = sum(weights[i] for i in combo)
            value = sum(values[i] for i in combo)
            if weight <= capacity:
                left.append((weight, value))

    # Генерация всех комбинаций для второй половины
    right = []
    for r in range(0, capacity // min(weights[half:]) + 1):
        for combo in combinations_with_replacement(range(half, n), r):
            weight = sum(weights[i] for i in combo)
            value = sum(values[i] for i in combo)
            if weight <= capacity:
                right.append((weight, value))

    # Сортировка правой половины по весу
    right.sort()
    # Удаление доминируемых решений (если вес больше, а ценность меньше)
    filtered_right = []
    max_value = -1
    for w, v in right:
        if v > max_value:
            filtered_right.append((w, v))
            max_value = v

    # Поиск оптимального решения
    max_total = 0
    for w1, v1 in left:
        remaining = capacity - w1
        # Бинарный поиск по filtered_right
        low, high = 0, len(filtered_right) - 1
        best = 0
        while low <= high:
            mid = (low + high) // 2
            if filtered_right[mid][0] <= remaining:
                best = filtered_right[mid][1]
                low = mid + 1
            else:
                high = mid - 1
        max_total = max(max_total, v1 + best)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print("Max value:", max_total)
    print(f"Время выполнения алгоритма: {elapsed_time:.2f} секунд")

weights = [2, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 3, 1, 3, 2, 1, 2, 1, 3, 1, 2, 1, 2, 3, 1, 2, 1, 3, 2, 3, 2, 3, 1, 1, 2, 3, 2, 1, 2, 3, 2, 3, 3, 2, 3, 2, 1, 3, 3, 1, 2, 1, 1, 1, 1, 2, 1, 3, 3, 2, 1, 2, 1, 1, 3, 2, 1, 3, 3, 2, 1, 3, 2, 1, 3, 1, 1, 1, 3, 2, 1, 1, 2, 2, 3, 3, 2, 2, 3, 2, 2, 2, 3, 1, 3, 3, 3, 2, 3, 3, 2, 2, 1, 3, 2, 2, 2, 2, 2, 3, 3, 3, 2, 2, 2, 3, 1, 2, 1, 1, 1, 1, 1, 3, 2, 2, 1, 1, 1, 1, 2, 1, 2, 1, 2, 3, 3, 2, 2, 2, 1, 2, 3, 1, 1, 3, 3, 3, 1, 3, 3, 3, 3, 2, 1, 1, 3, 2, 1, 1, 3, 1, 1, 1, 1, 2, 2, 3, 3, 3, 1, 1, 1, 3, 1, 1, 2, 2, 1, 1, 2, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2]
values = [499, 30, 263, 139, 224, 31, 13, 70, 273, 123, 405, 349, 23, 476, 82, 301, 169, 260, 168, 255, 83, 298, 107, 217, 95, 47, 381, 408, 260, 498, 368, 50, 388, 79, 255, 406, 288, 97, 82, 159, 244, 35, 38, 266, 422, 395, 191, 71, 67, 243, 82, 18, 98, 416, 126, 375, 192, 443, 450, 66, 30, 336, 357, 100, 468, 237, 371, 26, 334, 245, 241, 486, 122, 497, 91, 13, 294, 142, 380, 179, 268, 428, 168, 272, 465, 309, 416, 448, 99, 118, 402, 413, 137, 451, 303, 283, 82, 245, 238, 157, 187, 395, 223, 404, 420, 422, 333, 121, 354, 169, 437, 238, 98, 129, 173, 336, 330, 335, 20, 405, 268, 289, 202, 144, 409, 308, 255, 444, 456, 400, 64, 237, 151, 178, 230, 111, 417, 375, 393, 147, 304, 323, 112, 121, 25, 322, 69, 438, 433, 401, 485, 423, 181, 404, 64, 477, 381, 424, 340, 140, 137, 303, 383, 185, 241, 285, 333, 300, 345, 197, 113, 448, 63, 400, 377, 246, 232, 309, 41, 158, 65, 454, 15, 458, 370, 470, 281, 144, 24, 430, 54, 459, 372, 296, 153, 259, 482, 469, 320, 417]
capacity = 28

unbounded_knapsack(weights, values, capacity)
unbounded_knapsack_brute_force(weights, values, capacity)
unbounded_knapsack_meet_in_the_middle(weights, values, capacity)