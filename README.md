# 🚀 Calculadora e Visualizador de Métodos Numéricos

Seja bem-vindo ao projeto! Se você caiu aqui de paraquedas e precisa entender como essa bagaça funciona sem ter que ler um livro de cálculo de 800 páginas, relaxa que o resumo tá logo abaixo.

---

## 🛠️ Como essa engrenagem roda? (A Estrutura dos Arquivos)

O projeto foi dividido em pequenas caixas de ferramentas para o código não virar uma bagunça impossível de mexer:

1. **`app.py`**: É o "cérebro visual" da parada. Ele desenha os botões, os gráficos, as tabelas e conversa com você usando o Streamlit.
2. **`style.css`**: Deixa a interface bonita (porque ninguém merece usar software com cara de Windows 95).
3. **`sanitizador.py`**: É o faxineiro. Se você digitar uma função maluca tipo `xˆ3` ou `2,5x`, ele limpa e traduz para o Python e para o LaTeX entenderem.
4. **Os arquivos de métodos (`bissecao.py`, `newton.py`, `eliminacao_gauss.py`, etc.)**: Cada um guarda a matemática pura de um método específico. Eles recebem os dados, fazem as contas no talo e devolvem a resposta mastigada para o `app.py` desenhar a animação.

---

## 🧠 Explicando os Métodos (Como se você fosse uma mula 🐴)

### 1. Zeros de Funções (Achar onde $f(x) = 0$)
* **Bissecção:** Você chuta um intervalo onde a função muda de sinal (um lado é positivo, o outro é negativo). O computador corta o intervalo **exatamente no meio** repetidas vezes até cercar a raiz. É lento, mas é impossível de dar errado se o intervalo estiver certo.
* **Falsa Posição:** Parecido com a Bissecção, mas em vez de cortar no meio burramente, ele passa uma régua (linha secante) entre os pontos e adivinha onde a raiz está mais perto.
* **Newton-Raphson:** Ele usa a derivada da função (a inclinação da reta tangente) para dar um "tiro certeiro" na raiz. Converge absurdamente rápido, mas se você der um chute inicial muito ruim, ele voa para o espaço e explode.
* **Secantes:** Faz a mesma coisa que o Newton, mas sem precisar calcular a derivada analítica (ele aproxima a inclinação usando dois pontos anteriores).

### 2. Sistemas Lineares ($A \cdot x = b$)
* **Eliminação de Gauss:** Lembra do colégio? Você pega a matriz, zera a galera de baixo escalonando a parada e depois faz a conta de trás para frente para achar as incógnitas ($x_1, x_2$, etc.). O projeto usa **pivoteamento parcial** para o computador não dividir por zero e não arredondar errado.
* **Fatoração LU:** Quebra a matriz $A$ em duas outras matrizes mais fáceis de mexer ($L$ e $U$). Depois resolve o sistema em duas etapas rápidas.
* **Gauss-Jacobi e Gauss-Seidel:** São métodos de chute iterativo. Você isola as variáveis e vai atualizando os valores até os erros ficarem pequenininhos. **Aviso:** Se a matriz não tiver uma "diagonal forte" (diagonal dominante), esses métodos vão divergir e explodir para o infinito (`NaN`).

### 3. Ajuste de Curvas (Mínimos Quadrados)
* Você joga um monte de pontinhos espalhados no gráfico e pede para o computador achar uma linha ou parábola que passe "no meio de todo mundo" da forma mais justa possível, minimizando o erro quadrado dos resíduos. O $R^2$ te diz se a curva ficou boa ou se foi um chute aleatório.

### 4. Interpolação Polinomial
* Você tem $n$ pontos e quer criar um polinômio que cruze **obrigatoriamente** por cima de todos eles. 
* **Vandermonde:** Joga tudo em um pratão de sistema linear gigante.
* **Lagrange:** Soma vários mini-polinômios base.
* **Newton:** Usa uma tabela de diferenças divididas que é ótima porque, se você adicionar um ponto novo depois, não precisa refazer a conta inteira do zero.
* *(Dica: Pelo Teorema da Unicidade, os três métodos dão exatamente o **mesmo** polinômio no final!)*

