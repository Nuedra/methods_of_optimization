# ЛР-8. Задача о назначениях (10x10). Венгерский алгоритм (минимизация).
# Ресурс i -> Объект j, минимизируем суммарную стоимость.

from typing import List, Tuple


C: List[List[int]] = [
    [1, 7, 7, 8, 8, 2, 5, 8, 4, 2],
    [5, 1, 2, 8, 7, 8, 8, 8, 3, 5],
    [6, 3, 9, 1, 8, 6, 4, 8, 5, 9],
    [9, 3, 5, 2, 7, 6, 8, 8, 9, 9],
    [9, 2, 1, 5, 4, 9, 8, 4, 6, 6],
    [9, 1, 5, 7, 5, 9, 9, 8, 5, 8],
    [1, 6, 3, 3, 7, 7, 8, 2, 8, 8],
    [3, 1, 7, 8, 5, 2, 2, 4, 7, 3],
    [1, 7, 7, 2, 6, 4, 5, 1, 6, 3],
    [5, 4, 6, 1, 4, 6, 7, 4, 1, 7],
]


def hungarian_min(cost: List[List[int]]) -> Tuple[List[int], int]:
    """
    Венгерский алгоритм (вариант с потенциалами), минимизация.
    Возвращает:
      assignment[i] = j (1..n -> 1..n), где i и j 1-индексные
      total_cost
    """
    n = len(cost)
    m = len(cost[0])
    if n != m:
        raise ValueError("Ожидается квадратная матрица n x n.")

    INF = 10**18
    u = [0] * (n + 1)      # потенциалы строк
    v = [0] * (m + 1)      # потенциалы столбцов
    p = [0] * (m + 1)      # p[j] = i, какая строка сейчас назначена на столбец j
    way = [0] * (m + 1)    # восстановление пути

    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = [INF] * (m + 1)
        used = [False] * (m + 1)

        while True:
            used[j0] = True
            i0 = p[j0]
            delta = INF
            j1 = 0

            for j in range(1, m + 1):
                if not used[j]:
                    cur = cost[i0 - 1][j - 1] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j

            for j in range(0, m + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta

            j0 = j1
            if p[j0] == 0:
                break

        # увеличиваем паросочетание
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break

    assignment = [0] * (n + 1)  # 1..n
    for j in range(1, m + 1):
        assignment[p[j]] = j

    total_cost = 0
    for i in range(1, n + 1):
        total_cost += cost[i - 1][assignment[i] - 1]

    return assignment, total_cost


def solve_and_print(cost: List[List[int]]) -> None:
    assignment, total = hungarian_min(cost)

    print("Оптимальное назначение (минимизация стоимости):")
    for i in range(1, len(cost) + 1):
        j = assignment[i]
        print(f"Ресурс {i:2d} -> Объект {j:2d}, стоимость = {cost[i-1][j-1]}")
    print(f"\nСуммарная стоимость: Z* = {total}")


if __name__ == "__main__":
    solve_and_print(C)

    # При желании можно сверить со SciPy (если установлен):
    try:
        import numpy as np
        from scipy.optimize import linear_sum_assignment

        r, c = linear_sum_assignment(np.array(C))
        check_cost = int(np.array(C)[r, c].sum())
        print("\nПроверка SciPy linear_sum_assignment:")
        print("Z* =", check_cost)
    except Exception:
        pass
