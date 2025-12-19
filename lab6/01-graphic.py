# file: A_variant21_gomory_graphic.py
import os
import numpy as np
import matplotlib.pyplot as plt

plt.style.use("seaborn-v0_8")
plt.rc("text", usetex=False)

script_dir = os.path.dirname(os.path.abspath(__file__))

# F = 3 x1 + 2 x2
g1, g2 = 3, 2
def F(x1, x2):
    return g1 * x1 + g2 * x2

# Прямые:
# 1) 2x1 + x2 = 8   -> x2 = -2 x1 + 8
# 2) x1 + 3x2 = 6   -> x2 = -1/3 x1 + 2
# 3) x1 + x2 = 4    -> x2 = -x1 + 4 (отсечение Гомори)
# 4) x1 = 0
# 5) x2 = 0
a1, b1 = -2, 8
a2, b2 = -1/3, 2
a3, b3 = -1, 4              # x1 + x2 = 4
a4, b4 = float("inf"), 0    # x1 = 0
a5, b5 = 0, 0               # x2 = 0  -> x2 = 0 * x1 + 0

a = [a1, a2, a3, a4, a5]
b = [b1, b2, b3, b4, b5]

def find_intersection(a1, b1, a2, b2):
    # Пересечение прямых x2 = a1 x1 + b1 и x2 = a2 x1 + b2
    if a1 == float("inf") and a2 == float("inf"):
        return None
    if a1 == float("inf"):
        x1 = b1
        x2 = a2 * x1 + b2
        return (x1, x2)
    if a2 == float("inf"):
        x1 = b2
        x2 = a1 * x1 + b1
        return (x1, x2)
    if abs(a1 - a2) < 1e-12:
        return None
    x1 = (b2 - b1) / (a1 - a2)
    x2 = a1 * x1 + b1
    return (x1, x2)

def feasible(x1, x2):
    # Условия допустимой области:
    # 2x1 + x2 <= 8,  x1 + 3x2 <= 6,  x1 + x2 <= 4,  x1 >= 0, x2 >= 0
    return (
        x1 >= -1e-9 and
        x2 >= -1e-9 and
        x2 <= a1 * x1 + b1 + 1e-9 and
        x2 <= a2 * x1 + b2 + 1e-9 and
        x2 <= a3 * x1 + b3 + 1e-9
    )

X = np.linspace(-0.5, 5.5, 1000)
line1 = a1 * X + b1
line2 = a2 * X + b2
line3 = a3 * X + b3

fig, ax = plt.subplots()

# Вектор градиента
ax.quiver(
    0, 0, g1, g2,
    angles="xy", scale_units="xy", scale=1,
    color="black", label=r"$\nabla F(x_1,x_2)$"
)

# Прямые-границы
ax.plot(X, line1, label=r"$2x_1 + x_2 = 8$")
ax.plot(X, line2, label=r"$x_1 + 3x_2 = 6$")
ax.plot(X, line3, label=r"$x_1 + x_2 = 4$")
ax.plot(np.zeros_like(X), X, label=r"$x_1=0$")
ax.plot(X, np.zeros_like(X), label=r"$x_2=0$")

# Закрашиваем область, удовлетворяющую всем трём неравенствам
ax.fill_between(X, line1, -10, color="blue", alpha=0.15)
ax.fill_between(X, line2, -10, color="red", alpha=0.15)
ax.fill_between(X, line3, -10, color="green", alpha=0.15)

# Вершины допустимой области
pts = []
for i in range(len(a)):
    for j in range(i + 1, len(a)):
        p = find_intersection(a[i], b[i], a[j], b[j])
        if p and feasible(*p):
            pts.append(p)

# Убираем дубликаты
unique_pts = []
for p in pts:
    if not any(np.allclose(p, q, atol=1e-6) for q in unique_pts):
        unique_pts.append(p)
pts = unique_pts

for i, (x1, x2) in enumerate(pts, 1):
    ax.plot(x1, x2, "ko")
    ax.annotate(
        f'{i}: ({x1:.2f}, {x2:.2f})',
        xy=(x1, x2),
        xytext=(x1 + 0.2, x2 + 0.2),
        arrowprops=dict(facecolor="black", arrowstyle="->"),
        fontsize=9
    )

# Все целочисленные точки в допустимой области
int_pts = []
for x1 in range(0, 7):
    for x2 in range(0, 7):
        if feasible(x1, x2):
            int_pts.append((x1, x2))

if int_pts:
    xs_int, ys_int = zip(*int_pts)
    ax.scatter(xs_int, ys_int, marker="s", s=40,
               edgecolor="black", facecolor="black",
               label="Целочисленные допустимые точки")

ax.set_xlim(-0.1, 5.2)
ax.set_ylim(-0.1, 4.2)
ax.set_xlabel("x1")
ax.set_ylabel("x2")
ax.legend(fontsize=9, ncol=2)
ax.set_aspect("equal", "box")
plt.tight_layout()
plt.savefig(os.path.join(script_dir, "06-graphic-gomory-int.png"), dpi=200)
plt.show()

print("Вершины допустимой области:")
for i, (x1, x2) in enumerate(pts, 1):
    print(f"  Точка {i}: ({x1:.2f}, {x2:.2f}), F = {F(x1, x2):.2f}")

print("\nЦелочисленные допустимые точки:")
for (x1, x2) in int_pts:
    print(f"  ({x1}, {x2}), F = {F(x1, x2):.0f}")
