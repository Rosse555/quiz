import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="centered")
st.title("🎬 Simulación del Descenso del Gradiente Paso a Paso")

# --- Función objetivo y su derivada ---
def f(x):
    return x**2

def grad_f(x):
    return 2*x

# --- Inicialización en la sesión ---
if 'x_vals' not in st.session_state:
    st.session_state.x_vals = []
    st.session_state.iter = 0

# --- Parámetros de entrada ---
x0 = st.number_input("Valor inicial (x₀)", value=5.0)
lr = st.slider("Tasa de aprendizaje (learning rate)", 0.01, 1.0, 0.1)

# --- Inicializar (botón reset) ---
if st.button("🔁 Reiniciar"):
    st.session_state.x_vals = [x0]
    st.session_state.iter = 0

# --- Avanzar una iteración (botón Play) ---
if st.button("▶️ Play"):
    if len(st.session_state.x_vals) == 0:
        st.session_state.x_vals.append(x0)

    x_actual = st.session_state.x_vals[-1]
    grad = grad_f(x_actual)
    x_nuevo = x_actual - lr * grad
    st.session_state.x_vals.append(x_nuevo)
    st.session_state.iter += 1

# --- Obtener valores actuales ---
x_vals = st.session_state.x_vals
y_vals = [f(x) for x in x_vals]

# --- Gráfico ---
x_range = np.linspace(-10, 10, 400)
y_range = f(x_range)

fig, ax = plt.subplots()
ax.plot(x_range, y_range, label='f(x) = x²', color='blue')
if len(x_vals) > 1:
    ax.plot(x_vals, y_vals, 'ro-', label='Trayectoria')
    for i, (xi, yi) in enumerate(zip(x_vals, y_vals)):
        ax.annotate(f"{i}", (xi, yi), textcoords="offset points", xytext=(5,5), ha='center')

ax.set_title(f"Descenso del Gradiente - Iteración {st.session_state.iter}")
ax.set_xlabel("x")
ax.set_ylabel("f(x)")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# --- Mostrar tabla de iteraciones ---
st.subheader("📋 Valores por iteración")
for i, (x, y) in enumerate(zip(x_vals, y_vals)):
    st.write(f"Iteración {i}: x = {x:.4f}, f(x) = {y:.4f}")
