# file: A_variant21.py
import os
import numpy as np
import matplotlib.pyplot as plt

plt.style.use("seaborn-v0_8")
plt.rc("text", usetex=False)

script_dir = os.path.dirname(os.path.abspath(__file__))

g1, g2 = 3, 2  # F = 3x1 + 2x2
def F(x1, x2): return g1*x1 + g2*x2

# Прямые
a1, b1 = -2, 8       # 2x1 + x2 = 8
a2, b2 = -1/3, 2     # x1 + 3x2 = 6
a3, b3 = float("inf"), 0
a4, b4 = 0, 0
a = [a1, a2, a3, a4]; b = [b1, b2, b3, b4]

def find_intersection(a1, b1, a2, b2):
    if a1==float("inf") and a2==float("inf"): return None
    if a1==float("inf"): return (b1, a2*b1+b2)
    if a2==float("inf"): return (b2, a1*b2+b1)
    if abs(a1-a2)<1e-12: return None
    x1=(b2-b1)/(a1-a2); x2=a1*x1+b1; return (x1,x2)

def feasible(x1, x2):
    return (x1>=0 and x2>=0 and x2<=a1*x1+b1+1e-9 and x2<=a2*x1+b2+1e-9)

X = np.linspace(-1, 6, 1000)
line1 = a1*X+b1
line2 = a2*X+b2

fig, ax = plt.subplots()
ax.quiver(0,0,g1,g2, angles="xy", scale_units="xy", scale=1,
          color="black", label=r"$\nabla F(x_1,x_2)$")

ax.plot(X,line1,label=r"$x_2=-2x_1+8$")
ax.plot(X,line2,label=r"$x_2=-\frac{1}{3}x_1+2$")
ax.plot(np.zeros_like(X),X,label=r"$x_1=0$")
ax.plot(X,np.zeros_like(X),label=r"$x_2=0$")

ax.fill_between(X,line1,-10,color="blue",alpha=0.2,
                label="Область: " + r"$x_2 \leq -2x_1+8$")
ax.fill_between(X,line2,-10,color="red",alpha=0.2,
                label="Область: " + r"$x_2 \leq -\frac{1}{3}x_1+2$")

pts=[]
for i in range(len(a)):
    for j in range(i+1,len(a)):
        p=find_intersection(a[i],b[i],a[j],b[j])
        if p and feasible(*p): pts.append(p)

for i,(x1,x2) in enumerate(pts,1):
    ax.plot(x1,x2,'ko')
    ax.annotate(f'{i}: ({x1:.2f},{x2:.2f})',xy=(x1,x2),
                xytext=(x1+0.3,x2+0.4),
                arrowprops=dict(facecolor='black',arrowstyle='->'))

ax.set_xlim(-0.1,5.2); ax.set_ylim(-0.1,3.2)
ax.set_xlabel("x1"); ax.set_ylabel("x2")
ax.legend(fontsize=10,ncol=2)
ax.set_aspect("equal","box")
plt.tight_layout()
plt.savefig(os.path.join(script_dir, "01-graphic.png"), dpi=200)
plt.show()

for i,(x1,x2) in enumerate(pts,1):
    print(f"Точка {i}: F={F(x1,x2):.2f}")
