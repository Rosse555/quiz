import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("🌀 Descenso del Gradiente 3D con Plotly (Vista Ampliada)")

# --- Función y gradiente ---
def f(x, y):
    return x**2 + y**2

def grad_f(x, y):
    return np.array([2*x, 2*y])

# --- Parámetros del usuario ---
x0 = st.number_input("🔹 x₀", value=3.0)
y0 = st.number_input("🔹 y₀", value=3.0)
lr = st.slider("🔸 Learning rate", 0.01, 1.0, 0.1)
iters = st.slider("🎚️ Iteraciones", 1, 50, 10)

# --- Algoritmo de descenso ---
points = [(x0, y0)]
x, y = x0, y0
for _ in range(iters):
    grad = grad_f(x, y)
    x -= lr * grad[0]
    y -= lr * grad[1]
    points.append((x, y))

traj_x = np.array([p[0] for p in points])
traj_y = np.array([p[1] for p in points])
traj_z = np.array([f(x, y) for x, y in points])

# --- Malla de la superficie ---
x_range = np.linspace(-5, 5, 100)
y_range = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x_range, y_range)
Z = f(X, Y)

# --- Crear figura con mayor tamaño ---
fig = go.Figure()

# Superficie 3D
fig.add_trace(go.Surface(
    z=Z, x=X, y=Y,
    colorscale="Viridis",
    opacity=0.7,
    name='f(x, y)'
))

# Trayectoria del descenso
fig.add_trace(go.Scatter3d(
    x=traj_x, y=traj_y, z=traj_z,
    mode='lines+markers',
    marker=dict(size=5, color='red'),
    line=dict(color='red', width=5),
    name='Descenso'
))

# Configuración del diseño
fig.update_layout(
    title="Simulación 3D del Descenso del Gradiente",
    width=1000,  # ancho personalizado
    height=700,  # alto personalizado
    scene=dict(
        xaxis_title='x',
        yaxis_title='y',
        zaxis_title='f(x, y)',
    )
)

# --- Mostrar figura más grande en Streamlit ---
st.plotly_chart(fig, use_container_width=False)
