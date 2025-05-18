import streamlit as st
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📊 Superficies Cuádricas y Curvas de Nivel (Cortes en 3D + 2D)")

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

# --- Selección de superficie y plano ---
col1, col2 = st.columns(2)
with col1:
    tipo = st.selectbox("🧠 Superficie cuádrica", list(superficies.keys()))
    plano = st.radio("📏 Plano para curva de nivel", ["z = 0", "x = 0", "y = 0"])
    st.latex(superficies[tipo]["latex"])

z_func = superficies[tipo]["func"]

# --- Malla para la superficie ---
x_vals = np.linspace(-5, 5, 100)
y_vals = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x_vals, y_vals)
Z = z_func(X, Y)

# --- Gráfico 3D ---
fig3d = go.Figure()
fig3d.add_trace(go.Surface(z=Z, x=X, y=Y, colorscale="Viridis", opacity=0.8, name="Superficie"))

# Corte 3D según el plano
if plano == "x = 0":
    y_cut = y_vals
    z_cut = z_func(0, y_cut)
    fig3d.add_trace(go.Scatter3d(
        x=[0]*len(y_cut), y=y_cut, z=z_cut,
        mode='lines', line=dict(color='red', width=5), name="Corte x=0"
    ))
elif plano == "y = 0":
    x_cut = x_vals
    z_cut = z_func(x_cut, 0)
    fig3d.add_trace(go.Scatter3d(
        x=x_cut, y=[0]*len(x_cut), z=z_cut,
        mode='lines', line=dict(color='orange', width=5), name="Corte y=0"
    ))
elif plano == "z = 0":
    fig3d.add_trace(go.Surface(
        z=Z, x=X, y=Y,
        showscale=False,
        colorscale="Greys",
        opacity=0.3,
        contours={"z": {"show": True, "start": np.min(Z), "end": np.max(Z), "size": 0.5}}
    ))

fig3d.update_layout(
    title=f"Superficie: {tipo} con corte en {plano}",
    width=700, height=700,
    scene=dict(
        xaxis_title="x",
        yaxis_title="y",
        zaxis_title="z"
    )
)

# --- Mostrar curva de nivel 2D ---
with col2:
    st.markdown("### 📈 Curva de nivel 2D")
    fig2d, ax = plt.subplots(figsize=(5, 5))

    if plano == "x = 0":
        y_cut = y_vals
        z_cut = z_func(0, y_cut)
        ax.plot(y_cut, z_cut, color='red')
        ax.set_xlabel("y")
        ax.set_ylabel("z")
        ax.set_title("Corte en x = 0")

    elif plano == "y = 0":
        x_cut = x_vals
        z_cut = z_func(x_cut, 0)
        ax.plot(x_cut, z_cut, color='orange')
        ax.set_xlabel("x")
        ax.set_ylabel("z")
        ax.set_title("Corte en y = 0")

    elif plano == "z = 0":
        cp = ax.contour(X, Y, Z, levels=10, colors='black')
        ax.clabel(cp, inline=True, fontsize=8)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("Curvas de nivel z = c")

    st.pyplot(fig2d)

# --- Mostrar gráfico 3D completo ---
st.plotly_chart(fig3d, use_container_width=False)
