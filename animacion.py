import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide")
st.title("🧠 Visualización de Superficies Cuádricas con Cortes en Plotly")

# --- Funciones cuádricas ---
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

# --- Interfaz usuario ---
tipo = st.selectbox("📌 Elige una superficie cuádrica", list(superficies.keys()))
plano = st.radio("📏 Plano para visualizar curva de nivel", ["z = 0", "x = 0", "y = 0"])
st.latex(superficies[tipo]["latex"])
f = superficies[tipo]["func"]

# --- Datos de malla ---
x_vals = np.linspace(-5, 5, 100)
y_vals = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x_vals, y_vals)
Z = f(X, Y)

# --- Subgráficas (una 3D, una 2D en Plotly) ---
fig = make_subplots(
    rows=1, cols=2,
    specs=[[{"type": "surface"}, {"type": "xy"}]],
    column_widths=[0.6, 0.4],
    subplot_titles=("Superficie 3D", f"Corte en plano {plano}")
)

# --- Superficie 3D ---
fig.add_trace(
    go.Surface(z=Z, x=X, y=Y, colorscale="Viridis", showscale=True, name="Superficie"),
    row=1, col=1
)

# --- Curva en 3D y gráfico 2D ---
if plano == "x = 0":
    y_cut = y_vals
    z_cut = f(0, y_cut)
    # Agregar línea roja en 3D
    fig.add_trace(go.Scatter3d(x=[0]*len(y_cut), y=y_cut, z=z_cut, mode='lines', line=dict(color='red', width=5), name="x = 0"), row=1, col=1)
    # Agregar curva 2D (z vs y)
    fig.add_trace(go.Scatter(x=y_cut, y=z_cut, mode='lines+markers', line=dict(color='red'), name="z vs y"), row=1, col=2)
    fig.update_xaxes(title="y", row=1, col=2)
    fig.update_yaxes(title="z", row=1, col=2)

elif plano == "y = 0":
    x_cut = x_vals
    z_cut = f(x_cut, 0)
    fig.add_trace(go.Scatter3d(x=x_cut, y=[0]*len(x_cut), z=z_cut, mode='lines', line=dict(color='orange', width=5), name="y = 0"), row=1, col=1)
    fig.add_trace(go.Scatter(x=x_cut, y=z_cut, mode='lines+markers', line=dict(color='orange'), name="z vs x"), row=1, col=2)
    fig.update_xaxes(title="x", row=1, col=2)
    fig.update_yaxes(title="z", row=1, col=2)

elif plano == "z = 0":
    # Agregar curvas de nivel 2D
    contour = go.Contour(x=x_vals, y=y_vals, z=Z, colorscale="Hot", contours=dict(start=np.min(Z), end=np.max(Z), size=1))
    fig.add_trace(contour, row=1, col=2)
    fig.update_xaxes(title="x", row=1, col=2)
    fig.update_yaxes(title="y", row=1, col=2)

# --- Layout final ---
fig.update_layout(
    height=700,
    width=1200,
    title_text=f"Visualización de {tipo} con corte en {plano}",
    scene=dict(xaxis_title="x", yaxis_title="y", zaxis_title="z"),
)

# --- Mostrar en Streamlit ---
st.plotly_chart(fig, use_container_width=False)
