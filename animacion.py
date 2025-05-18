import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="centered")
st.title("📐 Simulación: Suma de Riemann")

# --- Definir funciones y fórmulas en LaTeX ---
funciones = {
    "x²": {
        "func": lambda x: x**2,
        "latex": r"f(x) = x^2"
    },
    "sin(x)": {
        "func": lambda x: np.sin(x),
        "latex": r"f(x) = \sin(x)"
    },
    "e^(-x²)": {
        "func": lambda x: np.exp(-x**2),
        "latex": r"f(x) = e^{-x^2}"
    },
    "ln(x + 1.1)": {
        "func": lambda x: np.log(x + 1.1),  # evitar log(0)
        "latex": r"f(x) = \ln(x + 1.1)"
    },
    "√x": {
        "func": lambda x: np.sqrt(x),
        "latex": r"f(x) = \sqrt{x}"
    }
}

# --- Menú de selección ---
nombre_funcion = st.selectbox("📌 Elige la función", list(funciones.keys()))
f = funciones[nombre_funcion]["func"]
latex = funciones[nombre_funcion]["latex"]

# --- Mostrar función seleccionada en LaTeX ---
st.latex(latex)

# --- Parámetros de la suma de Riemann ---
a = st.number_input("🔹 Límite inferior (a)", value=0.0)
b = st.number_input("🔹 Límite superior (b)", value=5.0)
n = st.slider("🔸 Número de subintervalos (n)", 1, 100, 10)
tipo = st.radio("📏 Tipo de suma de Riemann", ("Izquierda", "Derecha", "Punto medio"))

# --- Cálculo de la suma de Riemann ---
dx = (b - a) / n
x = np.linspace(a, b, 1000)
y = f(x)

if tipo == "Izquierda":
    x_rect = np.linspace(a, b - dx, n)
    heights = f(x_rect)
elif tipo == "Derecha":
    x_rect = np.linspace(a + dx, b, n)
    heights = f(x_rect)
else:  # Punto medio
    x_rect = np.linspace(a + dx/2, b - dx/2, n)
    heights = f(x_rect)

areas = heights * dx
area_total = np.sum(areas)

# --- Gráfica ---
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x, y, label=latex, color='blue')

for xi, hi in zip(x_rect, heights):
    x_base = xi - (0 if tipo == 'Izquierda' else dx if tipo == 'Derecha' else dx/2)
    ax.add_patch(plt.Rectangle((x_base, 0), dx, hi, alpha=0.4, color='orange'))

ax.set_title(f"Suma de Riemann ({tipo.lower()}) con n = {n}")
ax.set_xlabel("x")
ax.set_ylabel("f(x)")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# --- Resultado ---
st.subheader("📊 Resultado")
st.latex(r"\text{Área aproximada} = " + f"{area_total:.6f}")
