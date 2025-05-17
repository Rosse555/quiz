import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="centered")
st.title("🔽 Descenso del Gradiente en 2D con Curvas de Nivel")

# --- Función objetivo y gradiente ---
def f(x, y):
    return x**2 + y**2

def grad_f(x, y):
    return np.array([2*x, 2*y])

# --- Entradas del usuario ---
x0 = st.number_input("🔹 Valor inicial x₀", value=3.0)
y0 = st.number_input("🔹 Valor inicial y₀", value=3.0)
lr = st.slider("🔸 Tasa de aprendizaje", 0.01, 1.0, 0.1)
max_iters = 50
iteraciones = st.slider("🎚️ Número de iteraciones", 1, max_iters, 10)

# --- Ejecutar descenso del gradiente ---
points = [(x0, y0)]
x, y = x0, y0

for _ in range(iteraciones):
    grad = grad_f(x, y)
    x = x - lr * grad[0]
    y = y - lr * grad[1]
    points.append((x, y))

# --- Preparar curva de nivel ---
x_vals = np.linspace(-5, 5, 400)
y_vals = np.linspace(-5, 5, 400)
X, Y = np.meshgrid(x_vals, y_vals)
Z = f(X, Y)

# --- Graficar curvas de nivel ---
fig, ax = plt.subplots()
contours = ax.contour(X, Y, Z, levels=20, cmap='viridis')
ax.clabel(contours, inline=True, fontsize=8)

# --- Dibujar trayectoria del descenso ---
traj_x = [pt[0] for pt in points]
traj_y = [pt[1] for pt in points]
ax.plot(traj_x, traj_y, 'ro-', label="Trayectoria del descenso")
ax.set_title(f"Descenso del Gradiente con Curvas de Nivel ({iteraciones} iteraciones)")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# --- Mostrar valores ---
st.subheader("📋 Coordenadas por Iteración")
for i, (x_i, y_i) in enumerate(points):
    z_i = f(x_i, y_i)
    st.write(f"Iteración {i}: x = {x_i:.4f}, y = {y_i:.4f}, f(x, y) = {z_i:.4f}")
