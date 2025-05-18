import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide")
st.title("🧠 Visualización de Superficies Cuádricas con Cortes Dinámicos")

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

# --- Interfaz de usuario ---
tipo = st.selectbox("📌 Elige una superficie cuádrica", list(superficies.keys()))
plano = st.radio("📏 Plano para visualizar curva de nivel", ["z = 0", "x = 0", "y = 0"])
st.latex(superficies[tipo]["latex"])
f = superficies[tipo]["func"]

# --- Deslizadores según plano seleccionado ---
x_val = st.slider("🔹 Valor de x", -10.0, 10.0, 0.0) if plano == "x = 0" else None
y_val = st.slider("🔹 Valor de y", -10.0, 10.0, 0.0) if plano == "y = 0" else None
z_val = st.slider("🔹 Valor de z", -10.0, 10.0, 0.0) if plano == "z = 0" else None

# --- Malla de puntos ---
x_vals = np.linspace(-5, 5, 100)
y_vals = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x_vals, y_vals)
Z = f(X, Y)

# --- Subgráficas: superficie 3D y curva 2D ---
fig = make_subplots(
    rows=1, cols=2,
    specs=[[{"type": "surface"}, {"type": "xy"}]],
    column_widths=[0.6, 0.4],
    subplot_titles=("Superficie 3D", f"Corte en plano {plano}")
)

# --- Superficie 3D principal ---
fig.add_trace(
    go.Surface(z=Z, x=X, y=Y, colorscale="Viridis", showscale=True, name="Superficie"),
    row=1, col=1
)

# --- Visualización del corte según el plano seleccionado ---
if plano == "x = 0" and x_val is not None:
    y_cut = y_vals
    z_cut = f(x_val, y_cut)
    fig.add_trace(go.Scatter3d(
        x=[x_val]*len(y_cut), y=y_cut, z=z_cut,
        mode='lines', line=dict(color='red', width=5), name=f"x = {x_val}"
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=y_cut, y=z_cut,
        mode='lines+markers', line=dict(color='red'), name="z vs y"
    ), row=1, col=2)
    fig.update_xaxes(title="y", row=1, col=2)
    fig.update_yaxes(title="z", row=1, col=2)

elif plano == "y = 0" and y_val is not None:
    x_cut = x_vals
    z_cut = f(x_cut, y_val)
    fig.add_trace(go.Scatter3d(
        x=x_cut, y=[y_val]*len(x_cut), z=z_cut,
        mode='lines', line=dict(color='orange', width=5), name=f"y = {y_val}"
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=x_cut, y=z_cut,
        mode='lines+markers', line=dict(color='orange'), name="z vs x"
    ), row=1, col=2)
    fig.update_xaxes(title="x", row=1, col=2)
    fig.update_yaxes(title="z", row=1, col=2)

elif plano == "z = 0" and z_val is not None:
    fig.add_trace(go.Surface(
        z=Z, x=X, y=Y,
        showscale=False,
        colorscale="Greys",
        opacity=0.3,
        contours={"z": {"show": True, "start": z_val, "end": z_val, "size": 0.5}}
    ), row=1, col=1)
    fig.add_trace(go.Contour(
        x=x_vals, y=y_vals, z=Z,
        contours=dict(start=z_val, end=z_val, size=0.5, coloring="lines"),
        line=dict(color="black", width=2),
        showscale=False
    ), row=1, col=2)
    fig.update_xaxes(title="x", row=1, col=2)
    fig.update_yaxes(title="y", row=1, col=2)

# --- Layout final ---
fig.update_layout(
    height=700,
    width=1200,
    title_text=f"Visualización de {tipo} con corte en {plano}",
    scene=dict(xaxis_title="x", yaxis_title="y", zaxis_title="z"),
)

# --- Mostrar gráfico en Streamlit ---
st.plotly_chart(fig, use_container_width=False)
