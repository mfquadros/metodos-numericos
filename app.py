import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import math
import sympy as sp
import os
import time

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

def carregar_css(caminho_css="style.css"):
    if os.path.exists(caminho_css):
        with open(caminho_css, "r", encoding="utf-8") as f:
            css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

carregar_css("style.css")


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
        title=dict(text=titulo, font=dict(size=13, color="var(--text-color)", family="Inter, sans-serif"), x=0, xref="paper"),
        xaxis=dict(
            title=dict(text=xlabel, font=dict(size=12, color="var(--text-color)")),
            gridcolor="rgba(128, 128, 128, 0.1)",
            zerolinecolor="rgba(128, 128, 128, 0.2)",
            zerolinewidth=1,
            linecolor="rgba(128, 128, 128, 0.3)", showline=True,
            tickfont=dict(color="var(--text-color)", size=11)
        ),
        yaxis=dict(
            title=dict(text=ylabel, font=dict(size=12, color="var(--text-color)")),
            gridcolor="rgba(128, 128, 128, 0.1)",
            zerolinecolor="rgba(128, 128, 128, 0.2)",
            zerolinewidth=1,
            linecolor="rgba(128, 128, 128, 0.3)", showline=True,
            tickfont=dict(color="var(--text-color)", size=11)
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        hoverlabel=dict(font_size=11, font_family="JetBrains Mono, monospace"),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
            bgcolor="rgba(0,0,0,0)", bordercolor="rgba(128, 128, 128, 0.2)", borderwidth=1,
            font=dict(size=10)
        ),
        margin=dict(l=48, r=20, t=44, b=44),
        height=420,
        autosize=True
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


ARQUIVOS_METODOS = {
    "Bisseção": ["bissecao.py"],
    "Falsa Posição": ["falsa_posicao.py"],
    "Newton-Raphson": ["newton.py"],
    "Secantes": ["secantes.py"],
    "Eliminação de Gauss": ["eliminacao_gauss.py"],
    "Fatoração LU": ["fatoracao_lu.py"],
    "Gauss-Jacobi": ["gauss_jacobi.py"],
    "Gauss-Seidel": ["gauss_seidel.py"],
    "Mínimos Quadrados (Ajuste Polinomial)": ["ajuste_polinomial.py"],
    "Definição (Vandermonde)": ["interpolacao_definicao.py"],
    "Lagrange": ["interpolacao_lagrange.py"],
    "Newton": ["interpolacao_newton.py"],
    "Comparar os três": ["interpolacao_definicao.py", "interpolacao_lagrange.py", "interpolacao_newton.py"],
    "Trapézios Repetida": ["regra_trapezios.py"],
    "1ª Regra de Simpson": ["regra_simpson.py"],
    "Comparar os dois": ["regra_trapezios.py", "regra_simpson.py"]
}

@st.dialog("Código", width="large")
def exibir_modal_codigo(metodo_nome):
    arquivos = ARQUIVOS_METODOS.get(metodo_nome, [])
    if not arquivos:
        st.warning("Código não encontrado para este método.")
        return

    st.markdown(f"### {metodo_nome}")
    for nome_arq in arquivos:
        st.caption(f"Arquivo: `{nome_arq}`")
        if os.path.exists(nome_arq):
            with open(nome_arq, "r", encoding="utf-8") as f:
                conteudo = f.read()
            st.code(conteudo, language="python")
            st.download_button(
                label=f"Baixar {nome_arq}",
                data=conteudo,
                file_name=nome_arq,
                mime="text/x-python",
                use_container_width=True,
                key=f"dl_{metodo_nome}_{nome_arq}"
            )
        else:
            st.error(f"Arquivo '{nome_arq}' não foi encontrado no diretório do projeto.")
        st.markdown("---")


def badge_metodo(categoria, metodo):
    col_b1, col_b2 = st.columns([4, 1])
    with col_b1:
        st.markdown(
            f"<div style='background: var(--secondary-background-color); padding: 8px 14px; border-radius: 6px; "
            f"border-left: 4px solid #2563EB; margin-bottom: 18px; font-weight: 500; font-size: 0.9rem; color: var(--text-color);'>"
            f"Módulo: <b>{categoria}</b> &nbsp;|&nbsp; Método Ativo: <span style='color: #2563EB; font-weight: 600;'>{metodo}</span>"
            f"</div>",
            unsafe_allow_html=True
        )
    with col_b2:
        if st.button("Ver Código", key=f"btn_code_{categoria}_{metodo}", use_container_width=True):
            exibir_modal_codigo(metodo)


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


