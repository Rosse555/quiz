import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="centered")
st.title("📐 Simulación: Suma de Riemann")

# --- Funciones disponibles ---
def f1(x): return x**2
def f2(x): return np.sin(x)
def f3(x): return np.exp(-x**2)
def f4(x): return np.log(x + 1.1)  # evitar log(0)
def f5(x): return np.sqrt(x)

funciones = {
    "x²": f1,
    "sin(x)": f2,
    "e^(-x²)": f3,
    "ln(x + 1.1)": f4,
    "√x": f5
}

# --- Entradas del usuario ---
funcion_sel = st.selectbox("📌 Elige la función", list(funciones.keys()))
f = funciones[funcion_sel]

a = st.number_input("🔹 Límite inferior (a)", value=0.0)
b = st.number_input("🔹 Límite superior (b)", value=5.0)
n = st.slider("🔸 Número de subintervalos (n)", 1, 100, 10)
tipo = st.radio("📏 Tipo de suma de Riemann", ("Izquierda", "Derecha", "Punto medio"))

# --- Construcción de los rectángulos ---
x = np.linspace(a, b, 1000)
y = f(x)

dx = (b - a) / n

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

# --- Visualización ---
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x, y, label=f"f(x) = {funcion_sel}", color='blue')

for xi, hi in zip(x_rect, heights):
    ax.add_patch(plt.Rectangle((xi - (dx if tipo == 'Derecha' else 0 if tipo == 'Izquierda' else dx/2), 0),
                               dx, hi, alpha=0.4, color='orange'))

ax.set_title(f"Suma de Riemann ({tipo.lower()}) con n = {n}")
ax.set_xlabel("x")
ax.set_ylabel("f(x)")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# --- Resultado de la suma ---
st.subheader("📊 Resultado")
st.write(f"Área aproximada bajo la curva en [{a}, {b}] usando suma de Riemann ({tipo.lower()}): **{area_total:.6f}**")