### 5. Integração Numérica (Calcular a Área Abaixo da Curva)
* **Regra dos Trapézios:** Pega a área embaixo do gráfico e fatia em vários trapézios. Quanto mais fatias ($n$), mais preciso fica.
* **1ª Regra de Simpson:** Fatia a área usando arcos de parábola em vez de retas (exige número de fatias $n$ par). É muito mais precisa que os trapézios.

---

## 🔍 Como cada código funciona por dentro (Por trás dos panos)

### 🛠️ O Faxineiro de Dados

* **`sanitizador.py`**:
  * **O que faz:** Transforma o que o usuário digita na tela (ex: `xˆ3`, `9x`, `2,5x`) em código que o Python e o LaTeX entendem.
  * **Como funciona:** Usa a biblioteca de expressões regulares (`re`) para trocar `,` por `.`, e atalhos humanos (`sen`, `tg`, `ln`, `raiz`) por funções do Python (`sin`, `tan`, `log`, `sqrt`). Depois, roda o `parse_expr` do `sympy` com regras de multiplicação implícita para transformar `9x` em `9*x` sem quebrar a execução.

---

### 🎯 1. Zeros de Funções

* **`bissecao.py`**:
  * **Como chega no resultado:** Avalia $f(a)$ e $f(b)$ usando a função de avaliação segura (`eval`). Se $f(a) \cdot f(b) > 0$, ele aborta porque não cumpre o Teorema de Bolzano. No loop `for`, calcula o ponto médio $m = (a+b)/2$, descobre de qual lado o sinal muda e atualiza $a$ ou $b$. A cada passo, salva os valores em um dicionário dentro do histórico para alimentar o gráfico no Streamlit.
* **`falsa_posicao.py`**:
  * **Como chega no resultado:** Segue a mesma estrutura de histórico e validação da Bissecção, mas troca a fórmula do ponto médio pela fórmula da reta secante: `ponto = (a * fb - b * fa) / (fb - fa)`. O resto da lógica de substituição dos limites do intervalo permanece idêntico.
* **`newton.py`**:
  * **Como chega no resultado:** Usa uma função auxiliar de derivada que tenta usar a derivada simbólica do `sympy` (`diff`). Se falhar, calcula via diferença finita central `(f(x+h) - f(x-h))/(2h)`. No loop, calcula $x_{novo} = x_{atual} - f(x)/f'(x)$. Se $f'(x) \approx 0$, o código interrompe a execução para evitar a divisão por zero.
* **`secantes.py`**:
  * **Como chega no resultado:** Recebe dois pontos iniciais ($x_0, x_1$). A cada passo do loop, calcula a inclinação da reta secante usando o quociente de diferenças entre os dois últimos pontos (`den = f_curr - f_prev`) e encontra o próximo chute sem precisar derivar a função.

---

### 🔢 2. Sistemas Lineares

* **`eliminacao_gauss.py`**:
  * **Como chega no resultado:** Executa um loop por colunas. Em cada coluna, busca a linha com o maior valor absoluto para realizar o **pivoteamento parcial** (troca de linhas para evitar divisão por zero). Depois, calcula o multiplicador e zera os elementos abaixo do pivô. No final, roda um loop de trás para frente (substituição regressiva) para isolar e calcular cada variável.
* **`fatoracao_lu.py`**:
  * **Como chega no resultado:** Inicializa a matriz $L$ como identidade e a matriz $U$ como uma cópia de $A$. Durante o escalonamento, guarda os multiplicadores dentro da matriz $L$. Para resolver o sistema $A x = b$, executa duas etapas simples: primeiro resolve $L y = b$ de cima para baixo (substituição progressiva) e em seguida $U x = y$ de baixo para cima.