if categoria == "Zeros de Funções":
    metodo = st.sidebar.selectbox("Método", ["Bisseção", "Falsa Posição", "Newton-Raphson", "Secantes"])
    badge_metodo(categoria, metodo)

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
    def_expr, def_a, def_b, def_chute, def_x0, def_x1 = exemplos_map.get(exemplo, ("x^2 - 4", 0.0, 3.0, 1.0, 0.0, 3.0))

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

    def executar_calculo_zeros(a_v=None, b_v=None, chute_v=None, x0_v=None, x1_v=None):
        st.session_state.zeros_metodo = metodo
        st.session_state.zeros_expr_py = expr_py
        st.session_state.zeros_expr_raw = expr_raw
        st.session_state.zeros_expr_latex = expr_latex
        st.session_state.zeros_err_msg = None

        if err_parse or not expr_py:
            st.session_state.zeros_err_msg = f"Expressão inválida: {err_parse}"
            st.session_state.zeros_raiz = None
            st.session_state.zeros_hist = []
            return

        try:
            if metodo in ["Bisseção", "Falsa Posição"]:
                fa, fb = avalia_funcao(expr_py, a_v), avalia_funcao(expr_py, b_v)
                if fa * fb > 0:
                    st.session_state.zeros_err_msg = f"Bolzano não satisfeito: f({a_v}) = {fa:.4f} e f({b_v}) = {fb:.4f} têm o mesmo sinal."
                    st.session_state.zeros_raiz = None
                    st.session_state.zeros_hist = []
                else:
                    fn = bissecao if metodo == "Bisseção" else falsa_posicao
                    r, hist = fn(expr_py, a_v, b_v, tol, max_iter=max_iter)
                    st.session_state.zeros_raiz = r
                    st.session_state.zeros_hist = hist

            elif metodo == "Newton-Raphson":
                r, hist = newton(expr_py, chute_v, tol, max_iter=max_iter)
                st.session_state.zeros_raiz = r
                st.session_state.zeros_hist = hist

            elif metodo == "Secantes":
                r, hist = secantes(expr_py, x0_v, x1_v, tol, max_iter=max_iter)
                st.session_state.zeros_raiz = r
                st.session_state.zeros_hist = hist

        except Exception as e:
            st.session_state.zeros_err_msg = str(e)
            st.session_state.zeros_raiz = None
            st.session_state.zeros_hist = []

    if metodo in ["Bisseção", "Falsa Posição"]:
        ca, cb = st.sidebar.columns(2)
        a = ca.number_input("a", value=def_a)
        b = cb.number_input("b", value=def_b)
        if st.sidebar.button("Calcular", type="primary", use_container_width=True) or not st.session_state.zeros_hist:
            executar_calculo_zeros(a_v=a, b_v=b)

    elif metodo == "Newton-Raphson":
        chute = st.sidebar.number_input("Chute inicial x₀", value=def_chute)
        if st.sidebar.button("Calcular", type="primary", use_container_width=True) or not st.session_state.zeros_hist:
            executar_calculo_zeros(chute_v=chute)

    elif metodo == "Secantes":
        cx0, cx1 = st.sidebar.columns(2)
        x0 = cx0.number_input("x₀", value=def_x0)
        x1 = cx1.number_input("x₁", value=def_x1)
        if st.sidebar.button("Calcular", type="primary", use_container_width=True) or not st.session_state.zeros_hist:
            executar_calculo_zeros(x0_v=x0, x1_v=x1)

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

        total_steps = len(historico)
        cp_play, cp_slider = st.columns([1, 4])
        btn_play = cp_play.button("▶ Reproduzir", key="btn_play_zeros", use_container_width=True)
        passo_selecionado = cp_slider.slider("Iteração", 1, total_steps, total_steps, key="slider_zeros")

        tab_g, tab_t = st.tabs(["Gráfico de Convergência", "Tabela de Iterações"])

        with tab_g:
            plot_spot = st.empty()

            def desenha_grafico(step):
                xs = [h['x'] for h in historico if h.get('x') is not None]
                mn, mx = min(xs), max(xs)
                span = max(abs(mx - mn), 1.0)
                xp0, xp1 = mn - 0.5 * span, mx + 0.5 * span
                xv = np.linspace(xp0, xp1, 600)
                yv = [avalia_funcao(expr_p, xvv) for xvv in xv]

                fig = fig_base(f"Convergência ({met_calc}) — Iteração {step} de {total_steps}", xlabel="x", ylabel="f(x)")
                fig.add_trace(go.Scatter(x=xv, y=yv, mode='lines', name='f(x)', line=dict(color='#2563EB', width=2)))

                tx = [historico[i]['x'] for i in range(step) if historico[i].get('x') is not None]
                ty = [historico[i]['y'] for i in range(step) if historico[i].get('y') is not None]
                fig.add_trace(go.Scatter(x=tx, y=ty, mode='markers+lines', name='Trajetória',
                                         marker=dict(size=6, color='#64748B'),
                                         line=dict(color='#94A3B8', dash='dot', width=1)))

                pa = historico[step - 1]
                fig.add_trace(go.Scatter(x=[pa['x']], y=[pa['y']], mode='markers', name='Ponto atual',
                                         marker=dict(size=10, color='#10B981', symbol='diamond')))

                if met_calc in ["Bisseção", "Falsa Posição"] and 'a' in pa and 'b' in pa:
                    fig.add_vline(x=pa['a'], line_dash="dash", line_color="#64748B", line_width=1, annotation_text=f"a={pa['a']:.3f}")
                    fig.add_vline(x=pa['b'], line_dash="dash", line_color="#64748B", line_width=1, annotation_text=f"b={pa['b']:.3f}")

                plot_spot.plotly_chart(fig, use_container_width=True)

            if btn_play:
                for k in range(1, total_steps + 1):
                    desenha_grafico(k)
                    time.sleep(0.2)
            else:
                desenha_grafico(passo_selecionado)

        with tab_t:
            st.dataframe(pd.DataFrame(historico[:passo_selecionado]), use_container_width=True)


