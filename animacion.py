import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("📊 Superficies Cuádricas con Curvas de Nivel: Cortes en Z=0, X=0, Y=0")

# --- Definición de funciones cuádricas ---
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
        "func": lambda x, y: np.sqrt(np.abs(x**2 + y**2)),
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

# --- Selección de superficie y plano de corte ---
tipo = st.selectbox("🧠 Selecciona la superficie cuádrica", list(superficies.keys()))
z_func = superficies[tipo]["func"]
latex_eq = superficies[tipo]["latex"]
st.latex(latex_eq)

plano = st.radio("📏 Selecciona el plano para visualizar curvas de nivel", ["z = 0", "x = 0", "y = 0"])

# --- Malla de puntos ---
x_vals = np.linspace(-5, 5, 100)
y_vals = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x_vals, y_vals)
Z = z_func(X, Y)

fig = go.Figure()

# --- Superficie principal ---
fig.add_trace(go.Surface(
    z=Z, x=X, y=Y,
    colorscale="Viridis",
    opacity=0.8,
    name="Superficie"
))

# --- Agregar curvas de nivel según el plano seleccionado ---
if plano == "z = 0":
    fig.add_trace(go.Surface(
        z=Z, x=X, y=Y,
        showscale=False,
        colorscale="Greys",
        opacity=0.3,
        contours={"z": {"show": True, "start": np.min(Z), "end": np.max(Z), "size": 0.5, "color": "black"}}
    ))

elif plano == "x = 0":
    y_cut = y_vals
    z_cut = z_func(0 * y_cut, y_cut)
    fig.add_trace(go.Scatter3d(
        x=[0] * len(y_cut), y=y_cut, z=z_cut,
        mode='lines',
        name="Corte x = 0",
        line=dict(color='red', width=5)
    ))

elif plano == "y = 0":
    x_cut = x_vals
    z_cut = z_func(x_cut, 0 * x_cut)
    fig.add_trace(go.Scatter3d(
        x=x_cut, y=[0] * len(x_cut), z=z_cut,
        mode='lines',
        name="Corte y = 0",
        line=dict(color='orange', width=5)
    ))

# --- Configuración del gráfico ---
fig.update_layout(
    title=f"Superficie: {tipo} con curva de nivel en {plano}",
    width=1000,
    height=700,
    scene=dict(
        xaxis_title="x",
        yaxis_title="y",
        zaxis_title="z"
    )
)

# --- Mostrar resultado ---
st.plotly_chart(fig, use_container_width=False)
