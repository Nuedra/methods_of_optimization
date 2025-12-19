from itertools import product

# Данные задачи
M = 20
m = [2, 3, 4, 5, 7, 9]
p = [3, 4, 7, 8, 13, 17]
n = len(m)

# --- ДП (Беллман): B[i][x] = максимум с типов i+1..n при остатке x ---
B = [[0]*(M+1) for _ in range(n+1)]
U = [[0]*(M+1) for _ in range(n)]  # U[i][x] = оптимальное u_{i+1} при остатке x

for i in range(n-1, -1, -1):
    mi, pi = m[i], p[i]
    for x in range(M+1):
        best, bestu = -1, 0
        for u in range(x//mi + 1):
            val = u*pi + B[i+1][x - u*mi]
            if val > best:
                best, bestu = val, u
        B[i][x] = best
        U[i][x] = bestu

Z_star = B[0][M]

# восстановление плана
x = M
u_star = []
for i in range(n):
    u = U[i][x]
    u_star.append(u)
    x -= u*m[i]

print("DP: Z* =", Z_star)
print("DP: u* =", u_star)
print("DP: used_weight =", sum(u_star[i]*m[i] for i in range(n)))

# --- Brute force проверка ---
bounds = [M//mi for mi in m]
best_val = -1
best_u = None
best_w = None

for u in product(*[range(b+1) for b in bounds]):
    w = sum(u[i]*m[i] for i in range(n))
    if w <= M:
        val = sum(u[i]*p[i] for i in range(n))
        if val > best_val:
            best_val, best_u, best_w = val, u, w

print("Bruteforce: Z* =", best_val)
print("Bruteforce: u* =", list(best_u))
print("Bruteforce: used_weight =", best_w)