elif categoria == "Sistemas Lineares":
    metodo = st.sidebar.selectbox(
        "Método",
        ["Eliminação de Gauss", "Fatoração LU", "Gauss-Jacobi", "Gauss-Seidel"]
    )
    badge_metodo(categoria, metodo)

    preset = st.sidebar.selectbox("Exemplo / Fonte de Dados", ["Diagonal dominante", "Simétrico positivo definido", "Matriz Gigante 100x100 (Tridiagonal)", "Upload de Arquivo (CSV / TXT / JSON)", "Personalizado"])

    def gerar_matriz_100x100():
        dim = 100
        A = [[0.0]*dim for _ in range(dim)]
        b = [0.0]*dim
        for i in range(dim):
            A[i][i] = 10.0
            if i > 0:
                A[i][i-1] = -2.0
            if i < dim - 1:
                A[i][i+1] = -2.0
            b[i] = 6.0
        b[0] = 8.0
        b[dim-1] = 8.0
        return A, b, dim

    A_in = None
    b_in = None
    n = 3

    if preset == "Matriz Gigante 100x100 (Tridiagonal)":
        A_in, b_in, n = gerar_matriz_100x100()
        st.info("Matriz Tridiagonal 100x100 carregada com sucesso! A[i][i]=10, sub/superdiagonais=-2, b=[8, 6, ..., 6, 8].")
    elif preset == "Upload de Arquivo (CSV / TXT / JSON)":
        st.markdown("**Upload de Sistema Linear**")
        arquivo = st.file_uploader("Envie um arquivo CSV/TXT (linhas da matriz A + última coluna b) ou JSON (chaves 'A' e 'b')", type=["csv", "txt", "json"])
        if arquivo is not None:
            try:
                if arquivo.name.endswith('.json'):
                    import json
                    dados = json.load(arquivo)
                    A_in = dados['A']
                    b_in = dados['b']
                    n = len(A_in)
                else:
                    df_up = pd.read_csv(arquivo, header=None)
                    mat_vals = df_up.values.tolist()
                    n = len(mat_vals)
                    A_in = [row[:n] for row in mat_vals]
                    b_in = [row[n] if len(row) > n else 1.0 for row in mat_vals]
                st.success(f"Sistema {n}x{n} carregado do arquivo '{arquivo.name}'!")
            except Exception as e_up:
                st.error(f"Erro ao ler arquivo: {str(e_up)}")
                n = 3
        else:
            st.warning("Aguardando upload do arquivo. Carregando sistema 3x3 padrão temporariamente.")
            n = 3
    else:
        n = st.sidebar.number_input("Dimensão n×n", min_value=2, max_value=100, value=3, step=1)

    presets = {
        "Diagonal dominante": {
            2: ([[5., 1.], [2., 6.]], [7., 16.]),
            3: ([[10., 2., 1.], [1., 5., 1.], [2., 3., 10.]], [7., -8., 6.]),
            4: ([[10.,-1., 2., 0.],[-1.,11.,-1., 3.],[2.,-1.,10.,-1.],[0., 3.,-1., 8.]], [6.,25.,-11.,15.]),
            5: ([[12., 1., 2., 0., 1.], [1., 10., -1., 2., 0.], [2., -1., 11., 1., -1.], [0., 2., 1., 9., 1.], [1., 0., -1., 1., 8.]], [16., 12., 12., 13., 9.]),
            6: ([[15., 1., 2., 0., 1., 0.], [1., 12., -1., 2., 0., 1.], [2., -1., 14., 1., -1., 0.], [0., 2., 1., 11., 1., 2.], [1., 0., -1., 1., 10., 1.], [0., 1., 0., 2., 1., 9.]], [19., 15., 15., 17., 12., 13.])
        },
        "Simétrico positivo definido": {
            2: ([[4., 1.], [1., 3.]], [1., 2.]),
            3: ([[4.,-1., 0.],[-1., 4.,-1.],[0.,-1., 4.]], [1., 2., 3.]),
            4: ([[4., 1., 0., 0.],[1., 4., 1., 0.],[0., 1., 4., 1.],[0., 0., 1., 4.]], [1., 2., 3., 4.]),
            5: ([[5., 1., 0., 0., 0.], [1., 5., 1., 0., 0.], [0., 1., 5., 1., 0.], [0., 0., 1., 5., 1.], [0., 0., 0., 1., 5.]], [1., 2., 3., 4., 5.]),
            6: ([[6., 1., 0., 0., 0., 0.], [1., 6., 1., 0., 0., 0.], [0., 1., 6., 1., 0., 0.], [0., 0., 1., 6., 1., 0.], [0., 0., 0., 1., 6., 1.], [0., 0., 0., 0., 1., 6.]], [1., 2., 3., 4., 5., 6.])
        },
    }

    if A_in is None:
        if preset in presets and n in presets[preset]:
            dA, db = presets[preset][n]
        else:
            dA = [[1. if i == j else 0. for j in range(n)] for i in range(n)]
            db = [1.] * n

        A_in = [[0.] * n for _ in range(n)]
        b_in = [0.] * n

        with st.expander(f"Editar coeficientes da Matriz A e b ({n}×{n})", expanded=(n <= 6)):
            hdrs = st.columns(n + 1)
            for j in range(n):
                hdrs[j].markdown(f"<div style='text-align:center;font-size:0.8rem;opacity:0.7;'>x{j+1}</div>", unsafe_allow_html=True)
            hdrs[n].markdown("<div style='text-align:center;font-size:0.8rem;opacity:0.7;'>b</div>", unsafe_allow_html=True)

            for i in range(n):
                row = st.columns(n + 1)
                for j in range(n):
                    val_default = float(dA[i][j]) if i < len(dA) and j < len(dA[0]) else 0.0
                    A_in[i][j] = row[j].number_input(f"A{i+1}{j+1}", value=val_default, key=f"A_{n}_{preset}_{i}_{j}", label_visibility="collapsed")
                val_b_default = float(db[i]) if i < len(db) else 0.0
                b_in[i] = row[n].number_input(f"b{i+1}", value=val_b_default, key=f"b_{n}_{preset}_{i}", label_visibility="collapsed")
    else:
        with st.expander(f"Visualizar Preview da Matriz A e b ({n}×{n})", expanded=True):
            df_preview = pd.DataFrame(A_in, columns=[f"x{j+1}" for j in range(n)])
            df_preview["b"] = b_in
            st.dataframe(df_preview, use_container_width=True)

    tol_it, max_it, x0 = 1e-4, 50, [0.0] * n
    if "Jacobi" in metodo or "Seidel" in metodo:
        st.markdown("---")
        ct, cm, cx = st.columns(3)
        tol_it = ct.number_input("Tolerância ε", value=1e-4, format="%.2e")
        max_it = cm.number_input("Máx. iterações", value=50, min_value=5, max_value=5000)
        x0_v = cx.number_input("Chute inicial x⁽⁰⁾", value=0.0)
        x0 = [x0_v] * n

    if st.button("Resolver Sistema", type="primary", use_container_width=True):
        st.session_state.metodo_sl = metodo
        # Limpa resultados anteriores do session state
        for key in ["gauss_sol", "gauss_etapas", "lu_sol", "sistemas_sol", "sistemas_hist", "sl_err_msg"]:
            if key in st.session_state:
                del st.session_state[key]

        try:
            if metodo == "Eliminação de Gauss":
                sol, etapas = eliminacao_gauss_detalhada(A_in, b_in)
                if sol:
                    st.session_state.gauss_sol = sol
                    st.session_state.gauss_etapas = etapas
                else:
                    st.session_state.sl_err_msg = "Eliminação de Gauss falhou: Sistema singular ou pivô nulo encravado na diagonal."

            elif metodo == "Fatoração LU":
                sol, L, U, y = fatoracao_lu_detalhada(A_in, b_in)
                if sol:
                    st.session_state.lu_sol = (sol, L, U, y)
                else:
                    st.session_state.sl_err_msg = "Fatoração LU falhou: Encontrado pivô nulo ou divisão por zero."

            elif metodo in ["Gauss-Jacobi", "Gauss-Seidel"]:
                fn_iter = gauss_jacobi_detalhado if metodo == "Gauss-Jacobi" else gauss_seidel_detalhado
                resultado = fn_iter(A_in, b_in, x0, tol_it, max_it)
                
                # Trata retornos com sol ou histórico de iterações
                if isinstance(resultado, tuple) and len(resultado) >= 2:
                    sol, hist = resultado[0], resultado[1]
                    if sol is not None and len(hist) > 0:
                        st.session_state.sistemas_sol = sol
                        st.session_state.sistemas_hist = hist
                    else:
                        # Se não convergiu mas gerou histórico ou sol veio None
                        if hist and len(hist) > 0:
                            st.session_state.sistemas_hist = hist
                            st.session_state.sl_err_msg = f"O método {metodo} não convergiu em {max_it} iterações (divergência ou estouro de iterações)."
                        else:
                            st.session_state.sl_err_msg = f"Falha ao executar {metodo}: Verifique se há zeros na diagonal principal de A."
                else:
                    st.session_state.sl_err_msg = f"O método {metodo} não retornou um resultado válido."

        except Exception as e:
            st.session_state.sl_err_msg = f"Erro na execução do cálculo: {str(e)}" 

    met_ativo_sl = st.session_state.get("metodo_sl", metodo)

    if st.session_state.get("sl_err_msg"):
        st.error(st.session_state.sl_err_msg)

    if met_ativo_sl == "Eliminação de Gauss" and "gauss_sol" in st.session_state:
        sol = st.session_state.gauss_sol
        etapas = st.session_state.gauss_etapas
        st.markdown("**Vetor Solução x:**")
        df_sol = pd.DataFrame([sol], columns=[f"x{i+1}" for i in range(len(sol))])
        st.dataframe(df_sol.style.format("{:.6f}"), use_container_width=True)

        st.markdown("**Passos do Escalonamento:**")
        for et in etapas:
            st.caption(f"Passo {et['passo']} — {et['descricao']}")
            df_e = pd.DataFrame(et['matriz'], columns=[f"x{j+1}" for j in range(len(sol))] + ["b"])
            st.dataframe(df_e.style.format("{:.4f}"), use_container_width=True)

    elif met_ativo_sl == "Fatoração LU" and "lu_sol" in st.session_state:
        sol, L, U, y = st.session_state.lu_sol
        st.markdown("**Vetor Solução x:**")
        df_sol = pd.DataFrame([sol], columns=[f"x{i+1}" for i in range(len(sol))])
        st.dataframe(df_sol.style.format("{:.6f}"), use_container_width=True)

        cL, cU = st.columns(2)
        with cL:
            st.caption("Matriz L (Triangular Inferior)")
            st.dataframe(pd.DataFrame(L, columns=[f"c{j+1}" for j in range(len(sol))]).style.format("{:.4f}"), use_container_width=True)
        with cU:
            st.caption("Matriz U (Triangular Superior)")
            st.dataframe(pd.DataFrame(U, columns=[f"c{j+1}" for j in range(len(sol))]).style.format("{:.4f}"), use_container_width=True)

    elif ("sistemas_hist" in st.session_state) and ("Jacobi" in met_ativo_sl or "Seidel" in met_ativo_sl):
        hist = st.session_state.sistemas_hist
        sol = st.session_state.get("sistemas_sol")

        if sol is not None:
            st.markdown("**Vetor Solução x (Aproximação Final):**")
            df_sol = pd.DataFrame([sol], columns=[f"x{i+1}" for i in range(len(sol))])
            st.dataframe(df_sol.style.format("{:.6f}"), use_container_width=True)
            st.caption(f"Total de iterações para convergência: {len(hist) - 1}")

        tot_sys = len(hist)
        passo_sys = st.slider("Iteração do Histórico", 1, tot_sys, tot_sys, key="slider_sys")

        tab_t, tab_g = st.tabs(["Tabela de Iterações", "Gráfico do Erro"])

        with tab_t:
            rows = []
            for h in hist[:passo_sys]:
                r = {"k": h['iter']}
                for i, v in enumerate(h['x']): r[f"x{i+1}"] = v
                r["erro"] = h['erro'] if h['erro'] is not None else 0.
                rows.append(r)
            st.dataframe(pd.DataFrame(rows).style.format(precision=6), use_container_width=True)

        with tab_g:
            erros = [h['erro'] for h in hist[:passo_sys] if h['erro'] is not None]
            if erros:
                fig = fig_base(f"Convergência do Erro — Iteração 1 até {passo_sys}", "Iteração (k)", "Erro Relativo (Log)")
                fig.add_trace(go.Scatter(
                    x=list(range(1, len(erros)+1)), y=erros,
                    mode='lines+markers', name='Erro',
                    line=dict(color='#2563EB', width=2),
                    marker=dict(size=6, color='#1E40AF')
                ))
                fig.update_layout(yaxis_type="log")
                st.plotly_chart(fig, use_container_width=True)


