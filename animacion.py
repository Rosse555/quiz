import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

st.set_page_config(layout="centered")
st.title("🌄 Simulación 3D del Descenso del Gradiente (Varias Funciones)")

# --- Definir funciones y gradientes ---
def f1(x, y): return x**2 + y**2
def g1(x, y): return np.array([2*x, 2*y])

def f2(x, y): return x**2 + 2*y**2
def g2(x, y): return np.array([2*x, 4*y])

def f3(x, y): return (x - 2)**2 + (y + 3)**2
def g3(x, y): return np.array([2*(x - 2), 2*(y + 3)])

def f4(x, y): return np.sin(x) + np.cos(y)
def g4(x, y): return np.array([np.cos(x), -np.sin(y)])

def f5(x, y): return np.exp(x**2 + y**2)
def g5(x, y): return np.array([2*x*np.exp(x**2 + y**2), 2*y*np.exp(x**2 + y**2)])

funciones = {
    "x² + y²": (f1, g1),
    "x² + 2y²": (f2, g2),
    "(x - 2)² + (y + 3)²": (f3, g3),
    "sin(x) + cos(y)": (f4, g4),
    "exp(x² + y²)": (f5, g5)
}

# --- Selección de función ---
seleccion = st.selectbox("📌 Selecciona una función", list(funciones.keys()))
f, grad_f = funciones[seleccion]

# --- Parámetros del usuario ---
x0 = st.number_input("🔹 Valor inicial x₀", value=2.0)
y0 = st.number_input("🔹 Valor inicial y₀", value=2.0)
lr = st.slider("🔸 Tasa de aprendizaje", 0.01, 1.0, 0.1)
max_iters = 50
iteraciones = st.slider("🎚️ Número de iteraciones", 1, max_iters, 10)

# --- Descenso del gradiente ---
points = [(x0, y0)]
x, y = x0, y0
for _ in range(iteraciones):
    grad = grad_f(x, y)
    x -= lr * grad[0]
    y -= lr * grad[1]
    points.append((x, y))

traj_x = np.array([p[0] for p in points])
traj_y = np.array([p[1] for p in points])
traj_z = np.array([f(x, y) for x, y in points])

# --- Grilla para superficie 3D ---
X = np.linspace(-5, 5, 100)
Y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(X, Y)
Z = f(X, Y)

# --- Gráfico 3D ---
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')

# Superficie
ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.6)
# Trayectoria
ax.plot(traj_x, traj_y, traj_z, 'ro-', label='Trayectoria')
ax.scatter(traj_x[0], traj_y[0], traj_z[0], color='red', s=50, label='Inicio')
ax.scatter(traj_x[-1], traj_y[-1], traj_z[-1], color='green', s=50, label='Final')

ax.set_title(f"Descenso del Gradiente sobre: {seleccion}")
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('f(x, y)')
ax.legend()

st.pyplot(fig)

# --- Mostrar tabla de resultados ---
st.subheader("📋 Coordenadas por Iteración")
for i, (x_i, y_i, z_i) in enumerate(zip(traj_x, traj_y, traj_z)):
    st.write(f"Iteración {i}: x = {x_i:.4f}, y = {y_i:.4f}, f(x, y) = {z_i:.4f}")
