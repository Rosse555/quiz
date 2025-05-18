import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("📊 Visualización de Superficies Cuádricas y Curvas de Nivel")

# --- Definición de superficies cuádricas ---
superficies = {
    "Paraboloide elíptico": {
        "func": lambda x, y: x**2 + y**2,
        "latex": r"z = x^2 + y^2"
    },
    "Paraboloide hiperbólico": {
        "func": lambda x, y: x**2 - y**2,
        "latex": r"z = x^2 - y^2"
    },
    "Cono elíptico": {
        "func": lambda x, y: np.sqrt(np.abs(x**2 + y**2)),  # evitar complejos
        "latex": r"z = \sqrt{x^2 + y^2}"
    },
    "Hiperboloide de una hoja": {
        "func": lambda x, y: np.sqrt(1 + x**2 + y**2),
        "latex": r"z = \sqrt{1 + x^2 + y^2}"
    },
    "Hiperboloide de dos hojas": {
        "func": lambda x, y: np.sqrt(np.abs(-1 + x**2 + y**2)),
        "latex": r"z = \sqrt{-1 + x^2 + y^2}"
    },
    "Elipsoide": {
        "func": lambda x, y: np.sqrt(np.clip(1 - x**2/4 - y**2/9, 0, None)),
        "latex": r"z = \sqrt{1 - \frac{x^2}{4} - \frac{y^2}{9}}"
    }
}

# --- Interfaz ---
tipo = st.selectbox("🧠 Elige una superficie cuádrica", list(superficies.keys()))
z_func = superficies[tipo]["func"]
latex_eq = superficies[tipo]["latex"]
st.latex(latex_eq)

# --- Crear malla para graficar ---
x_range = np.linspace(-5, 5, 100)
y_range = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x_range, y_range)
Z = z_func(X, Y)

# --- Superficie 3D ---
fig = go.Figure()

# Superficie
fig.add_trace(go.Surface(
    z=Z, x=X, y=Y,
    colorscale="Viridis",
    opacity=0.8,
    name="Superficie"
))

# Curvas de nivel (cortes horizontales)
fig.add_trace(go.Surface(
    z=Z, x=X, y=Y,
    showscale=False,
    colorscale="Greys",
    opacity=0.3,
    contours={"z": {"show": True, "start": np.min(Z), "end": np.max(Z), "size": 0.5, "color":"black"}}
))

# --- Ajustes de gráfico ---
fig.update_layout(
    width=1000,
    height=700,
    title=f"Superficie: {tipo}",
    scene=dict(
        xaxis_title="x",
        yaxis_title="y",
        zaxis_title="z"
    )
)

# --- Mostrar figura ---
st.plotly_chart(fig, use_container_width=False)
