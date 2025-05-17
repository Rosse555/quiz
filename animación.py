import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, diff, lambdify, sympify

# --- Configuración ---
st.set_page_config(layout="wide")
st.title("🧠 Simulador Interactivo: Método de Newton-Raphson")

# --- Entrada del usuario ---
st.sidebar.header("Parámetros de Entrada")
funcion_str = st.sidebar.text_input("Ingresa la función f(x):", "x**3 - 2*x - 5")
x0 = st.sidebar.number_input("Valor inicial (x₀):", value=2.0)
iteraciones = st.sidebar.slider("Número de iteraciones:", 1, 10, 5)

# --- Cálculo de derivada y funciones ---
x = symbols('x')
f_expr = sympify(funcion_str)
f_prime_expr = diff(f_expr, x)

f = lambdify(x, f_expr, modules=["numpy"])
f_prime = lambdify(x, f_prime_expr, modules=["numpy"])

# --- Iteraciones de Newton-Raphson ---
x_vals = [x0]
for i in range(iteraciones):
    xi = x_vals[-1]
    try:
        xi_new = xi - f(xi) / f_prime(xi)
    except ZeroDivisionError:
        st.error("Derivada cero. Método detenido.")
        break
    x_vals.append(xi_new)

# --- Gráfica interactiva ---
x_range = np.linspace(x0 - 5, x0 + 5, 400)
y_vals = f(x_range)

fig, ax = plt.subplots()
ax.plot(x_range, y_vals, label='f(x)', color='blue')

# Dibujar iteraciones
for i in range(len(x_vals)-1):
    xi = x_vals[i]
    yi = f(xi)
    slope = f_prime(xi)
    x_line = np.linspace(xi-1, xi+1, 10)
    y_line = slope * (x_line - xi) + yi
    ax.plot(x_line, y_line, '--', color='gray')
    ax.plot(xi, yi, 'ro')
    ax.annotate(f"x{i}", (xi, yi))

ax.axhline(0, color='black', linewidth=1)
ax.set_title("Iteraciones del Método de Newton-Raphson")
ax.legend()
st.pyplot(fig)

# --- Mostrar valores resultantes ---
st.subheader("📋 Resultados")
for i, val in enumerate(x_vals):
    st.write(f"x{i} = {val}")
