# 📐 Métodos Numéricos Computacionais — Visualizador Interativo

> **Suite completa e robusta de algoritmos numéricos implementada em Python e Streamlit, com visualização gráfica passo a passo, gráficos interativos via Plotly, rigor analítico e interface visual moderna.**

---

## 📌 Sumário

1. [Visão Geral](#-visão-geral)
2. [Estrutura do Projeto](#-estrutura-do-projeto)
3. [Detalhamento Teórico e Matemático dos Métodos](#-detalhamento-teórico-e-matemático-dos-métodos)
   - [1) Zeros de Funções](#1-zeros-de-funções)
   - [2) Sistemas Lineares](#2-sistemas-lineares)
   - [3) Ajuste de Curvas](#3-ajuste-de-curvas)
   - [4) Interpolação Polinomial](#4-interpolação-polinomial)
   - [5) Integração Numérica](#5-integração-numérica)
4. [Guia dos Módulos e Algoritmos](#-guia-dos-módulos-e-algoritmos)
5. [Recursos Visuais e Didáticos do App](#-recursos-visuais-e-didáticos-do-app)
6. [Instalação e Execução](#-instalação-e-execução)

---

## 🧭 Visão Geral

Este projeto foi construído para atender com máxima precisão e didática o programa de **Métodos Numéricos Computacionais / Cálculo Numérico**. 

O sistema separa estritamente a **lógica pura de computação numérica** (arquivos `.py` individuais, limpos e sem comentários) da **camada de apresentação interativa** ([app.py](file:///Users/mateusquadros/Desktop/Aulas/Metodos/app.py)), que utiliza Streamlit, Plotly, Pandas e SymPy para gerar análises gráficas, tabelas dinâmicas e resoluções completas com passo a passo.

---

## 📂 Estrutura do Projeto

```text
.
├── app.py                      # Aplicação visual Streamlit principal
├── sanitizador.py              # Tratamento e conversão de entrada natural de funções
├── bissecao.py                 # Método da Bissecção
├── falsa_posicao.py            # Método da Falsa Posição (Regula Falsi)
├── newton.py                   # Método de Newton-Raphson
├── secantes.py                 # Método das Secantes
├── eliminacao_gauss.py         # Eliminação de Gauss com pivoteamento parcial
├── fatoracao_lu.py             # Fatoração LU (Decomposição Doolittle)
├── gauss_jacobi.py             # Gauss-Jacobi com Critério das Linhas
├── gauss_seidel.py             # Gauss-Seidel com Critério de Sassenfeld
├── ajuste_polinomial.py        # Mínimos Quadrados Polinomial com R² e Resíduos
├── interpolacao_definicao.py   # Interpolação via Sistema de Vandermonde
├── interpolacao_lagrange.py    # Interpolação pelo Polinômio de Lagrange
├── interpolacao_newton.py      # Interpolação por Diferenças Divididas de Newton
├── regra_trapezios.py          # Regra dos Trapézios Repetida
├── regra_simpson.py            # 1ª Regra de Simpson (Simpson 1/3 Repetida)
└── README.md                   # Documentação detalhada do projeto
```

---

## 🔬 Detalhamento Teórico e Matemático dos Métodos

### 1) Zeros de Funções

O objetivo central é determinar raízes $\alpha$ tais que $f(\alpha) = 0$.

#### Teorema de Bolzano (Teorema do Valor Intermediário)
Seja $f: [a, b] \to \mathbb{R}$ uma função contínua. Se $f(a) \cdot f(b) < 0$, então existe pelo menos um $\alpha \in (a, b)$ tal que $f(\alpha) = 0$.

---

#### 1.1) Método da Bissecção
- **Fundamento**: Divide o intervalo $[a, b]$ ao meio sucessivamente a cada iteração.
- **Ponto Médio**:
  $$x_k = \frac{a_k + b_k}{2}$$
- **Atualização do Intervalo**:
  - Se $f(a_k) \cdot f(x_k) < 0$, a raiz está no subintervalo esquerdo: $a_{k+1} = a_k$ e $b_{k+1} = x_k$.
  - Caso contrário, a raiz está no subintervalo direito: $a_{k+1} = x_k$ e $b_{k+1} = b_k$.
- **Critério de Parada**:
  $$\frac{b_k - a_k}{2} < \varepsilon \quad \text{ou} \quad |f(x_k)| < \varepsilon$$
- **Ordem de Convergência**: Linear ($p = 1$). O número de iterações necessárias para atingir tolerância $\varepsilon$ pode ser estimado *a priori* por:
  $$k > \frac{\ln(b_0 - a_0) - \ln(\varepsilon)}{\ln(2)}$$

---

#### 1.2) Método da Falsa Posição (*Regula Falsi*)
- **Fundamento**: Em vez de adotar a média aritmética simples, interpola linearmente os pontos $(a, f(a))$ e $(b, f(b))$. A raiz da reta secante intercepta o eixo $x$ no ponto:
  $$x_k = \frac{a_k f(b_k) - b_k f(a_k)}{f(b_k) - f(a_k)}$$
- **Atualização**: Segue a mesma lógica de troca de sinal de Bolzano utilizada na Bissecção.
- **Vantagem**: Tende a convergir mais rapidamente quando a inclinação da função orienta adequadamente o ponto médio ponderado.

---

#### 1.3) Método de Newton-Raphson
- **Fundamento**: Baseado na expansão em Série de Taylor de primeira ordem em torno da aproximação atual $x_k$:
  $$f(x) \approx f(x_k) + f'(x_k)(x - x_k) = 0$$
- **Fórmula de Recorrência**:
  $$x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)}$$
- **Ordem de Convergência**: Quadrática ($p = 2$) nas vizinhanças da raiz simples, desde que $f'(x) \neq 0$ e $f''(x)$ seja contínua.
- **Cálculo da Derivada**: No projeto, a derivada é obtida simbolicamente via SymPy ou aproximada por diferenças finitas centrais de alta precisão:
  $$f'(x_k) \approx \frac{f(x_k + h) - f(x_k - h)}{2h}, \quad h = 10^{-7}$$

---

#### 1.4) Método das Secantes
- **Fundamento**: Elimina a necessidade de calcular analiticamente a derivada $f'(x_k)$, substituindo-a pelo quociente de diferenças finitas entre dois pontos sucessivos $x_{k-1}$ e $x_k$:
  $$f'(x_k) \approx \frac{f(x_k) - f(x_{k-1})}{x_k - x_{k-1}}$$
- **Fórmula de Recorrência**:
  $$x_{k+1} = \frac{x_{k-1} f(x_k) - x_k f(x_{k-1})}{f(x_k) - f(x_{k-1})}$$
- **Ordem de Convergência**: Superlinear ($p = \frac{1 + \sqrt{5}}{2} \approx 1{,}618$, proporção áurea).
- **Entrada Necessária**: Dois palpites iniciais $x_0$ e $x_1$.

---

### 2) Sistemas Lineares

Dado o sistema $A x = b$, onde $A \in \mathbb{R}^{n \times n}$ e $x, b \in \mathbb{R}^n$.

---

#### 2.1) Método de Eliminação de Gauss (com Pivoteamento Parcial)
- **Escalonamento Triangular**: Converte a matriz aumentada $[A \mid b]$ em uma matriz triangular superior equivalente $[U \mid c]$.
- **Pivoteamento Parcial**: Em cada passo $i$ ($i = 1, \dots, n-1$), busca-se na coluna $i$ o elemento com maior valor absoluto:
  $$|A_{k, i}| = \max_{j=i}^n |A_{j, i}|$$
  Se $k \neq i$, permutam-se as linhas $i$ e $k$ para minimizar erros de arredondamento.
- **Multiplicadores de Eliminação**:
  $$m_{ji} = \frac{A_{ji}}{A_{ii}}, \quad j = i+1, \dots, n$$
  Operação na linha: $L_j \leftarrow L_j - m_{ji} L_i$.
- **Substituição Regressiva**:
  $$x_n = \frac{b_n}{A_{nn}}, \qquad x_i = \frac{b_i - \sum_{j=i+1}^n A_{ij} x_j}{A_{ii}}, \quad i = n-1, \dots, 1$$

---

#### 2.2) Fatoração LU (Decomposição de Doolittle)
- **Decomposição**: Fatora $A$ no produto $A = L \cdot U$, onde:
  - $L$ é triangular inferior com 1s na diagonal principal ($L_{ii} = 1$ e $L_{ij} = m_{ij}$ para $i > j$).
  - $U$ é a matriz triangular superior resultante da eliminação.
- **Resolução do Sistema em Dois Passos Triangulares**:
  1. **Substituição Progressiva**: Resolve $L \cdot y = b$:
     $$y_1 = b_1, \qquad y_i = b_i - \sum_{j=1}^{i-1} L_{ij} y_j, \quad i = 2, \dots, n$$
  2. **Substituição Regressiva**: Resolve $U \cdot x = y$:
     $$x_n = \frac{y_n}{U_{nn}}, \qquad x_i = \frac{y_i - \sum_{j=i+1}^n U_{ij} x_j}{U_{ii}}, \quad i = n-1, \dots, 1$$

---

#### 2.3) Método Iterativo de Gauss-Jacobi
- **Isolamento de Variáveis**: Isola-se a incógnita $x_i$ da $i$-ésima equação:
  $$x_i^{(k+1)} = \frac{1}{A_{ii}} \left( b_i - \sum_{j \neq i} A_{ij} x_j^{(k)} \right)$$
- **Critério das Linhas (Convergência Garantida)**:
  Uma matriz $A$ é estritamente diagonal dominante por linhas se:
  $$\alpha_i = \frac{\sum_{j \neq i} |A_{ij}|}{|A_{ii}|} < 1, \quad \forall i \in \{1, \dots, n\}$$
  Se $\max_{i} \alpha_i < 1$, o método de Gauss-Jacobi converge para qualquer chute inicial $x^{(0)}$.
- **Critério de Parada**:
  $$\frac{\|x^{(k+1)} - x^{(k)}\|_\infty}{\|x^{(k+1)}\|_\infty} < \varepsilon$$

---

#### 2.4) Método Iterativo de Gauss-Seidel
- **Atualização Imediata**: Utiliza os valores $x_j^{(k+1)}$ já computados na iteração corrente:
  $$x_i^{(k+1)} = \frac{1}{A_{ii}} \left( b_i - \sum_{j < i} A_{ij} x_j^{(k+1)} - \sum_{j > i} A_{ij} x_j^{(k)} \right)$$
- **Critério de Sassenfeld (Condição Suficiente de Convergência)**:
  Calculam-se os coeficientes $\beta_i$:
  $$\beta_1 = \frac{\sum_{j=2}^n |A_{1j}|}{|A_{11}|}, \qquad \beta_i = \frac{\sum_{j=1}^{i-1} |A_{ij}| \beta_j + \sum_{j=i+1}^n |A_{ij}|}{|A_{ii}|}, \quad i = 2, \dots, n$$
  Se $\max_{i} \beta_i < 1$, o método de Gauss-Seidel converge independentemente do vetor inicial $x^{(0)}$.

---

### 3) Ajuste de Curvas (Mínimos Quadrados Polinomial)

Dado um conjunto de $n$ observações amostrais $\{(x_k, y_k)\}_{k=1}^n$, busca-se um polinômio de grau $m < n$:
$$P_m(x) = c_0 + c_1 x + c_2 x^2 + \dots + c_m x^m$$
que minimize a soma dos quadrados dos resíduos:
$$S(c_0, c_1, \dots, c_m) = \sum_{k=1}^n \left( y_k - P_m(x_k) \right)^2$$

#### Sistema de Equações Normais
Ao impor $\frac{\partial S}{\partial c_i} = 0$ para todo $i = 0, \dots, m$, obtém-se o sistema linear simétrico $M \cdot c = B$:

$$\begin{bmatrix}
n & \sum x_k & \sum x_k^2 & \dots & \sum x_k^m \\
\sum x_k & \sum x_k^2 & \sum x_k^3 & \dots & \sum x_k^{m+1} \\
\sum x_k^2 & \sum x_k^3 & \sum x_k^4 & \dots & \sum x_k^{m+2} \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
\sum x_k^m & \sum x_k^{m+1} & \sum x_k^{m+2} & \dots & \sum x_k^{2m}
\end{bmatrix}
\begin{bmatrix} c_0 \\ c_1 \\ c_2 \\ \vdots \\ c_m \end{bmatrix}
=
\begin{bmatrix} \sum y_k \\ \sum x_k y_k \\ \sum x_k^2 y_k \\ \vdots \\ \sum x_k^m y_k \end{bmatrix}$$

#### Métricas Estatísticas
- **Soma Quadrática dos Erros (SQE)**:
  $$\text{SQE} = \sum_{k=1}^n (y_k - P(x_k))^2$$
- **Soma Quadrática Total (SQT)**:
  $$\text{SQT} = \sum_{k=1}^n (y_k - \bar{y})^2, \quad \bar{y} = \frac{1}{n} \sum_{k=1}^n y_k$$
- **Coeficiente de Determinação ($R^2$)**:
  $$R^2 = 1 - \frac{\text{SQE}}{\text{SQT}}$$
  Quanto mais próximo de 1, melhor o polinômio explica a variância dos dados.

---

### 4) Interpolação Polinomial

Dados $n+1$ pontos distintos $(x_0, y_0), (x_1, y_1), \dots, (x_n, y_n)$.
O **Teorema de Existência e Unicidade** garante que existe um único polinômio $P_n(x)$ de grau no máximo $n$ tal que $P_n(x_i) = y_i$ para todo $i = 0, \dots, n$.

---

#### 4.1) Pela Definição (Sistema Linear de Vandermonde)
- **Forma Canônica**:
  $$P_n(x) = a_0 + a_1 x + a_2 x^2 + \dots + a_n x^n$$
- **Sistema Linear**:
  $$\begin{bmatrix}
  1 & x_0 & x_0^2 & \dots & x_0^n \\
  1 & x_1 & x_1^2 & \dots & x_1^n \\
  \vdots & \vdots & \vdots & \ddots & \vdots \\
  1 & x_n & x_n^2 & \dots & x_n^n
  \end{bmatrix}
  \begin{bmatrix} a_0 \\ a_1 \\ \vdots \\ a_n \end{bmatrix}
  =
  \begin{bmatrix} y_0 \\ y_1 \\ \vdots \\ y_n \end{bmatrix}$$
- O determinante da matriz de Vandermonde é $\prod_{0 \le j < i \le n} (x_i - x_j) \neq 0$ se todos os nós $x_i$ forem distintos, garantindo solução única.

---

#### 4.2) Polinômio de Lagrange
- **Construção**:
  $$P_n(x) = \sum_{i=0}^n y_i L_i(x)$$
- **Polinômios Base de Lagrange**:
  $$L_i(x) = \prod_{\substack{j=0 \\ j \neq i}}^n \frac{x - x_j}{x_i - x_j}$$
- **Propriedade Fundamental**:
  $$L_i(x_j) = \delta_{ij} = \begin{cases} 1, & \text{se } i = j \\ 0, & \text{se } i \neq j \end{cases}$$
- Evita a resolução explícita de sistemas lineares.

---

#### 4.3) Polinômio de Newton (Diferenças Divididas)
- **Forma de Newton**:
  $$P_n(x) = f[x_0] + f[x_0, x_1](x - x_0) + f[x_0, x_1, x_2](x - x_0)(x - x_1) + \dots + f[x_0, \dots, x_n]\prod_{j=0}^{n-1}(x - x_j)$$
- **Definição Recursiva das Diferenças Divididas**:
  $$f[x_i] = y_i, \qquad f[x_i, \dots, x_{i+k}] = \frac{f[x_{i+1}, \dots, x_{i+k}] - f[x_i, \dots, x_{i+k-1}]}{x_{i+k} - x_i}$$
- **Vantagem**: Adicionar um novo ponto $(x_{n+1}, y_{n+1})$ requer apenas calcular uma linha a mais na tabela triangular de diferenças, sem recalcular todo o polinômio.

---

### 5) Integração Numérica (Fórmulas de Newton-Cotes Fechadas)

Aproxima a integral definida $I = \int_a^b f(x) \, dx$ dividindo o intervalo $[a, b]$ em $n$ subintervalos regulares de largura $h = \frac{b - a}{n}$, com nós $x_i = a + i \cdot h$.

---

#### 5.1) Regra dos Trapézios Repetida
- **Fundamento**: Em cada subintervalo $[x_i, x_{i+1}]$, aproxima-se $f(x)$ por uma reta que une $(x_i, f(x_i))$ a $(x_{i+1}, f(x_{i+1}))$.
- **Fórmula Composta**:
  $$I_T = \frac{h}{2} \left[ f(x_0) + 2 \sum_{i=1}^{n-1} f(x_i) + f(x_n) \right]$$
- **Erro de Truncamento Global**:
  $$E_T = -\frac{(b - a) h^2}{12} f''(\xi), \quad \xi \in (a, b) \quad \implies O(h^2)$$

---

#### 5.2) 1ª Regra de Simpson (Simpson 1/3 Repetida)
- **Fundamento**: Em cada par de subintervalos $[x_{2k}, x_{2k+2}]$, interpola-se uma parábola passando por 3 pontos: $x_{2k}, x_{2k+1}, x_{2k+2}$. Logo, **o número de subintervalos $n$ deve ser obrigatoriamente par**.
- **Fórmula Composta**:
  $$I_S = \frac{h}{3} \left[ f(x_0) + 4 \sum_{\substack{i=1 \\ i \text{ ímpar}}}^{n-1} f(x_i) + 2 \sum_{\substack{i=2 \\ i \text{ par}}}^{n-2} f(x_i) + f(x_n) \right]$$
- **Pesos dos Nós**: $1, 4, 2, 4, 2, \dots, 2, 4, 1$.
- **Erro de Truncamento Global**:
  $$E_S = -\frac{(b - a) h^4}{180} f^{(4)}(\eta), \quad \eta \in (a, b) \quad \implies O(h^4)$$
  Integra exatamente polinômios de até grau 3, apesar de ser baseado em parábolas (grau 2).

---

## 💻 Guia dos Módulos e Algoritmos

Cada módulo foi concebido para expor tanto uma função de uso direto quanto uma função detalhada utilizada pelo visualizador gráfico:

### [sanitizador.py](file:///Users/mateusquadros/Desktop/Aulas/Metodos/sanitizador.py)
- `sanitiza_expressao(s)` e `processa_expressao_natural(texto)`: Converte expressões matemáticas escritas na forma natural humana (como `xˆ3-9xˆ2+3`, `9x`, `sen(x)`, `e^-x`, `2,5x`) em expressões canônicas executáveis pelo Python e SymPy, fornecendo também a formatação direta em LaTeX.

### [bissecao.py](file:///Users/mateusquadros/Desktop/Aulas/Metodos/bissecao.py)
- `bissecao(expr, a, b, tol, max_iter=100)`: Retorna `(raiz, historico)` contendo as iterações, valores de $a$, $b$, ponto médio $x$, $f(x)$ e estimativa do erro $(b-a)/2$.

### [falsa_posicao.py](file:///Users/mateusquadros/Desktop/Aulas/Metodos/falsa_posicao.py)
- `falsa_posicao(expr, a, b, tol, max_iter=100)`: Registra os extremos $[a, b]$, valores funcionais, a interseção da reta secante e o erro estimado.

### [newton.py](file:///Users/mateusquadros/Desktop/Aulas/Metodos/newton.py)
- `newton(expr, chute, tol, max_iter=100)`: Calcula $x_{k+1}$ e a derivada $f'(x_k)$ em cada passo, registrando os pontos necessários para desenhar a reta tangente.

### [secantes.py](file:///Users/mateusquadros/Desktop/Aulas/Metodos/secantes.py)
- `secantes(expr, x0, x1, tol, max_iter=100)`: Registra o histórico de pares $(x_{k-1}, x_k)$, valores da função e o próximo valor estimado $x_{k+1}$.

### [eliminacao_gauss.py](file:///Users/mateusquadros/Desktop/Aulas/Metodos/eliminacao_gauss.py)
- `eliminacao_gauss_detalhada(A, b)`: Retorna o vetor solução e uma lista detalhada de cada etapa do escalonamento com pivoteamento parcial, incluindo a matriz aumentada e os multiplicadores $m_{ji}$.

### [fatoracao_lu.py](file:///Users/mateusquadros/Desktop/Aulas/Metodos/fatoracao_lu.py)
- `fatoracao_lu_detalhada(A, b)`: Retorna `(x, L, U, y)` onde $L$ e $U$ são as matrizes da decomposição, $y$ é o vetor intermediário da substituição progressiva ($Ly = b$) e $x$ é a solução final ($Ux = y$).

### [gauss_jacobi.py](file:///Users/mateusquadros/Desktop/Aulas/Metodos/gauss_jacobi.py)
- `criterio_linhas(A)`: Testa se $\max_i \alpha_i < 1$ e calcula os coeficientes $\alpha_i$ por linha.
- `gauss_jacobi_detalhado(A, b, x0, tol, max_iter)`: Retorna a solução, se convergiu, e a tabela de iterações com o erro estimado a cada iteração.

### [gauss_seidel.py](file:///Users/mateusquadros/Desktop/Aulas/Metodos/gauss_seidel.py)
- `criterio_sassenfeld(A)`: Calcula os coeficientes $\beta_i$ e verifica se $\max_i \beta_i < 1$.
- `gauss_seidel_detalhado(A, b, x0, tol, max_iter)`: Executa as iterações com atualização imediata e calcula os erros relativos.

### [ajuste_polinomial.py](file:///Users/mateusquadros/Desktop/Aulas/Metodos/ajuste_polinomial.py)
- `ajuste_polinomial_detalhado(x, y, grau)`: Monta o sistema normal, resolve por Eliminação de Gauss, calcula os coeficientes, o coeficiente $R^2$, a soma quadrática dos resíduos (SQE) e gera a tabela completa de resíduos $e_i = y_i - P(x_i)$.

### [interpolacao_definicao.py](file:///Users/mateusquadros/Desktop/Aulas/Metodos/interpolacao_definicao.py)
- `interpolacao_definicao_detalhada(x_pts, y_pts, x_eval)`: Constrói a Matriz de Vandermonde $V_{ij} = x_i^j$, resolve $V \cdot a = y$ e avalia $P(x^*)$.

### [interpolacao_lagrange.py](file:///Users/mateusquadros/Desktop/Aulas/Metodos/interpolacao_lagrange.py)
- `interpolacao_lagrange_detalhada(x_pts, y_pts, x_eval)`: Constrói simbolicamente cada $L_i(x)$, avalia $L_i(x^*)$ e gera o polinômio simplificado expandido.

### [interpolacao_newton.py](file:///Users/mateusquadros/Desktop/Aulas/Metodos/interpolacao_newton.py)
- `tabela_completa_diferencas(x_pts, y_pts)`: Constrói a matriz triangular com todas as ordens de diferenças divididas.
- `interpolacao_newton_detalhada(x_pts, y_pts, x_eval)`: Gera a expressão expandida e o valor interpolado.

### [regra_trapezios.py](file:///Users/mateusquadros/Desktop/Aulas/Metodos/regra_trapezios.py)
- `regra_trapezios_detalhada(expr, a, b, n)`: Computa a integral aproximada, os nós $x_i$, os pesos $c_i$, a tabela de soma e os vértices de cada trapézio individual para visualização gráfica.

### [regra_simpson.py](file:///Users/mateusquadros/Desktop/Aulas/Metodos/regra_simpson.py)
- `regra_simpson_detalhada(expr, a, b, n)`: Valida paridade de $n$, aplica os pesos $1, 4, 2, 4, \dots, 1$, calcula a integral e gera os arcos de parábola de 3 pontos para renderização no gráfico.

---

## 🎨 Recursos Visuais e Didáticos do App

A interface em [app.py](file:///Users/mateusquadros/Desktop/Aulas/Metodos/app.py) conta com:

1. **Slider de Passo a Passo**: Controle deslizante que permite viajar no tempo da execução do algoritmo, inspecionando cada iteração e o estado das variáveis.
2. **Retas Tangentes e Secantes Dinâmicas**:
   - Em **Newton-Raphson**, traça a reta tangente real no ponto $(x_k, f(x_k))$ descendo até o eixo $x$ em $x_{k+1}$.
   - Em **Secantes**, desenha a reta secante passando por $(x_{k-1}, f(x_{k-1}))$ e $(x_k, f(x_k))$.
   - Em **Falsa Posição**, traça a corda entre os extremos $[a, f(a)]$ e $[b, f(b)]$.
3. **Escalonamento de Matrizes Passo a Passo**: Visualização em tabelas formatadas de cada etapa da Eliminação de Gauss com destaque para os multiplicadores e pivôs.
4. **Gráficos de Convergência Logarítmica**: Curva de decaimento do erro em escala logarítmica para os métodos iterativos de Gauss-Jacobi e Gauss-Seidel.
5. **Geometria dos Métodos de Integração**:
   - Desenho de **cada trapézio individual sombreado** sob a curva.
   - Desenho dos **arcos parabólicos contínuos** da Regra de Simpson.
   - Cálculo analítico via SymPy com apresentação do **Erro Absoluto** real da aproximação.
6. **Comparador de Métodos**:
   - Comparação direta entre **Definição, Lagrange e Newton** demonstrando a unicidade do polinômio.
   - Comparação de convergência $O(h^2)$ vs. $O(h^4)$ entre **Trapézios e Simpson**.

---

## 🚀 Instalação e Execução

### Pré-requisitos
- Python 3.9 ou superior

### Dependências
Instale as bibliotecas necessárias via pip:

```bash
pip install streamlit numpy pandas plotly sympy
```

### Inicialização do Visualizador
No diretório do projeto, execute:

```bash
streamlit run app.py
```

O navegador abrirá automaticamente no endereço local padrão:
`http://localhost:8501`

