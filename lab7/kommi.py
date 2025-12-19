import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

import sys

if not sys.warnoptions:
    import warnings

    warnings.simplefilter("ignore")

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)


# ------------------------------------------------------------------------------------
def distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


# ------------------------------------------------------------------------------------
def in_deep_matrix(p, y, x):
    # Возвращает новую матрицу меньшего размера, за вычитом строки и столбца
    return p.drop([y], axis=0).drop([x], axis=1)


# ------------------------------------------------------------------------------------
def reduction_matrix(p):
    # Производим редуцирование матрицы, возвращаем нижнюю границу
    bottom_line = 0

    # Находим минимум по каждой строке и вычитаем его
    for index, row in p.iterrows():
        min = row.min()
        if np.isinf(min):
            return np.inf
        bottom_line += min
        for key, value in row.items():
            p.at[index, key] -= min

    # Находим минимум по каждому столбцу и вычитаем его
    for key, value in p.items():
        min = value.min()
        if np.isinf(min):
            return np.inf
        bottom_line += min
        for index, row in value.items():
            p.at[index, key] -= min

    return bottom_line


# ------------------------------------------------------------------------------------
def partition_matrix(p):
    # Ищем элемент для разбиения матрицы на m1 и m2
    # Для этого производим оценку нулевых элементов матрицы
    max_sum = 0
    index_i = None
    index_j = None
    for index in p.index:
        for key in p.columns:
            if p[key][index] == 0:
                min_i = np.inf
                min_j = np.inf

                for k, v in p[key].items():  # по столбецу
                    if k != index and v < min_i:
                        min_i = v

                for k, v in p.loc[index].items():
                    if k != key and v < min_j:
                        min_j = v

                l = min_i + min_j
                if l > max_sum:
                    max_sum = l
                    index_i = index
                    index_j = key

    return [index_i, index_j, max_sum]


# ------------------------------------------------------------------------------------
def reverse_index(l, i, j):
    # Находим обрытный индекс для матрицы
    def in_dict(d, v):
        while v in d:
            v = d[v]
        return v

    ln = len(l)
    d1 = {l[k][0]: l[k][1] for k in range(0, ln, 1)}
    d2 = {l[k][1]: l[k][0] for k in range(0, ln, 1)}
    return [in_dict(d1, i), in_dict(d2, j)]


# ------------------------------------------------------------------------------------
def evaluation_matrix(p, res, bottom_line):
    # Оценка матрицы, поиск решения
    if len(p) == 1:
        res["steps"] += 1
        bottom_line += p.iat[0, 0]

        # Если текущее решение лучше, запоминаем его
        if bottom_line < res["global_min"]:
            res["global_min"] = bottom_line
            res["local_result"].append([p.index[0], p.columns[0]])
            res["best_result"] = res["local_result"].copy()
            print(
                "Решение лучше:", bottom_line, res["best_result"], "шаг: ", res["steps"]
            )
        return

    # Производим редуцирование матрицы, возвращаем минимальную нижнюю границу
    bottom_line += reduction_matrix(p)
    if np.isinf(bottom_line):
        return

    max_sum = 0
    while True:
        res["steps"] += 1
        # Находим элемент для разбиения на подмножества m1 и m2
        i, j, max_sum = partition_matrix(p)
        # Больше нет элементов для разбиения
        if i is None:
            return

        v_len = len(res["local_result"])
        # Рассматриваем m1 (соглашаемся на разбиение по элементу)
        if bottom_line < res["global_min"]:
            res["local_result"].append([i, j])
            p1 = in_deep_matrix(p, i, j)
            # Вычёркиваем обратный элемент только для матрицы большей чем 2х2, чтоб не получить inf
            if len(p1) > 2:
                i_reverse, j_reverse = reverse_index(res["local_result"], i, j)
                p1[j_reverse][i_reverse] = np.inf
            evaluation_matrix(p1, res, bottom_line)

        # Рассматриваем m2
        if res["global_min"] < bottom_line + max_sum:
            return
        p[j][i] = np.inf  # Исключаем не выбранный элемент
        res["local_result"] = res["local_result"][:v_len]  # Обрезаем список пути


# ------------------------------------------------------------------------------------
def return_res(res):
    l = res["best_result"]
    if l:
        d = {l[k][0]: l[k][1] for k in range(len(l))}
        li = []
        a = l[0][0]
        for v in range(len(l)):
            li.append(a)
            a = d[a]
        return li
    else:
        return []


n = 10
input_matrix = [
    [float("inf"), 88, 77, 67, 31, 40, 80, 4, 74, 56],
    [5, float("inf"), 41, 6, 91, 25, 91, 56, 33, 27],
    [92, 79, float("inf"), 94, 87, 69, 22, 47, 89, 85],
    [9, 53, 41, float("inf"), 56, 54, 85, 74, 56, 36],
    [10, 56, 69, 8, float("inf"), 12, 42, 60, 99, 10],
    [45, 45, 67, 58, 1, float("inf"), 56, 95, 15, 49],
    [87, 97, 79, 76, 91, 65, float("inf"), 25, 79, 19],
    [12, 21, 5, 92, 93, 63, 42, float("inf"), 56, 7],
    [89, 79, 37, 23, 3, 63, 7, 51, float("inf"), 33],
    [63, 69, 54, 26, 27, 38, 7, 81, 94, float("inf")],
]

f1 = pd.DataFrame(input_matrix)

print("\nИсходная матрица расстояний:")
print(f1.to_string())

# --- Инициализация массива решений ---
res = {"global_min": np.inf, "best_result": [], "local_result": [], "steps": 0}

# --- Запуск решения ---
evaluation_matrix(f1, res, 0)

# --- Формирование результата ---
best_path = list(np.array(return_res(res)) + 1)
best_path_str = " → ".join(map(str, best_path))

print("\n===== Результаты решения задачи коммивояжера =====")
print(f"Минимальная длина маршрута: {res['global_min']}")
print(f"Лучший путь: {best_path_str}")
print(f"Количество шагов алгоритма: {res['steps']}")

# --- Табличное представление ---
df = pd.DataFrame({
    "Результат (длина маршрута)": [res["global_min"]],
    "Путь": [best_path_str],
    "Шагов": [res["steps"]]
})

print("\nТабличный вывод:")
print(df.to_string(index=False))
