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