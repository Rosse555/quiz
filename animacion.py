import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configurar la interfaz
st.set_page_config(layout="centered")
st.title("🔽 Simulación del Descenso del Gradiente")

# Definimos la función y su derivada
def f(x):
    return x**2

def grad_f(x):
    return 2*x

# Parámetros de entrada
x0 = st.slider("Valor inicial (x₀)", -10.0, 10.0, value=5.0)
lr = st.slider("Tasa de aprendizaje (learning rate)", 0.001, 1.0, value=0.1)
iteraciones = st.slider("Número de iteraciones", 1, 50, value=10)

# Ejecutar descenso del gradiente
x_vals = [x0]
for _ in range(iteraciones):
    x_actual = x_vals[-1]
    grad = grad_f(x_actual)
    x_nuevo = x_actual - lr * grad
    x_vals.append(x_nuevo)

y_vals = [f(x) for x in x_vals]

# Crear gráfica
x_range = np.linspace(-10, 10, 400)
y_range = f(x_range)

fig, ax = plt.subplots()
ax.plot(x_range, y_range, label='f(x) = x²', color='blue')
ax.plot(x_vals, y_vals, 'ro-', label='Descenso del gradiente')
ax.set_title("Visualización del Descenso del Gradiente")
ax.set_xlabel("x")
ax.set_ylabel("f(x)")
ax.legend()
ax.grid(True)

# Mostrar resultados
st.pyplot(fig)
st.subheader("📋 Valores de cada iteración:")
for i, (xv, yv) in enumerate(zip(x_vals, y_vals)):
    st.write(f"Iteración {i}: x = {xv:.4f}, f(x) = {yv:.4f}")