* **`gauss_jacobi.py`**:
  * **Como chega no resultado:** Recebe um vetor de chute inicial. Em cada iteração $k$, calcula todas as variáveis do vetor novo `x_novo` utilizando **exclusivamente** os valores das variáveis salvas no vetor antigo `x` da iteração anterior. No final de cada ciclo, calcula o erro relativo máximo e substitui o vetor antigo pelo novo.
* **`gauss_seidel.py`**:
  * **Como chega no resultado:** Funciona de forma similar ao Jacobi, mas não utiliza um vetor novo separado. Ele atualiza os valores diretamente na mesma lista em tempo real. Assim, quando o algoritmo vai calcular $x_2$, ele já utiliza o valor de $x_1$ recém-calculado na própria iteração corrente, acelerando a convergência.

---

### 📈 3. Ajuste de Curvas

* **`ajuste_polinomial.py`**:
  * **Como chega no resultado:** Para ajustar um polinômio de grau $m$, calcula os somatórios das potências de $x$ ($\sum x^0, \sum x^1 \dots$) para preencher a matriz das Equações Normais $A$ e o vetor $B$. Resolve esse sistema linear com a Eliminação de Gauss para obter os coeficientes. Em seguida, calcula a Soma Quadrática dos Resíduos (SQE) e entrega o coeficiente de determinação $R^2 = 1 - (SQE / SQT)$.

---

### 🔀 4. Interpolação Polinomial

* **`interpolacao_definicao.py` (Vandermonde)**:
  * **Como chega no resultado:** Constrói uma matriz quadrada $V$ onde cada coluna $j$ da linha $i$ contém $x_i^j$. Em seguida, resolve o sistema linear $V \cdot a = y$. O vetor resultante $a$ contém os coeficientes exatos da forma canônica do polinômio.
* **`interpolacao_lagrange.py`**:
  * **Como chega no resultado:** Usa o `sympy` para construir expressões simbólicas. Para cada ponto $i$, roda um loop para calcular o polinômio base $L_i(x) = \prod \frac{x - x_j}{x_i - x_j}$. Multiplica cada $L_i(x)$ por seu respetivo $y_i$, soma todos e roda a função `expand()` para retornar a expressão simplificada do polinômio final.
* **`interpolacao_newton.py`**:
  * **Como chega no resultado:** Monta uma matriz triangular contendo a tabela de diferenças divididas de todas as ordens. Extrai os elementos da primeira linha da tabela (que são os coeficientes de Newton) e constrói o polinômio na forma produtória $P(x) = c_0 + c_1(x-x_0) + c_2(x-x_0)(x-x_1) \dots$.

---

### 📐 5. Integração Numérica

* **`regra_trapezios.py`**:
  * **Como chega no resultado:** Divide o intervalo $[a, b]$ em $n$ pedaços de tamanho $h = (b-a)/n$. Avalia os pontos e atribui peso 1 para o primeiro e último ponto ($x_0, x_n$) e peso 2 para todos os pontos intermediários. Soma todos os valores ponderados e multiplica o resultado por $h / 2$. Retorna também a geometria de cada trapézio para plotar o gráfico.
* **`regra_simpson.py` (1ª Regra de Simpson - 1/3)**:
  * **Como chega no resultado:** Valida se o número de subintervalos $n$ é par. Atribui pesos no padrão $1, 4, 2, 4, 2 \dots 4, 1$ (sendo 4 para os nós de índice ímpar e 2 para os nós de índice par). Soma esses termos e multiplica por $h / 3$. Para o gráfico visual, calcula a interpolação parabólica de 3 em 3 pontos.

---

## 💻 Como Rodar essa joça no seu PC

### 1. Pré-requisitos
Certifique-se de ter o **Python** instalado no seu computador.

### 2. Instalar as dependências
Abra o seu terminal na pasta do projeto e digite o comando abaixo para instalar as bibliotecas necessárias:

```bash
pip install streamlit numpy pandas plotly sympy
```

### 3. Iniciar o App
Com tudo instalado, rode:

```bash
streamlit run app.py
```

O navegador do seu computador vai abrir sozinho na página local (`http://localhost:8501`) rodando a aplicação bonitinha!