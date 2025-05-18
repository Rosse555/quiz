import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("🌀 Descenso del Gradiente 3D Paso a Paso")

# --- Función objetivo y su gradiente ---
def f(x, y): return x**2 + y**2
def grad_f(x, y): return np.array([2*x, 2*y])

# --- Entrada de parámetros ---
x0 = st.number_input("🔹 x₀", value=3.0)
y0 = st.number_input("🔹 y₀", value=3.0)
lr = st.slider("🔸 Learning rate", 0.01, 1.0, 0.1)
max_iters = st.slider("🎚️ Iteraciones máximas", 1, 50, 10)

# --- Inicializar estado de la simulación ---
if 'points' not in st.session_state:
    st.session_state.points = [(x0, y0)]
    st.session_state.iter = 0
    st.session_state.x0 = x0
    st.session_state.y0 = y0

# --- Reiniciar simulación si cambian los valores iniciales ---
if st.session_state.x0 != x0 or st.session_state.y0 != y0:
    st.session_state.points = [(x0, y0)]
    st.session_state.iter = 0
    st.session_state.x0 = x0
    st.session_state.y0 = y0

# --- Botón para avanzar paso a paso ---
if st.button("▶️ Siguiente iteración"):
    if st.session_state.iter < max_iters:
        x, y = st.session_state.points[-1]
        grad = grad_f(x, y)
        x_new = x - lr * grad[0]
        y_new = y - lr * grad[1]
        st.session_state.points.append((x_new, y_new))
        st.session_state.iter += 1

# --- Extraer puntos de trayectoria ---
traj_x = np.array([p[0] for p in st.session_state.points])
traj_y = np.array([p[1] for p in st.session_state.points])
traj_z = np.array([f(x, y) for x, y in st.session_state.points])

# --- Superficie de la función ---
X = np.linspace(-5, 5, 100)
Y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(X, Y)
Z = f(X, Y)

fig = go.Figure()

# Superficie
fig.add_trace(go.Surface(z=Z, x=X, y=Y, colorscale="Viridis", opacity=0.7))

# Trayectoria
fig.add_trace(go.Scatter3d(
    x=traj_x, y=traj_y, z=traj_z,
    mode='lines+markers',
    marker=dict(size=5, color='red'),
    line=dict(color='red', width=4),
    name="Descenso"
))

# Puntos inicial y final
fig.add_trace(go.Scatter3d(
    x=[traj_x[0]], y=[traj_y[0]], z=[traj_z[0]],
    mode='markers',
    marker=dict(size=8, color='orange'),
    name="Inicio"
))
fig.add_trace(go.Scatter3d(
    x=[traj_x[-1]], y=[traj_y[-1]], z=[traj_z[-1]],
    mode='markers',
    marker=dict(size=8, color='green'),
    name="Último punto"
))

# Configuración
fig.update_layout(
    title=f"Iteración: {st.session_state.iter}",
    width=1000,
    height=700,
    scene=dict(
        xaxis_title='x',
        yaxis_title='y',
        zaxis_title='f(x, y)'
    ),
    legend=dict(
        x=0.8,  # horizontal (0 a 1)
        y=0.95, # vertical (0 a 1)
        bgcolor='rgba(255,255,255,0.7)',
        bordercolor='black',
        borderwidth=1
    )
)


# --- Mostrar gráfica ---
st.plotly_chart(fig, use_container_width=False)

# --- Mostrar resultados ---
st.subheader("📋 Valores por iteración")
for i, (x_i, y_i, z_i) in enumerate(zip(traj_x, traj_y, traj_z)):
    st.write(f"Iteración {i}: x = {x_i:.4f}, y = {y_i:.4f}, f(x, y) = {z_i:.4f}")
