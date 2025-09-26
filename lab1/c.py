# file: C_variant21.py
import os
import numpy as np
import matplotlib.pyplot as plt

plt.style.use("seaborn-v0_8")
plt.rc("text", usetex=False)

script_dir = os.path.dirname(os.path.abspath(__file__))

g1, g2 = 1, 2

X=np.linspace(-1,20,1000)
line_upper=(1/6)*X - 1   # x2 <= (1/6)x1 - 1
line_lower=2*X + 2       # x2 >= 2x1 + 2

fig,ax=plt.subplots()
ax.quiver(0,0,g1,g2, angles="xy", scale_units="xy", scale=1,
          color="black", label=r"$\nabla F(x_1,x_2)$")

ax.plot(X,line_upper,label=r"$x_2=\frac{1}{6}x_1-1$")
ax.plot(X,line_lower,label=r"$x_2=2x_1+2$")
ax.plot(np.zeros_like(X),X,label=r"$x_1=0$")
ax.plot(X,np.zeros_like(X),label=r"$x_2=0$")

ax.fill_between(X,-20,line_upper,color="blue",alpha=0.2,
                label="Область: " + r"$x_2 \leq \frac{1}{6}x_1-1$")
ax.fill_between(X,line_lower,40,color="red",alpha=0.2,
                label="Область: " + r"$x_2 \geq 2x_1+2$")

ax.set_xlim(-0.1,10); ax.set_ylim(-0.1,10)
ax.set_xlabel("x1"); ax.set_ylabel("x2")
ax.legend(fontsize=10,loc="upper left")
ax.set_aspect("equal","box")
plt.title("Допустимая область отсутствует")
plt.tight_layout()
plt.savefig(os.path.join(script_dir, "03-graphic.png"), dpi=200)
plt.show()

print("Допустимая область пуста, решений нет.")
