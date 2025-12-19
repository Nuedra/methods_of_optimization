from itertools import product

V = 6
P = {
    1: [0, 1, 2, 4, 5, 7, 8],
    2: [0, 2, 3, 3, 4, 5, 6],
    3: [0, 0, 2, 3, 5, 6, 6],
    4: [0, 1, 3, 5, 6, 7, 9],
    5: [0, 2, 2, 4, 4, 6, 7],
    6: [0, 1, 4, 4, 6, 8, 9],
}

best_val = -1
best_plans = []

for x in product(range(V + 1), repeat=6):
    if sum(x) == V:
        z = sum(P[i + 1][x[i]] for i in range(6))
        if z > best_val:
            best_val = z
            best_plans = [x]
        elif z == best_val:
            best_plans.append(x)

print("F_max =", best_val)
for i in range(len(best_plans)):
    print("Один из оптимальных планов:", best_plans[i])
print("Всего оптимальных планов:", len(best_plans))