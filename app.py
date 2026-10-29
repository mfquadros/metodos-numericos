import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import math
import sympy as sp

from sanitizador import sanitiza_expressao, processa_expressao_natural
from bissecao import bissecao
from falsa_posicao import falsa_posicao
from newton import newton
from secantes import secantes
from eliminacao_gauss import eliminacao_gauss, eliminacao_gauss_detalhada
from fatoracao_lu import fatoracao_lu, fatoracao_lu_detalhada
from gauss_jacobi import gauss_jacobi, gauss_jacobi_detalhado, criterio_linhas
from gauss_seidel import gauss_seidel, gauss_seidel_detalhado, criterio_sassenfeld
from ajuste_polinomial import ajuste_polinomial, ajuste_polinomial_detalhado
from interpolacao_definicao import interpolacao_definicao, interpolacao_definicao_detalhada
from interpolacao_lagrange import interpolacao_lagrange, interpolacao_lagrange_detalhada
from interpolacao_newton import interpolacao_newton, interpolacao_newton_detalhada
from regra_trapezios import regra_trapezios_repetida, regra_trapezios_detalhada
from regra_simpson import regra_simpson_13, regra_simpson_detalhada

st.set_page_config(
    page_title="Métodos Numéricos",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"], .stApp {
        background-color: #111827 !important;
        color: #E5E7EB !important;
        font-family: 'Inter', system-ui, sans-serif !important;
    }

    [data-testid="stAppViewContainer"] { background-color: #111827 !important; }
    [data-testid="stHeader"] { background-color: transparent !important; }

    [data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid #1F2937 !important;
    }
    [data-testid="stSidebar"] * { color: #D1D5DB !important; }
    [data-testid="stSidebar"] label { font-size: 0.82rem !important; color: #9CA3AF !important; }

    h1, h2, h3 { font-weight: 600 !important; letter-spacing: -0.02em !important; }

    div[data-testid="stMetric"] {
        background-color: #1F2937;
        border: 1px solid #374151;
        border-radius: 6px;
        padding: 14px 16px;
    }
    div[data-testid="stMetric"] label {
        font-size: 0.72rem !important;
        font-weight: 500 !important;
        color: #9CA3AF !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-size: 1.4rem !important;
        font-weight: 600 !important;
        color: #F9FAFB !important;
        font-family: 'JetBrains Mono', monospace !important;
    }

    .nota-rodape {
        font-size: 0.78rem;
        color: #6B7280;
        margin: 6px 0 18px 0;
    }

    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        background-color: #1F2937 !important;
        color: #F9FAFB !important;
        border: 1px solid #374151 !important;
        border-radius: 5px !important;
        font-size: 0.88rem !important;
    }
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #3B82F6 !important;
        box-shadow: none !important;
        outline: none !important;
    }

    .stButton > button {
        background-color: #1D4ED8 !important;
        color: #fff !important;
        border: none !important;
        border-radius: 5px !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        padding: 8px 18px !important;
        box-shadow: none !important;
        letter-spacing: 0.01em;
    }
    .stButton > button:hover {
        background-color: #2563EB !important;
    }

    .stTabs [data-baseweb="tab-highlight-title"] {
        display: none !important;
    }
    .stTabs [data-baseweb="tab-border"] {
        background-color: transparent !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent !important;
        border-bottom: 1px solid #1F2937 !important;
        gap: 0 !important;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        color: #6B7280 !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        border: none !important;
        padding: 8px 18px !important;
    }
    .stTabs [aria-selected="true"] {
        color: #E5E7EB !important;
        border-bottom: 2px solid #3B82F6 !important;
    }

    [data-testid="stDataFrame"] {
        background: #1F2937 !important;
        border: 1px solid #374151 !important;
        border-radius: 5px !important;
    }

    .streamlit-expanderHeader {
        background: #1F2937 !important;
        color: #D1D5DB !important;
        border-radius: 5px !important;
        border: 1px solid #374151 !important;
        font-size: 0.84rem !important;
    }
    .streamlit-expanderContent {
        background: #1F2937 !important;
        border: 1px solid #374151 !important;
        border-top: none !important;
        border-radius: 0 0 5px 5px !important;
    }

    .stAlert { border-radius: 5px !important; }

    hr { border-color: #1F2937 !important; }

    .bloco-equacao {
        background: #1F2937;
        border-left: 3px solid #3B82F6;
        border-radius: 0 5px 5px 0;
        padding: 10px 16px;
        margin: 10px 0 16px 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
        color: #E5E7EB;
    }

    .sintaxe-item {
        font-size: 0.8rem;
        color: #9CA3AF;
        margin: 2px 0;
        line-height: 1.7;
    }
    .sintaxe-item code {
        background: #374151;
        padding: 1px 5px;
        border-radius: 3px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        color: #93C5FD;
    }
</style>
""", unsafe_allow_html=True)


def avalia_funcao(expr, x_val):
    ns = {
        "x": float(x_val), "math": math,
        "sin": math.sin, "cos": math.cos, "tan": math.tan,
        "asin": math.asin, "acos": math.acos, "atan": math.atan,
        "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh,
        "exp": math.exp, "log": math.log, "log10": math.log10,
        "sqrt": math.sqrt, "pi": math.pi, "e": math.e, "abs": abs
    }
    return float(eval(expr, {"__builtins__": {}}, ns))


def fmt_sci(val, prec=6):
    if val is None:
        return "—"
    try:
        val = float(val)
    except Exception:
        return str(val)
    if val == 0:
        return f"0.{'0'*prec}"
    av = abs(val)
    if av < 1e-4 or av >= 1e6:
        exp = int(math.floor(math.log10(av)))
        m = val / (10 ** exp)
        sup = str(exp).translate(str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹"))
        return f"{m:.3f} × 10{sup}"
    return f"{val:.{prec}f}"


def lim_str(val):
    try:
        f = float(val)
        return f"{int(round(f))}" if abs(f - round(f)) < 1e-7 else f"{f:.4g}"
    except Exception:
        return str(val)


def fig_base(titulo="", xlabel="x", ylabel="f(x)"):
    fig = go.Figure()
    fig.update_layout(
        title=dict(text=titulo, font=dict(size=13, color="#9CA3AF", family="Inter, sans-serif"), x=0, xref="paper"),
        xaxis=dict(
            title=dict(text=xlabel, font=dict(size=12, color="#9CA3AF")),
            gridcolor="rgba(255,255,255,0.04)",
            zerolinecolor="rgba(255,255,255,0.15)",
            zerolinewidth=1,
            linecolor="#374151", showline=True,
            tickfont=dict(color="#9CA3AF", size=11)
        ),
        yaxis=dict(
            title=dict(text=ylabel, font=dict(size=12, color="#9CA3AF")),
            gridcolor="rgba(255,255,255,0.04)",
            zerolinecolor="rgba(255,255,255,0.15)",
            zerolinewidth=1,
            linecolor="#374151", showline=True,
            tickfont=dict(color="#9CA3AF", size=11)
        ),
        plot_bgcolor="#1F2937",
        paper_bgcolor="#111827",
        hoverlabel=dict(bgcolor="#111827", font_size=11, font_color="#E5E7EB", font_family="JetBrains Mono, monospace"),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
            bgcolor="rgba(17,24,39,0.6)", bordercolor="#374151", borderwidth=1,
            font=dict(size=10, color="#9CA3AF")
        ),
        margin=dict(l=48, r=20, t=44, b=44),
        height=420
    )
    return fig


def card(col, label, valor, nota=""):
    col.metric(label=label, value=valor)
    if nota:
        col.markdown(f"<div class='nota-rodape'>{nota}</div>", unsafe_allow_html=True)


def sintaxe_sidebar():
    with st.sidebar.expander("Sintaxe aceita", expanded=False):
        st.markdown("""
        <div class="sintaxe-item">Potências: <code>x^3</code>, <code>xˆ3</code>, <code>x**3</code></div>
        <div class="sintaxe-item">Multiplicação implícita: <code>9x</code>, <code>2(x+1)</code></div>
        <div class="sintaxe-item">Exponencial: <code>e^x</code>, <code>e^-x</code>, <code>exp(x)</code></div>
        <div class="sintaxe-item">Trig.: <code>sen(x)</code>, <code>cos(x)</code>, <code>tg(x)</code></div>
        <div class="sintaxe-item">Log/Raiz: <code>ln(x)</code>, <code>log(x)</code>, <code>raiz(x)</code></div>
        <div class="sintaxe-item">Decimais: <code>2.5x</code> ou <code>2,5x</code></div>
        """, unsafe_allow_html=True)


categoria = st.sidebar.selectbox(
    "Módulo",
    [
        "Zeros de Funções",
        "Sistemas Lineares",
        "Ajuste de Curvas",
        "Interpolação Polinomial",
        "Integração Numérica"
    ]
)
st.sidebar.markdown("---")


if categoria == "Zeros de Funções":
    st.header("Zeros de Funções")

    metodo = st.sidebar.selectbox("Método", ["Bisseção", "Falsa Posição", "Newton-Raphson", "Secantes"])

    exemplo = st.sidebar.selectbox(
        "Exemplo",
        ["xˆ3 − 9xˆ2 + 3", "x^3 − 9x + 3", "cos(x) − x", "e^-x − x", "x^2 − 2", "Personalizado"]
    )

    exemplos_map = {
        "xˆ3 − 9xˆ2 + 3": ("xˆ3-9xˆ2+3", 0.0, 1.0, 0.5, 0.0, 1.0),
        "x^3 − 9x + 3":    ("x^3-9x+3",   0.0, 3.0, 2.0, 0.0, 3.0),
        "cos(x) − x":      ("cos(x)-x",    0.0, 1.5, 0.5, 0.0, 1.0),
        "e^-x − x":        ("e^-x-x",      0.0, 1.5, 0.5, 0.0, 1.0),
        "x^2 − 2":         ("x^2-2",       1.0, 2.0, 1.5, 1.0, 2.0),
    }
    def_expr, def_a, def_b, def_chute, def_x0, def_x1 = exemplos_map.get(exemplo, ("xˆ3-9xˆ2+3", 0.0, 1.0, 0.5, 0.0, 1.0))

    expr_raw = st.sidebar.text_input("f(x)", value=def_expr)
    expr_py, expr_latex, err_parse = processa_expressao_natural(expr_raw)

    sintaxe_sidebar()

    tol = st.sidebar.number_input("Tolerância ε", value=1e-4, format="%.2e", min_value=1e-12)
    max_iter = st.sidebar.number_input("Máx. iterações", value=50, min_value=5, max_value=500, step=5)

    for k, v in [
        ("zeros_hist", []), ("zeros_raiz", None), ("zeros_metodo", metodo),
        ("zeros_expr_py", expr_py), ("zeros_expr_raw", expr_raw),
        ("zeros_expr_latex", expr_latex), ("zeros_err_msg", None)
    ]:
        if k not in st.session_state:
            st.session_state[k] = v

    if metodo in ["Bisseção", "Falsa Posição"]:
        ca, cb = st.sidebar.columns(2)
        a = ca.number_input("a", value=def_a)
        b = cb.number_input("b", value=def_b)
        if st.sidebar.button("Calcular", type="primary", use_container_width=True):
            st.session_state.zeros_metodo = metodo
            st.session_state.zeros_expr_py = expr_py
            st.session_state.zeros_expr_raw = expr_raw
            st.session_state.zeros_expr_latex = expr_latex
            st.session_state.zeros_err_msg = None
            if err_parse or not expr_py:
                st.session_state.zeros_err_msg = f"Expressão inválida: {err_parse}"
                st.session_state.zeros_raiz = None
                st.session_state.zeros_hist = []
            else:
                try:
                    fa, fb = avalia_funcao(expr_py, a), avalia_funcao(expr_py, b)
                    if fa * fb > 0:
                        st.session_state.zeros_err_msg = f"Bolzano não satisfeito: f({a}) = {fa:.4f} e f({b}) = {fb:.4f} têm o mesmo sinal."
                        st.session_state.zeros_raiz = None
                        st.session_state.zeros_hist = []
                    else:
                        fn = bissecao if metodo == "Bisseção" else falsa_posicao
                        r, hist = fn(expr_py, a, b, tol, max_iter=max_iter)
                        st.session_state.zeros_raiz = r
                        st.session_state.zeros_hist = hist
                except Exception as e:
                    st.session_state.zeros_err_msg = str(e)
                    st.session_state.zeros_raiz = None
                    st.session_state.zeros_hist = []

    elif metodo == "Newton-Raphson":
        chute = st.sidebar.number_input("Chute inicial x₀", value=def_chute)
        if st.sidebar.button("Calcular", type="primary", use_container_width=True):
            st.session_state.zeros_metodo = metodo
            st.session_state.zeros_expr_py = expr_py
            st.session_state.zeros_expr_raw = expr_raw
            st.session_state.zeros_expr_latex = expr_latex
            st.session_state.zeros_err_msg = None
            if err_parse or not expr_py:
                st.session_state.zeros_err_msg = f"Expressão inválida: {err_parse}"
                st.session_state.zeros_raiz = None
                st.session_state.zeros_hist = []
            else:
                try:
                    r, hist = newton(expr_py, chute, tol, max_iter=max_iter)
                    st.session_state.zeros_raiz = r
                    st.session_state.zeros_hist = hist
                except Exception as e:
                    st.session_state.zeros_err_msg = str(e)
                    st.session_state.zeros_raiz = None
                    st.session_state.zeros_hist = []

    elif metodo == "Secantes":
        cx0, cx1 = st.sidebar.columns(2)
        x0 = cx0.number_input("x₀", value=def_x0)
        x1 = cx1.number_input("x₁", value=def_x1)
        if st.sidebar.button("Calcular", type="primary", use_container_width=True):
            st.session_state.zeros_metodo = metodo
            st.session_state.zeros_expr_py = expr_py
            st.session_state.zeros_expr_raw = expr_raw
            st.session_state.zeros_expr_latex = expr_latex
            st.session_state.zeros_err_msg = None
            if err_parse or not expr_py:
                st.session_state.zeros_err_msg = f"Expressão inválida: {err_parse}"
                st.session_state.zeros_raiz = None
                st.session_state.zeros_hist = []
            else:
                try:
                    r, hist = secantes(expr_py, x0, x1, tol, max_iter=max_iter)
                    st.session_state.zeros_raiz = r
                    st.session_state.zeros_hist = hist
                except Exception as e:
                    st.session_state.zeros_err_msg = str(e)
                    st.session_state.zeros_raiz = None
                    st.session_state.zeros_hist = []

    if st.session_state.zeros_err_msg:
        st.error(st.session_state.zeros_err_msg)

    historico = st.session_state.zeros_hist
    raiz = st.session_state.zeros_raiz
    expr_p = st.session_state.zeros_expr_py
    expr_l = st.session_state.zeros_expr_latex
    met_calc = st.session_state.zeros_metodo

    if historico:
        str_raiz = f"{raiz:.6f}" if raiz is not None else "não convergiu"
        y_final = avalia_funcao(expr_p, raiz) if raiz is not None else 0.0

        c1, c2, c3 = st.columns(3)
        card(c1, "Raiz aproximada", str_raiz)
        card(c2, "Iterações", str(len(historico)))
        card(c3, "|f(x*)|", fmt_sci(y_final))

        st.latex(f"f(x) = {expr_l}")

        tab_g, tab_t = st.tabs(["Gráfico de Convergência", "Tabela de Iterações"])

        with tab_g:
            total = len(historico)
            c_sl, c_txt = st.columns([4, 1])
            passo = c_sl.slider("Iteração", 1, total, total, label_visibility="collapsed")
            c_txt.markdown(f"<div style='padding-top:4px;font-size:0.85rem;color:#9CA3AF;'>Iteração {passo} de {total}</div>", unsafe_allow_html=True)

            xs = [h['x'] for h in historico if h.get('x') is not None]
            mn, mx = min(xs), max(xs)
            span = max(abs(mx - mn), 1.0)
            xp0, xp1 = mn - 0.5 * span, mx + 0.5 * span
            xv = np.linspace(xp0, xp1, 600)
            yv = []
            for xvv in xv:
                try:
                    yv.append(avalia_funcao(expr_p, xvv))
                except Exception:
                    yv.append(np.nan)

            fig = fig_base(f"Convergência do Método ({met_calc}) — Iteração {passo} de {total}", xlabel="x", ylabel="f(x)")
            fig.add_trace(go.Scatter(x=xv, y=yv, mode='lines', name='f(x)',
                                     line=dict(color='#60A5FA', width=2)))

            tx = [historico[i]['x'] for i in range(passo) if historico[i].get('x') is not None]
            ty = [historico[i]['y'] for i in range(passo) if historico[i].get('y') is not None]
            fig.add_trace(go.Scatter(x=tx, y=ty, mode='markers+lines', name='Trajetória',
                                     marker=dict(size=6, color='#F87171'),
                                     line=dict(color='#F87171', dash='dot', width=1)))

            pa = historico[passo - 1]
            fig.add_trace(go.Scatter(x=[pa['x']], y=[pa['y']], mode='markers',
                                     name=f'Ponto atual',
                                     marker=dict(size=10, color='#34D399', symbol='diamond')))

            if met_calc in ["Bisseção", "Falsa Posição"] and 'a' in pa and 'b' in pa:
                fig.add_vline(x=pa['a'], line_dash="dash", line_color="#FBBF24",
                              annotation_text=f"a={pa['a']:.3f}", annotation_font_color="#FBBF24")
                fig.add_vline(x=pa['b'], line_dash="dash", line_color="#FBBF24",
                              annotation_text=f"b={pa['b']:.3f}", annotation_font_color="#FBBF24")
                if met_calc == "Falsa Posição":
                    fa_v = avalia_funcao(expr_p, pa['a'])
                    fb_v = avalia_funcao(expr_p, pa['b'])
                    fig.add_trace(go.Scatter(x=[pa['a'], pa['b']], y=[fa_v, fb_v],
                                             mode='lines+markers', name='Corda',
                                             line=dict(color='#A78BFA', width=1.5),
                                             marker=dict(size=5, color='#A78BFA')))

            elif met_calc == "Newton-Raphson" and pa.get('df') and abs(pa['df']) > 1e-12:
                xc, yc, df = pa['x'], pa['y'], pa['df']
                xp = pa.get('x_prox', xc - yc / df)
                if xp is not None:
                    fig.add_trace(go.Scatter(x=[xc, xp], y=[yc, 0], mode='lines+markers',
                                             name='Tangente', line=dict(color='#A78BFA', width=1.5),
                                             marker=dict(size=5, color='#A78BFA')))

            elif met_calc == "Secantes" and 'x0' in pa and 'x1' in pa:
                fig.add_trace(go.Scatter(x=[pa['x0'], pa['x1']], y=[pa['fx0'], pa['fx1']],
                                         mode='lines+markers', name='Secante',
                                         line=dict(color='#A78BFA', width=1.5),
                                         marker=dict(size=5, color='#A78BFA')))

            st.plotly_chart(fig, use_container_width=True)

        with tab_t:
            st.dataframe(pd.DataFrame(historico[:passo]), use_container_width=True)


elif categoria == "Sistemas Lineares":
    st.header("Sistemas Lineares")

    metodo = st.sidebar.selectbox(
        "Método",
        ["Eliminação de Gauss", "Fatoração LU", "Gauss-Jacobi", "Gauss-Seidel"]
    )
    n = st.sidebar.selectbox("Dimensão n×n", [2, 3, 4], index=1)

    preset = st.sidebar.selectbox("Exemplo", ["Diagonal dominante", "Simétrico positivo definido", "Personalizado"])

    presets = {
        "Diagonal dominante": {
            2: ([[5., 1.], [2., 6.]], [7., 16.]),
            3: ([[10., 2., 1.], [1., 5., 1.], [2., 3., 10.]], [7., -8., 6.]),
            4: ([[10.,-1., 2., 0.],[-1.,11.,-1., 3.],[2.,-1.,10.,-1.],[0., 3.,-1., 8.]], [6.,25.,-11.,15.]),
        },
        "Simétrico positivo definido": {
            2: ([[4., 1.], [1., 3.]], [1., 2.]),
            3: ([[4.,-1., 0.],[-1., 4.,-1.],[0.,-1., 4.]], [1., 2., 3.]),
            4: ([[4., 1., 0., 0.],[1., 4., 1., 0.],[0., 1., 4., 1.],[0., 0., 1., 4.]], [1., 2., 3., 4.]),
        },
    }
    if preset in presets:
        dA, db = presets[preset][n]
    else:
        dA = [[1. if i == j else 0. for j in range(n)] for i in range(n)]
        db = [1.] * n

    st.markdown(f"**Sistema $Ax = b$ — {n}×{n}**")

    hdrs = st.columns(n + 1)
    for j in range(n):
        hdrs[j].markdown(f"<div style='text-align:center;font-size:0.8rem;color:#6B7280'>x{j+1}</div>", unsafe_allow_html=True)
    hdrs[n].markdown("<div style='text-align:center;font-size:0.8rem;color:#6B7280'>b</div>", unsafe_allow_html=True)

    A_in = [[0.] * n for _ in range(n)]
    b_in = [0.] * n
    for i in range(n):
        row = st.columns(n + 1)
        for j in range(n):
            A_in[i][j] = row[j].number_input(f"A{i+1}{j+1}", value=float(dA[i][j]),
                                              key=f"A_{n}_{preset}_{i}_{j}", label_visibility="collapsed")
        b_in[i] = row[n].number_input(f"b{i+1}", value=float(db[i]),
                                       key=f"b_{n}_{preset}_{i}", label_visibility="collapsed")

    if "Jacobi" in metodo or "Seidel" in metodo:
        st.markdown("---")
        ct, cm, cx = st.columns(3)
        tol_it = ct.number_input("Tolerância ε", value=1e-4, format="%.2e")
        max_it = cm.number_input("Máx. iterações", value=50, min_value=5, max_value=500)
        x0_v = cx.number_input("Valor inicial x⁽⁰⁾", value=0.0)
        x0 = [x0_v] * n

    if st.button("Resolver", type="primary", use_container_width=True):
        if metodo == "Eliminação de Gauss":
            sol, etapas = eliminacao_gauss_detalhada(A_in, b_in)
            if sol:
                cols = st.columns(n)
                for i, v in enumerate(sol):
                    card(cols[i], f"x{i+1}", f"{v:.6f}")
                st.markdown("**Escalonamento:**")
                for et in etapas:
                    st.caption(f"Passo {et['passo']} — {et['descricao']}")
                    df_e = pd.DataFrame(et['matriz'], columns=[f"x{j+1}" for j in range(n)] + ["b"])
                    st.dataframe(df_e.style.format("{:.4f}"), use_container_width=True)
            else:
                st.error("Sistema singular ou pivô nulo.")

        elif metodo == "Fatoração LU":
            sol, L, U, y = fatoracao_lu_detalhada(A_in, b_in)
            if sol:
                cL, cU = st.columns(2)
                with cL:
                    st.caption("Matriz L")
                    st.dataframe(pd.DataFrame(L, columns=[f"c{j+1}" for j in range(n)]).style.format("{:.4f}"), use_container_width=True)
                with cU:
                    st.caption("Matriz U")
                    st.dataframe(pd.DataFrame(U, columns=[f"c{j+1}" for j in range(n)]).style.format("{:.4f}"), use_container_width=True)
                y_s = ", ".join([f"{v:.4f}" for v in y])
                x_s = ", ".join([f"{v:.4f}" for v in sol])
                st.latex(rf"Ly = b \implies y = \begin{{bmatrix}} {y_s} \end{{bmatrix}}^T")
                st.latex(rf"Ux = y \implies x = \begin{{bmatrix}} {x_s} \end{{bmatrix}}^T")
                cols = st.columns(n)
                for i, v in enumerate(sol):
                    card(cols[i], f"x{i+1}", f"{v:.6f}")
            else:
                st.error("Fatoração falhou: pivô nulo.")

        elif metodo == "Gauss-Jacobi":
            ok_l, max_a, _ = criterio_linhas(A_in)
            st.caption(f"Critério das linhas: α_max = {max_a:.4f} {'< 1 (convergência garantida)' if ok_l else '≥ 1'}")
            sol, hist, _ = gauss_jacobi_detalhado(A_in, b_in, x0, tol_it, max_it)
            if sol:
                cols = st.columns(n + 1)
                for i, v in enumerate(sol):
                    card(cols[i], f"x{i+1}", f"{v:.6f}")
                card(cols[n], "Iterações", str(len(hist) - 1))

                tab_t, tab_g = st.tabs(["Tabela", "Convergência do erro"])
                rows = []
                for h in hist:
                    r = {"k": h['iter']}
                    for i, v in enumerate(h['x']): r[f"x{i+1}"] = v
                    r["erro"] = h['erro'] if h['erro'] is not None else 0.
                    rows.append(r)
                with tab_t:
                    st.dataframe(pd.DataFrame(rows).style.format(precision=6), use_container_width=True)
                with tab_g:
                    erros = [h['erro'] for h in hist if h['erro'] is not None]
                    if erros:
                        fig = fig_base("Erro por iteração", "Iteração", "Erro")
                        fig.add_trace(go.Scatter(x=list(range(1, len(erros)+1)), y=erros,
                                                 mode='lines+markers', name='erro',
                                                 line=dict(color='#60A5FA', width=2),
                                                 marker=dict(size=5)))
                        fig.update_layout(yaxis_type="log")
                        st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("Diagonal principal contém zero.")

        elif metodo == "Gauss-Seidel":
            ok_s, max_b, _ = criterio_sassenfeld(A_in)
            ok_l, max_a, _ = criterio_linhas(A_in)
            st.caption(f"Sassenfeld: β_max = {max_b:.4f} {'< 1 (convergência garantida)' if ok_s else '≥ 1'}")
            sol, hist, _ = gauss_seidel_detalhado(A_in, b_in, x0, tol_it, max_it)
            if sol:
                cols = st.columns(n + 1)
                for i, v in enumerate(sol):
                    card(cols[i], f"x{i+1}", f"{v:.6f}")
                card(cols[n], "Iterações", str(len(hist) - 1))

                tab_t, tab_g = st.tabs(["Tabela", "Convergência do erro"])
                rows = []
                for h in hist:
                    r = {"k": h['iter']}
                    for i, v in enumerate(h['x']): r[f"x{i+1}"] = v
                    r["erro"] = h['erro'] if h['erro'] is not None else 0.
                    rows.append(r)
                with tab_t:
                    st.dataframe(pd.DataFrame(rows).style.format(precision=6), use_container_width=True)
                with tab_g:
                    erros = [h['erro'] for h in hist if h['erro'] is not None]
                    if erros:
                        fig = fig_base("Erro por iteração", "Iteração", "Erro")
                        fig.add_trace(go.Scatter(x=list(range(1, len(erros)+1)), y=erros,
                                                 mode='lines+markers', name='erro',
                                                 line=dict(color='#34D399', width=2),
                                                 marker=dict(size=5)))
                        fig.update_layout(yaxis_type="log")
                        st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("Diagonal principal contém zero.")


elif categoria == "Ajuste de Curvas":
    st.header("Ajuste de Curvas — Mínimos Quadrados")

    preset_aj = st.selectbox(
        "Conjunto de dados",
        ["Linear com ruído", "Parábola", "Cúbica", "Personalizado"]
    )
    presets_aj = {
        "Linear com ruído": ("1, 2, 3, 4, 5, 6", "1.2, 1.9, 3.2, 4.1, 5.3, 7.1", 1),
        "Parábola":         ("0, 1, 2, 3, 4, 5", "2.1, 5.0, 10.2, 17.1, 26.0, 37.3", 2),
        "Cúbica":           ("-2,-1, 0, 1, 2, 3", "-7.8,-0.9, 1.1, 3.2, 9.8, 28.1", 3),
    }
    def_x, def_y, def_g = presets_aj.get(preset_aj, ("1,2,3,4,5", "0.5,2.5,2.0,4.0,3.5", 2))

    col1, col2 = st.columns(2)
    str_x = col1.text_input("Coordenadas X (vírgula)", def_x)
    str_y = col2.text_input("Coordenadas Y (vírgula)", def_y)
    cg, cp = st.columns(2)
    grau = cg.number_input("Grau do polinômio", min_value=1, max_value=6, value=def_g)
    x_ev = cp.number_input("Avaliar em x*", value=2.5)

    if st.button("Ajustar", type="primary", use_container_width=True):
        try:
            px = [float(v.strip()) for v in str_x.split(",") if v.strip()]
            py = [float(v.strip()) for v in str_y.split(",") if v.strip()]
            if len(px) != len(py):
                st.error("X e Y devem ter o mesmo número de elementos.")
            elif len(px) <= grau:
                st.error(f"Pontos ({len(px)}) insuficientes para grau {grau}.")
            else:
                coefs, matA, vecB, r2, sqe, sqt, res_tab = ajuste_polinomial_detalhado(px, py, grau)
                partes = []
                for idx, c in enumerate(coefs):
                    pw = grau - idx
                    s = (" + " if c >= 0 and idx > 0 else (" - " if c < 0 and idx > 0 else ("-" if c < 0 else "")))
                    v = abs(c)
                    if pw > 1: partes.append(f"{s}{v:.4f}x^{{{pw}}}")
                    elif pw == 1: partes.append(f"{s}{v:.4f}x")
                    else: partes.append(f"{s}{v:.4f}")
                st.latex(f"P_{{{grau}}}(x) = {''.join(partes)}")

                poly = np.poly1d(coefs)
                y_pred = poly(x_ev)
                c1, c2, c3 = st.columns(3)
                card(c1, "R²", f"{r2:.6f}", nota="coeficiente de determinação")
                card(c2, "SQE", fmt_sci(sqe), nota="soma quadrática dos resíduos")
                card(c3, f"P({x_ev})", f"{y_pred:.6f}")

                mn, mx = min(px), max(px)
                sp_ = mx - mn
                xc = np.linspace(mn - 0.15*sp_, mx + 0.15*sp_, 300)
                yc = poly(xc)

                fig = fig_base(f"Ajuste polinomial grau {grau}", "x", "y")
                fig.add_trace(go.Scatter(x=xc, y=yc, mode='lines', name=f'P_{grau}(x)',
                                         line=dict(color='#60A5FA', width=2)))
                for xi, yi in zip(px, py):
                    fig.add_trace(go.Scatter(x=[xi, xi], y=[yi, poly(xi)], mode='lines',
                                             line=dict(color='#4B5563', dash='dash', width=1),
                                             showlegend=False))
                fig.add_trace(go.Scatter(x=px, y=py, mode='markers', name='Dados',
                                         marker=dict(size=8, color='#F87171')))
                fig.add_trace(go.Scatter(x=[x_ev], y=[y_pred], mode='markers',
                                         name=f'P({x_ev})',
                                         marker=dict(size=10, color='#34D399', symbol='diamond')))
                st.plotly_chart(fig, use_container_width=True)

                tab_s, tab_r = st.tabs(["Equações normais", "Resíduos"])
                with tab_s:
                    df_m = pd.DataFrame(matA, columns=[f"a{k}" for k in range(grau+1)])
                    df_m["b"] = vecB
                    st.dataframe(df_m.style.format("{:.4f}"), use_container_width=True)
                with tab_r:
                    st.dataframe(pd.DataFrame(res_tab).style.format("{:.4f}"), use_container_width=True)

        except Exception as e:
            st.error(str(e))


elif categoria == "Interpolação Polinomial":
    st.header("Interpolação Polinomial")

    metodo = st.sidebar.selectbox(
        "Método",
        ["Definição (Vandermonde)", "Lagrange", "Newton", "Comparar os três"]
    )

    preset_ip = st.selectbox("Conjunto de nós", ["3 pontos", "4 pontos (cúbica)", "Personalizado"])
    presets_ip = {
        "3 pontos":         ("0, 1, 2", "1, 3, 2", 1.5),
        "4 pontos (cúbica)": ("-1, 0, 2, 4", "4, 1, -1, 9", 1.0),
    }
    def_ix, def_iy, def_ie = presets_ip.get(preset_ip, ("0,1,2,3", "1,2,5,10", 1.5))

    cx, cy = st.columns(2)
    str_x = cx.text_input("Nós X", def_ix)
    str_y = cy.text_input("Valores Y", def_iy)
    x_ev = st.number_input("Interpolação em x*", value=float(def_ie))

    if st.button("Interpolar", type="primary", use_container_width=True):
        try:
            px = [float(v.strip()) for v in str_x.split(",") if v.strip()]
            py = [float(v.strip()) for v in str_y.split(",") if v.strip()]
            if len(px) != len(py):
                st.error("X e Y devem ter o mesmo número de elementos.")
            elif len(set(px)) != len(px):
                st.error("Os nós X devem ser distintos.")
            else:
                np_ = len(px)
                grau = np_ - 1
                res = None

                if metodo == "Definição (Vandermonde)":
                    res, coefs, V = interpolacao_definicao_detalhada(px, py, x_ev)
                    c1, c2 = st.columns(2)
                    card(c1, f"P({x_ev})", f"{res:.6f}")
                    card(c2, "Grau", str(grau))
                    partes = []
                    for j, c in enumerate(coefs):
                        s = (" + " if c >= 0 and j > 0 else (" - " if c < 0 and j > 0 else ("-" if c < 0 else "")))
                        v = abs(c)
                        if j == 0: partes.append(f"{c:.4f}")
                        elif j == 1: partes.append(f"{s}{v:.4f}x")
                        else: partes.append(f"{s}{v:.4f}x^{{{j}}}")
                    st.latex(f"P(x) = {''.join(partes)}")
                    st.caption("Matriz de Vandermonde")
                    cols_v = [f"x^{j}" for j in range(np_)]
                    df_V = pd.DataFrame(V, columns=cols_v)
                    df_V["y"] = py
                    st.dataframe(df_V.style.format("{:.4f}"), use_container_width=True)

                elif metodo == "Lagrange":
                    res, polys_L, P_sym = interpolacao_lagrange_detalhada(px, py, x_ev)
                    c1, c2 = st.columns(2)
                    card(c1, f"P({x_ev})", f"{res:.6f}")
                    card(c2, "Grau", str(grau))
                    st.latex(f"P(x) = {sp.latex(P_sym)}")
                    tab_L = [{"i": it['i'], "xᵢ": it['xi'], "yᵢ": it['yi'],
                               f"Lᵢ(x*)": it['L_val'], f"yᵢ·Lᵢ(x*)": it['termo_val']} for it in polys_L]
                    st.dataframe(pd.DataFrame(tab_L).style.format(precision=6), use_container_width=True)

                elif metodo == "Newton":
                    res, tab_diff, coefs_n, P_sym = interpolacao_newton_detalhada(px, py, x_ev)
                    c1, c2 = st.columns(2)
                    card(c1, f"P({x_ev})", f"{res:.6f}")
                    card(c2, "Grau", str(grau))
                    st.latex(f"P(x) = {sp.latex(P_sym)}")
                    st.caption("Tabela de diferenças divididas")
                    cols_dd = [f"Ordem {j}" for j in range(np_)]
                    df_dd = pd.DataFrame(tab_diff, columns=cols_dd)
                    df_dd.insert(0, "xᵢ", px)
                    st.dataframe(df_dd.style.format(precision=6, na_rep=""), use_container_width=True)

                elif metodo == "Comparar os três":
                    r_v, _, _ = interpolacao_definicao_detalhada(px, py, x_ev)
                    r_l, _, _ = interpolacao_lagrange_detalhada(px, py, x_ev)
                    r_n, _, _, _ = interpolacao_newton_detalhada(px, py, x_ev)
                    st.caption("Pelo teorema da unicidade, os três métodos produzem o mesmo resultado.")
                    c1, c2, c3 = st.columns(3)
                    card(c1, "Vandermonde", f"{r_v:.6f}")
                    card(c2, "Lagrange", f"{r_l:.6f}")
                    card(c3, "Newton", f"{r_n:.6f}")
                    res = r_v

                xmn, xmx = min(px), max(px)
                sp_ = max(abs(xmx - xmn), 1.0)
                xd = np.linspace(xmn - 0.2*sp_, xmx + 0.2*sp_, 400)
                pf = np.poly1d(np.polyfit(px, py, grau))
                yd = pf(xd)
                rv = res if res is not None else pf(x_ev)

                fig = fig_base(f"Polinômio interpolador grau {grau}", "x", "P(x)")
                fig.add_trace(go.Scatter(x=xd, y=yd, mode='lines', name='P(x)',
                                         line=dict(color='#60A5FA', width=2)))
                fig.add_trace(go.Scatter(x=px, y=py, mode='markers', name='Nós',
                                         marker=dict(size=8, color='#F87171')))
                fig.add_trace(go.Scatter(x=[x_ev], y=[rv], mode='markers',
                                         name=f'P({x_ev})',
                                         marker=dict(size=10, color='#34D399', symbol='diamond')))
                st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(str(e))


elif categoria == "Integração Numérica":
    st.header("Integração Numérica")

    metodo = st.sidebar.selectbox("Método", ["Trapézios Repetida", "1ª Regra de Simpson", "Comparar os dois"])

    preset_in = st.selectbox(
        "Função",
        ["x² em [0, 2]", "xˆ3−9xˆ2+3 em [0, 2]", "sen(x) em [0, π]", "e^x em [0, 1]", "1/(1+x²) em [0, 1]", "Personalizado"]
    )
    presets_in = {
        "x² em [0, 2]":          ("x^2",              0.0, 2.0),
        "xˆ3−9xˆ2+3 em [0, 2]": ("xˆ3-9xˆ2+3",      0.0, 2.0),
        "sen(x) em [0, π]":      ("sen(x)",            0.0, float(math.pi)),
        "e^x em [0, 1]":         ("e^x",               0.0, 1.0),
        "1/(1+x²) em [0, 1]":    ("1/(1+x^2)",         0.0, 1.0),
    }
    def_fn, def_a, def_b = presets_in.get(preset_in, ("x^2", 0.0, 2.0))

    fn_raw = st.sidebar.text_input("Integranda f(x)", value=def_fn)
    fn_py, fn_latex, err_fn = processa_expressao_natural(fn_raw)

    sintaxe_sidebar()

    ca, cb = st.sidebar.columns(2)
    a = ca.number_input("a", value=def_a)
    b = cb.number_input("b", value=def_b)

    step_n = 2 if "Simpson" in metodo else 1
    n_sub = st.sidebar.number_input("Subintervalos n", value=10, min_value=2, step=step_n)

    if st.sidebar.button("Calcular", type="primary", use_container_width=True):
        if b <= a:
            st.error("b deve ser maior que a.")
        elif "Simpson" in metodo and n_sub % 2 != 0:
            st.error("Para Simpson, n deve ser par.")
        elif err_fn or not fn_py:
            st.error(f"Expressão inválida: {err_fn}")
        else:
            try:
                xs = sp.Symbol('x')
                f_sym = sp.sympify(fn_py)
                int_sym = sp.integrate(f_sym, (xs, a, b))
                tem_exata = False
                try:
                    exato = float(int_sym.evalf())
                    tem_exata = True
                except Exception:
                    exato = None

                ls = lim_str(a)
                lb = lim_str(b)
                if any(op in fn_latex for op in ['+', '-']):
                    st.latex(rf"I = \int_{{{ls}}}^{{{lb}}} \left( {fn_latex} \right) dx")
                else:
                    st.latex(rf"I = \int_{{{ls}}}^{{{lb}}} {fn_latex} \, dx")

                if metodo == "Trapézios Repetida":
                    area, h, tab_p, soma_i, subints = regra_trapezios_detalhada(fn_py, a, b, n_sub)
                    err_abs = abs(area - exato) if tem_exata else None

                    c1, c2, c3 = st.columns(3)
                    card(c1, "Área aproximada", f"{area:.6f}")
                    card(c2, "Valor analítico", f"{exato:.6f}" if tem_exata else "—")
                    card(c3, "Erro absoluto", fmt_sci(err_abs))
                    st.markdown(f"<div class='nota-rodape'>Ordem O(h²) &nbsp;|&nbsp; h = {h:.6f} &nbsp;|&nbsp; n = {n_sub}</div>", unsafe_allow_html=True)

                    xp = np.linspace(a, b, 400)
                    yp = [avalia_funcao(fn_py, v) for v in xp]
                    fig = fig_base(f"Aproximação por {n_sub} trapézios")
                    for i, sub in enumerate(subints):
                        fig.add_trace(go.Scatter(
                            x=[sub['x0'], sub['x0'], sub['x1'], sub['x1'], sub['x0']],
                            y=[0, sub['y0'], sub['y1'], 0, 0],
                            fill='toself', fillcolor='rgba(59,130,246,0.12)',
                            line=dict(color='#3B82F6', width=1),
                            mode='lines', showlegend=(i == 0), name='Trapézios'
                        ))
                    fig.add_trace(go.Scatter(x=xp, y=yp, mode='lines', name='f(x)',
                                             line=dict(color='#E5E7EB', width=2)))
                    xn = [r['xi'] for r in tab_p]
                    yn = [r['f(xi)'] for r in tab_p]
                    fig.add_trace(go.Scatter(x=xn, y=yn, mode='markers', name='Nós',
                                             marker=dict(size=5, color='#60A5FA')))
                    st.plotly_chart(fig, use_container_width=True)

                    with st.expander("Tabela de nós e ponderações"):
                        st.dataframe(pd.DataFrame(tab_p).style.format(precision=6), use_container_width=True)

                elif metodo == "1ª Regra de Simpson":
                    area, h, tab_p, s_imp, s_par, segs = regra_simpson_detalhada(fn_py, a, b, n_sub)
                    err_abs = abs(area - exato) if tem_exata else None

                    c1, c2, c3 = st.columns(3)
                    card(c1, "Área aproximada", f"{area:.6f}")
                    card(c2, "Valor analítico", f"{exato:.6f}" if tem_exata else "—")
                    card(c3, "Erro absoluto", fmt_sci(err_abs))
                    st.markdown(f"<div class='nota-rodape'>Ordem O(h⁴) &nbsp;|&nbsp; h = {h:.6f} &nbsp;|&nbsp; {n_sub//2} arcos parabólicos</div>", unsafe_allow_html=True)

                    xp = np.linspace(a, b, 400)
                    yp = [avalia_funcao(fn_py, v) for v in xp]
                    fig = fig_base(f"Aproximação por {n_sub//2} arcos de Simpson")
                    for i, seg in enumerate(segs):
                        pp = np.poly1d(np.polyfit(seg['x_pts'], seg['y_pts'], 2))
                        xs_ = np.linspace(seg['x_pts'][0], seg['x_pts'][2], 50)
                        ys_ = pp(xs_)
                        fig.add_trace(go.Scatter(
                            x=np.concatenate([[xs_[0]], xs_, [xs_[-1]], [xs_[0]]]),
                            y=np.concatenate([[0], ys_, [0], [0]]),
                            fill='toself', fillcolor='rgba(16,185,129,0.12)',
                            line=dict(color='#10B981', width=1),
                            mode='lines', showlegend=(i == 0), name='Arcos parabólicos'
                        ))
                    fig.add_trace(go.Scatter(x=xp, y=yp, mode='lines', name='f(x)',
                                             line=dict(color='#E5E7EB', width=2)))
                    xn = [r['xi'] for r in tab_p]
                    yn = [r['f(xi)'] for r in tab_p]
                    fig.add_trace(go.Scatter(x=xn, y=yn, mode='markers', name='Nós',
                                             marker=dict(size=5, color='#34D399')))
                    st.plotly_chart(fig, use_container_width=True)

                    with st.expander("Tabela de nós e ponderações"):
                        st.dataframe(pd.DataFrame(tab_p).style.format(precision=6), use_container_width=True)

                elif metodo == "Comparar os dois":
                    np_ = n_sub if n_sub % 2 == 0 else n_sub + 1
                    a_trap = regra_trapezios_repetida(fn_py, a, b, np_)
                    a_simp = regra_simpson_13(fn_py, a, b, np_)

                    c1, c2 = st.columns(2)
                    card(c1, "Trapézios — O(h²)", f"{a_trap:.6f}")
                    card(c2, "Simpson — O(h⁴)", f"{a_simp:.6f}")

                    dados = [
                        {"Método": "Trapézios Repetida", "Ordem": "O(h²)", "Resultado": f"{a_trap:.6f}",
                         "Erro": fmt_sci(abs(a_trap - exato)) if tem_exata else "—"},
                        {"Método": "1ª Regra de Simpson", "Ordem": "O(h⁴)", "Resultado": f"{a_simp:.6f}",
                         "Erro": fmt_sci(abs(a_simp - exato)) if tem_exata else "—"},
                    ]
                    if tem_exata:
                        st.markdown(f"<div class='nota-rodape'>Valor analítico: {exato:.6f}</div>", unsafe_allow_html=True)
                    st.dataframe(pd.DataFrame(dados), use_container_width=True)

            except Exception as e:
                st.error(str(e))

