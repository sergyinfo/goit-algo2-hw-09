import random
import math


# Визначення функції Сфери
def sphere_function(x):
    """
    Обчислює значення функції Сфери f(x) = ∑(xi^2).
    """
    return sum(xi ** 2 for xi in x)


# Алгоритм «Підйом на гору» (Hill Climbing)
def hill_climbing(func, bounds, iterations=1000, epsilon=1e-6, step_size=0.1):
    """
    Мінімізує функцію за допомогою алгоритму Hill Climbing.

    Аргументи:
    func -- цільова функція для мінімізації.
    bounds -- список кортежів (min, max) для кожної змінної.
    iterations -- максимальна кількість ітерацій.
    epsilon -- точність для умови зупинки.
    step_size -- розмір кроку для пошуку сусідніх рішень.

    Повертає:
    Кортеж (оптимальна точка, значення функції).
    """
    # 1. Початкова точка
    current_solution = [random.uniform(b[0], b[1]) for b in bounds]
    current_value = func(current_solution)

    for _ in range(iterations):
        previous_value = current_value

        # 2. Генерація сусідньої точки
        neighbor = list(current_solution)
        for i in range(len(neighbor)):
            # Робимо невеликий крок у випадковому напрямку
            neighbor[i] += random.uniform(-step_size, step_size)
            # Перевірка, чи не вийшли за межі
            neighbor[i] = max(bounds[i][0], min(bounds[i][1], neighbor[i]))

        # 3. Оцінка сусідньої точки
        neighbor_value = func(neighbor)

        # 4. Якщо сусідня точка краща, переходимо до неї
        if neighbor_value < current_value:
            current_solution = neighbor
            current_value = neighbor_value

        # 5. Умова зупинки
        if abs(previous_value - current_value) < epsilon:
            break

    return current_solution, current_value


# Випадковий локальний пошук (Random Local Search)
def random_local_search(func, bounds, iterations=1000, epsilon=1e-6):
    """
    Мінімізує функцію за допомогою випадкового локального пошуку.

    Аргументи:
    func -- цільова функція для мінімізації.
    bounds -- список кортежів (min, max) для кожної змінної.
    iterations -- максимальна кількість ітерацій.
    epsilon -- точність для умови зупинки.

    Повертає:
    Кортеж (найкраща знайдена точка, значення функції).
    """
    # 1. Початкова точка
    best_solution = [random.uniform(b[0], b[1]) for b in bounds]
    best_value = func(best_solution)

    for _ in range(iterations):
        previous_best_value = best_value

        # 2. Генеруємо абсолютно нову випадкову точку
        candidate_solution = [random.uniform(b[0], b[1]) for b in bounds]
        candidate_value = func(candidate_solution)

        # 3. Якщо нова точка краща, оновлюємо найкращий розв'язок
        if candidate_value < best_value:
            best_solution = candidate_solution
            best_value = candidate_value

        # 4. Умова зупинки
        if abs(previous_best_value - best_value) < epsilon:
            break

    return best_solution, best_value


# Імітація відпалу (Simulated Annealing)
def simulated_annealing(func, bounds, iterations=1000, temp=1000.0, cooling_rate=0.99, epsilon=1e-6):
    """
    Мінімізує функцію за допомогою імітації відпалу.

    Аргументи:
    func -- цільова функція для мінімізації.
    bounds -- список кортежів (min, max) для кожної змінної.
    iterations -- максимальна кількість ітерацій.
    temp -- початкова температура.
    cooling_rate -- коефіцієнт охолодження.
    epsilon -- точність для умови зупинки (мінімальна температура).

    Повертає:
    Кортеж (найкраща знайдена точка, значення функції).
    """
    # 1. Початкова точка
    current_solution = [random.uniform(b[0], b[1]) for b in bounds]
    current_value = func(current_solution)
    best_solution, best_value = current_solution, current_value

    for _ in range(iterations):
        # 2. Генеруємо сусідню точку
        neighbor = list(current_solution)
        dim_to_change = random.randint(0, len(bounds) - 1)
        neighbor[dim_to_change] += random.uniform(-1, 1)
        neighbor[dim_to_change] = max(bounds[dim_to_change][0], min(bounds[dim_to_change][1], neighbor[dim_to_change]))

        neighbor_value = func(neighbor)

        # 3. Рішення про перехід
        delta = neighbor_value - current_value
        if delta < 0:  # Якщо рішення краще - приймаємо
            current_solution, current_value = neighbor, neighbor_value
        else:
            # Якщо рішення гірше - приймаємо з певною ймовірністю
            probability = math.exp(-delta / temp)
            if random.random() < probability:
                current_solution, current_value = neighbor, neighbor_value

        # Оновлюємо найкращий знайдений розв'язок
        if current_value < best_value:
            best_solution, best_value = current_solution, current_value

        # 4. Охолодження
        temp *= cooling_rate

        # 5. Умова зупинки
        if temp < epsilon:
            break

    return best_solution, best_value


if __name__ == "__main__":
    # Межі для функції
    bounds = [(-5, 5), (-5, 5)]

    # Виконання алгоритмів
    print("Hill Climbing:")
    hc_solution, hc_value = hill_climbing(sphere_function, bounds)
    print(f"Розв'язок: {hc_solution}, Значення: {hc_value}")

    print("\nRandom Local Search:")
    rls_solution, rls_value = random_local_search(sphere_function, bounds)
    print(f"Розв'язок: {rls_solution}, Значення: {rls_value}")

    print("\nSimulated Annealing:")
    sa_solution, sa_value = simulated_annealing(sphere_function, bounds)
    print(f"Розв'язок: {sa_solution}, Значення: {sa_value}")