import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Configuración de la app ---
st.set_page_config(layout="centered")
st.title("🧮 Simulación del Descenso del Gradiente con Deslizador")

# --- Función objetivo y derivada ---
def f(x):
    return x**2

def grad_f(x):
    return 2*x

# --- Parámetros de entrada ---
x0 = st.number_input("🔹 Valor inicial (x₀)", value=5.0)
lr = st.slider("🔸 Tasa de aprendizaje", 0.01, 1.0, 0.1)
max_iters = 50
iteraciones = st.slider("🎚️ Número de iteraciones", 0, max_iters, 10)

# --- Ejecutar el algoritmo hasta el número seleccionado ---
x_vals = [x0]
for i in range(iteraciones):
    x_actual = x_vals[-1]
    grad = grad_f(x_actual)
    x_nuevo = x_actual - lr * grad
    x_vals.append(x_nuevo)

y_vals = [f(x) for x in x_vals]

# --- Graficar ---
x_range = np.linspace(-10, 10, 400)
y_range = f(x_range)

fig, ax = plt.subplots()
ax.plot(x_range, y_range, label='f(x) = x²', color='blue')
ax.plot(x_vals, y_vals, 'ro-', label='Descenso del gradiente')

for i, (x_i, y_i) in enumerate(zip(x_vals, y_vals)):
    ax.annotate(f"{i}", (x_i, y_i), textcoords="offset points", xytext=(5,5), fontsize=8)

ax.set_title(f"Descenso del Gradiente - Iteraciones: {iteraciones}")
ax.set_xlabel("x")
ax.set_ylabel("f(x)")
ax.grid(True)
ax.legend()

st.pyplot(fig)

# --- Tabla de resultados ---
st.subheader("📋 Resultados por Iteración")
for i, (x_i, y_i) in enumerate(zip(x_vals, y_vals)):
    st.write(f"Iteración {i}: x = {x_i:.4f}, f(x) = {y_i:.4f}")