elif categoria == "Ajuste de Curvas":
    st.header("Ajuste de Curvas — Mínimos Quadrados")
    badge_metodo(categoria, "Mínimos Quadrados (Ajuste Polinomial)")

    preset_aj = st.selectbox("Conjunto de dados", ["Linear com ruído", "Parábola", "Cúbica", "Personalizado"])
    presets_aj = {
        "Linear com ruído": ("1, 2, 3, 4, 5, 6", "1.2, 1.9, 3.2, 4.1, 5.3, 7.1", 1),
        "Parábola":         ("0, 1, 2, 3, 4, 5", "2.1, 5.0, 10.2, 17.1, 26.0, 37.3", 2),
        "Cúbica":           ("-2,-1, 0, 1, 2, 3", "-7.8,-0.9, 1.1, 3.2, 9.8, 28.1", 3),
    }
    def_x, def_y, def_g = presets_aj.get(preset_aj, ("1, 2, 3, 4, 5", "1.0, 2.0, 2.5, 3.5, 5.0", 2))

    col1, col2 = st.columns(2)
    str_x = col1.text_input("Coordenadas X (separadas por vírgula)", def_x)
    str_y = col2.text_input("Coordenadas Y (separadas por vírgula)", def_y)
    cg, cp = st.columns(2)
    grau = cg.number_input("Grau do polinômio", min_value=1, max_value=6, value=def_g)
    x_ev = cp.number_input("Avaliar em x*", value=2.5)

    try:
        px = [float(v.strip()) for v in str_x.split(",") if v.strip()]
        py = [float(v.strip()) for v in str_y.split(",") if v.strip()]
        if len(px) != len(py):
            st.error("X e Y devem ter o mesmo número de elementos.")
        elif len(px) <= grau:
            st.error(f"Pontos ({len(px)}) insuficientes para grau {grau}.")
        else:
            coefs, matA, vecB, r2, sqe, sqt, res_tab = ajuste_polinomial_detalhado(px, py, grau)

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

            fig = fig_base(f"Ajuste Polinomial Grau {grau}", "x", "y")
            fig.add_trace(go.Scatter(x=xc, y=yc, mode='lines', name=f'P_{grau}(x)', line=dict(color='#2563EB', width=2)))
            fig.add_trace(go.Scatter(x=px, y=py, mode='markers', name='Dados', marker=dict(size=8, color='#EF4444')))
            fig.add_trace(go.Scatter(x=[x_ev], y=[y_pred], mode='markers', name=f'P({x_ev})', marker=dict(size=10, color='#10B981', symbol='diamond')))
            st.plotly_chart(fig, use_container_width=True)

            tab_s, tab_r = st.tabs(["Equações Normais", "Resíduos"])
            with tab_s:
                df_m = pd.DataFrame(matA, columns=[f"a{k}" for k in range(grau+1)])
                df_m["b"] = vecB
                st.dataframe(df_m.style.format("{:.4f}"), use_container_width=True)
            with tab_r:
                st.dataframe(pd.DataFrame(res_tab).style.format("{:.4f}"), use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao processar o ajuste: {str(e)}")


elif categoria == "Interpolação Polinomial":
    metodo = st.sidebar.selectbox("Método", ["Definição (Vandermonde)", "Lagrange", "Newton", "Comparar os três"])
    badge_metodo(categoria, metodo)

    preset_ip = st.sidebar.selectbox("Conjunto de nós", ["3 pontos", "4 pontos (cúbica)", "Personalizado"])
    presets_ip = {
        "3 pontos":         ("0, 1, 2", "1, 3, 2", 1.5),
        "4 pontos (cúbica)": ("-1, 0, 2, 4", "4, 1, -1, 9", 1.0),
    }
    def_ix, def_iy, def_ie = presets_ip.get(preset_ip, ("0, 1, 2", "1, 3, 2", 1.5))

    cx, cy = st.columns(2)
    str_x = cx.text_input("Nós X", def_ix)
    str_y = cy.text_input("Valores Y", def_iy)
    x_ev = st.number_input("Interpolação em x*", value=float(def_ie))

    try:
        px = [float(v.strip()) for v in str_x.split(",") if v.strip()]
        py = [float(v.strip()) for v in str_y.split(",") if v.strip()]
        if len(px) != len(py):
            st.error("X e Y devem ter o mesmo número de elementos.")
        elif len(set(px)) != len(px):
            st.error("Os nós X devem ser distintos.")
        else:
            grau = len(px) - 1
            r_v, coefs_v, V = interpolacao_definicao_detalhada(px, py, x_ev)
            r_l, polys_L, P_sym_L = interpolacao_lagrange_detalhada(px, py, x_ev)
            r_n, tab_diff, coefs_n, P_sym_N = interpolacao_newton_detalhada(px, py, x_ev)

            if metodo == "Comparar os três":
                st.success("Pelo Teorema da Unicidade do Polinômio Interpolador, todos os três métodos geram o mesmo polinômio e resultado final.")

                c1, c2, c3 = st.columns(3)
                card(c1, "Vandermonde", f"{r_v:.6f}")
                card(c2, "Lagrange", f"{r_l:.6f}")
                card(c3, "Newton", f"{r_n:.6f}")

                df_comp = pd.DataFrame([
                    {"Método": "Definição (Vandermonde)", "P(x*)": f"{r_v:.6f}", "Complexidade": "O(n³)", "Estrutura": "Sistema Linear V·a = y"},
                    {"Método": "Lagrange", "P(x*)": f"{r_l:.6f}", "Complexidade": "O(n²)", "Estrutura": "Soma de polinômios base L_i(x)"},
                    {"Método": "Newton", "P(x*)": f"{r_n:.6f}", "Complexidade": "O(n²)", "Estrutura": "Diferenças Divididas f[x_0,...,x_k]"},
                ])
                st.dataframe(df_comp, use_container_width=True)

            else:
                res_map = {"Definição (Vandermonde)": r_v, "Lagrange": r_l, "Newton": r_n}
                res_atual = res_map.get(metodo, r_v)

                c1, c2 = st.columns(2)
                card(c1, f"P({x_ev})", f"{res_atual:.6f}")
                card(c2, "Grau", str(grau))

                if metodo == "Definição (Vandermonde)":
                    st.caption("Matriz de Vandermonde:")
                    df_V = pd.DataFrame(V, columns=[f"x^{j}" for j in range(len(px))])
                    df_V["y"] = py
                    st.dataframe(df_V.style.format("{:.4f}"), use_container_width=True)

                elif metodo == "Lagrange":
                    st.latex(f"P(x) = {sp.latex(P_sym_L)}")
                    tab_L = [{"i": it['i'], "xᵢ": it['xi'], "yᵢ": it['yi'], "Lᵢ(x*)": f"{it['L_val']:.6f}"} for it in polys_L]
                    st.dataframe(pd.DataFrame(tab_L), use_container_width=True)

                elif metodo == "Newton":
                    st.latex(f"P(x) = {sp.latex(P_sym_N)}")
                    st.caption("Tabela de Diferenças Divididas:")
                    df_dd = pd.DataFrame(tab_diff, columns=[f"Ordem {j}" for j in range(len(px))])
                    df_dd.insert(0, "xᵢ", px)
                    st.dataframe(df_dd.style.format(precision=6, na_rep=""), use_container_width=True)

            xmn, xmx = min(px), max(px)
            sp_ = max(abs(xmx - xmn), 1.0)
            xd = np.linspace(xmn - 0.2*sp_, xmx + 0.2*sp_, 400)
            pf = np.poly1d(np.polyfit(px, py, grau))
            yd = pf(xd)

            fig = fig_base(f"Polinômio Interpolador Grau {grau}", "x", "P(x)")
            fig.add_trace(go.Scatter(x=xd, y=yd, mode='lines', name='P(x)', line=dict(color='#2563EB', width=2)))
            fig.add_trace(go.Scatter(x=px, y=py, mode='markers', name='Nós', marker=dict(size=8, color='#EF4444')))
            fig.add_trace(go.Scatter(x=[x_ev], y=[r_v], mode='markers', name=f'P({x_ev})', marker=dict(size=10, color='#10B981', symbol='diamond')))
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao calcular interpolação: {str(e)}")


elif categoria == "Integração Numérica":
    metodo = st.sidebar.selectbox("Método", ["Trapézios Repetida", "1ª Regra de Simpson", "Comparar os dois"])
    badge_metodo(categoria, metodo)

    preset_in = st.sidebar.selectbox("Função", ["x² em [0, 2]", "xˆ3−9xˆ2+3 em [0, 2]", "sen(x) em [0, π]", "e^x em [0, 1]", "Personalizado"])
    presets_in = {
        "x² em [0, 2]":          ("x^2",              0.0, 2.0),
        "xˆ3−9xˆ2+3 em [0, 2]": ("xˆ3-9xˆ2+3",      0.0, 2.0),
        "sen(x) em [0, π]":      ("sen(x)",            0.0, float(math.pi)),
        "e^x em [0, 1]":         ("e^x",               0.0, 1.0),
    }
    def_fn, def_a, def_b = presets_in.get(preset_in, ("x^2", 0.0, 2.0))

    fn_raw = st.sidebar.text_input("Integranda f(x)", value=def_fn)
    fn_py, fn_latex, err_fn = processa_expressao_natural(fn_raw)

    sintaxe_sidebar()

    ca, cb = st.sidebar.columns(2)
    a = ca.number_input("a", value=def_a)
    b = cb.number_input("b", value=def_b)
    n_sub = st.sidebar.number_input("Subintervalos n", value=10, min_value=2, step=2 if "Simpson" in metodo else 1)

    if b <= a:
        st.error("b deve ser maior que a.")
    elif err_fn or not fn_py:
        st.error(f"Expressão inválida: {err_fn}")
    else:
        try:
            area_t, h_t, tab_t, soma_i_t, subints_t = regra_trapezios_detalhada(fn_py, a, b, n_sub)
            n_simpson = n_sub if n_sub % 2 == 0 else n_sub + 1
            area_s, h_s, tab_s, s_imp_s, s_par_s, segs_s = regra_simpson_detalhada(fn_py, a, b, n_simpson)

            xs_sym = sp.Symbol('x')
            try:
                exato = float(sp.integrate(sp.sympify(fn_py), (xs_sym, a, b)).evalf())
            except Exception:
                exato = None

            if metodo == "Comparar os dois":
                st.markdown("### Comparação entre Trapézios e Simpson")

                c1, c2, c3 = st.columns(3)
                card(c1, "Trapézios — O(h²)", f"{area_t:.6f}", nota=f"Erro Abs: {fmt_sci(abs(area_t-exato)) if exato else '—'}")
                card(c2, "Simpson — O(h⁴)", f"{area_s:.6f}", nota=f"Erro Abs: {fmt_sci(abs(area_s-exato)) if exato else '—'}")
                card(c3, "Valor Analítico (Exato)", f"{exato:.6f}" if exato else "—")

                df_comp_in = pd.DataFrame([
                    {"Método": "Trapézios Repetida", "Resultado": f"{area_t:.6f}", "Ordem de Erro": "O(h²)", "Erro Absoluto": fmt_sci(abs(area_t-exato)) if exato else "—"},
                    {"Método": "1ª Regra de Simpson", "Resultado": f"{area_s:.6f}", "Ordem de Erro": "O(h⁴)", "Erro Absoluto": fmt_sci(abs(area_s-exato)) if exato else "—"},
                ])
                st.dataframe(df_comp_in, use_container_width=True)

                col_g1, col_g2 = st.columns(2)
                xp = np.linspace(a, b, 300)
                yp = [avalia_funcao(fn_py, v) for v in xp]

                with col_g1:
                    fig_t = fig_base(f"Aproximação por Trapézios (n={n_sub})")
                    for sub in subints_t:
                        fig_t.add_trace(go.Scatter(
                            x=[sub['x0'], sub['x0'], sub['x1'], sub['x1'], sub['x0']],
                            y=[0, sub['y0'], sub['y1'], 0, 0],
                            fill='toself', fillcolor='rgba(37, 99, 235, 0.2)',
                            line=dict(color='#2563EB', width=1), mode='lines', showlegend=False
                        ))
                    fig_t.add_trace(go.Scatter(x=xp, y=yp, mode='lines', name='f(x)', line=dict(color='var(--text-color)', width=2)))
                    st.plotly_chart(fig_t, use_container_width=True)

                with col_g2:
                    fig_s = fig_base(f"Aproximação por Simpson (n={n_simpson})")
                    for seg in segs_s:
                        pp = np.poly1d(np.polyfit(seg['x_pts'], seg['y_pts'], 2))
                        xs_ = np.linspace(seg['x_pts'][0], seg['x_pts'][2], 40)
                        ys_ = pp(xs_)
                        fig_s.add_trace(go.Scatter(
                            x=np.concatenate([[xs_[0]], xs_, [xs_[-1]], [xs_[0]]]),
                            y=np.concatenate([[0], ys_, [0], [0]]),
                            fill='toself', fillcolor='rgba(16, 185, 129, 0.2)',
                            line=dict(color='#10B981', width=1), mode='lines', showlegend=False
                        ))
                    fig_s.add_trace(go.Scatter(x=xp, y=yp, mode='lines', name='f(x)', line=dict(color='var(--text-color)', width=2)))
                    st.plotly_chart(fig_s, use_container_width=True)

            else:
                area_atual = area_t if metodo == "Trapézios Repetida" else area_s
                h_atual = h_t if metodo == "Trapézios Repetida" else h_s
                elementos = subints_t if metodo == "Trapézios Repetida" else segs_s

                c1, c2, c3 = st.columns(3)
                card(c1, "Área Aproximada", f"{area_atual:.6f}")
                card(c2, "Valor Analítico", f"{exato:.6f}" if exato else "—")
                card(c3, "Passo h", f"{h_atual:.6f}")

                tot_integ = len(elementos)
                cp_int, cs_int = st.columns([1, 4])
                btn_play_int = cp_int.button("▶ Preencher Área", key="btn_int_play", use_container_width=True)
                passo_int = cs_int.slider("Subintervalos exibidos", 1, tot_integ, tot_integ, key="slider_int")

                plot_int_spot = st.empty()

                def desenha_grafico_integ(step):
                    xp = np.linspace(a, b, 400)
                    yp = [avalia_funcao(fn_py, v) for v in xp]
                    fig = fig_base(f"Construção da Área — Subintervalos 1 a {step} de {tot_integ}")

                    if metodo == "Trapézios Repetida":
                        for sub in elementos[:step]:
                            fig.add_trace(go.Scatter(
                                x=[sub['x0'], sub['x0'], sub['x1'], sub['x1'], sub['x0']],
                                y=[0, sub['y0'], sub['y1'], 0, 0],
                                fill='toself', fillcolor='rgba(37, 99, 235, 0.2)',
                                line=dict(color='#2563EB', width=1), mode='lines', showlegend=False
                            ))
                    else:
                        for seg in elementos[:step]:
                            pp = np.poly1d(np.polyfit(seg['x_pts'], seg['y_pts'], 2))
                            xs_ = np.linspace(seg['x_pts'][0], seg['x_pts'][2], 50)
                            ys_ = pp(xs_)
                            fig.add_trace(go.Scatter(
                                x=np.concatenate([[xs_[0]], xs_, [xs_[-1]], [xs_[0]]]),
                                y=np.concatenate([[0], ys_, [0], [0]]),
                                fill='toself', fillcolor='rgba(16, 185, 129, 0.2)',
                                line=dict(color='#10B981', width=1), mode='lines', showlegend=False
                            ))

                    fig.add_trace(go.Scatter(x=xp, y=yp, mode='lines', name='f(x)', line=dict(color='var(--text-color)', width=2)))
                    plot_int_spot.plotly_chart(fig, use_container_width=True)

                if btn_play_int:
                    for k in range(1, tot_integ + 1):
                        desenha_grafico_integ(k)
                        time.sleep(0.2)
                else:
                    desenha_grafico_integ(passo_int)

        except Exception as e:
            st.error(f"Erro no cálculo numérico: {str(e)}")