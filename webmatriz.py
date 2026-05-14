import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Calculadora de Matrices Pro", 
    page_icon="🧮", 
    layout="wide"
)

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    div[data-testid="column"]:nth-of-type(1) h3 { color: #28B463; }
    div[data-testid="column"]:nth-of-type(2) h3 { color: #2E86C1; }
    .resultado-header { color: #CB4335; font-size: 24px; font-weight: bold; margin-top: 20px; }
    .stButton>button { 
        width: 100%; border-radius: 8px; height: 3em; 
        background-color: #2E86C1; color: white; font-weight: bold; border: none;
    }
    .stButton>button:hover { background-color: #1B4F72; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGO Y TÍTULO ---
try:
    st.image("logo_uni.png", width=150)
except:
    st.info("💡 Tip: Sube 'logo_uni.png' a tu GitHub para ver el logo aquí.")

st.title("🧮 Calculadora de Matrices Universitaria")
st.info("Ingresa los valores abajo y presiona el botón para calcular.")

# --- INTERFAZ DE USUARIO (SIDEBAR) ---
with st.sidebar:
    st.title("⚙️ Configuración")
    opcion = st.selectbox(
        "¿Qué operación deseas realizar?",
        ["Suma (A + B)", "Resta (A - B)", "Multiplicación (A x B)", 
         "Transpuesta (Aᵀ)", "Matriz x Vector", "Matriz x Escalar", "Inversa (A⁻¹)"]
    )
    st.write("---")
    st.header("📏 Dimensiones de Matriz A")
    f1 = st.number_input("Filas A", min_value=1, max_value=5, value=3)
    c1 = st.number_input("Columnas A", min_value=1, max_value=5, value=3)

# --- SECCIÓN DE ENTRADA DE DATOS ---
col_mat_a, col_espacio = st.columns(2)

with col_mat_a:
    st.subheader("Matriz A")
    A = []
    for i in range(f1):
        cols = st.columns(c1)
        fila = []
        for j in range(c1):
            with cols[j]:
                val = st.number_input(f"A[{i+1},{j+1}]", value=0, step=1, format="%d", key=f"A_{i}_{j}")
                fila.append(val)
        A.append(fila)

# --- ENTRADA PARA SEGUNDA MATRIZ, ESCALAR O VECTOR ---
B = None
escalar = 1
vector = []

with col_espacio:
    if opcion in ["Suma (A + B)", "Resta (A - B)", "Multiplicación (A x B)"]:
        st.subheader("Matriz B")
        if opcion == "Multiplicación (A x B)":
            f2, c2 = c1, st.number_input("Columnas B", min_value=1, max_value=5, value=3)
        else:
            f2, c2 = f1, c1
            st.write(f"Dimensiones fijas: {f2}x{c2}")
        
        B = []
        for i in range(f2):
            cols = st.columns(c2)
            fila = []
            for j in range(c2):
                with cols[j]:
                    val = st.number_input(f"B[{i+1},{j+1}]", value=0, step=1, format="%d", key=f"B_{i}_{j}")
                    fila.append(val)
            B.append(fila)

    elif opcion == "Matriz x Vector":
        st.subheader("Vector v")
        st.write(f"Introduce los {c1} elementos del vector:")
        for i in range(c1):
            vector.append(st.number_input(f"v[{i+1}]", value=0, format="%d", key=f"v_{i}"))

    elif opcion == "Matriz x Escalar":
        st.subheader("Escalar")
        escalar = st.number_input("Introduce el número por el que multiplicarás la matriz:", value=1, format="%d")

# --- BOTÓN Y LÓGICA DE CÁLCULO ---
st.write("---")
if st.button("🚀 REALIZAR OPERACIÓN"):
    try:
        mat_a = np.array(A)

        # Propiedades Académicas
        with st.expander("📊 Ver Propiedades de la Matriz A"):
            pcol1, pcol2 = st.columns(2)
            with pcol1:
                if f1 == c1:
                    st.write(f"**Determinante:** {np.linalg.det(mat_a):.2f}")
                    st.write(f"**Traza:** {np.trace(mat_a)}")
                else:
                    st.write("**Determinante:** N/A")
            with pcol2:
                st.write(f"**Rango:** {np.linalg.matrix_rank(mat_a)}")
                st.write(f"**¿Es Cuadrada?:** {'Sí' if f1 == c1 else 'No'}")

        # Lógica de operaciones
        def mostrar(res, tit):
            st.markdown(f'<p class="resultado-header">{tit}</p>', unsafe_allow_html=True)
            st.dataframe(res)

        if opcion == "Suma (A + B)": mostrar(mat_a + np.array(B), "Resultado Suma:")
        elif opcion == "Resta (A - B)": mostrar(mat_a - np.array(B), "Resultado Resta:")
        elif opcion == "Multiplicación (A x B)": mostrar(np.dot(mat_a, np.array(B)), "Resultado Producto:")
        elif opcion == "Transpuesta (Aᵀ)": mostrar(mat_a.T, "Matriz A Transpuesta:")
        elif opcion == "Matriz x Vector":
            res = np.dot(mat_a, np.array(vector))
            st.markdown('<p class="resultado-header">Resultado A x v:</p>', unsafe_allow_html=True)
            st.write(res)
        elif opcion == "Matriz x Escalar": mostrar(mat_a * escalar, f"Resultado A * {escalar}:")
        elif opcion == "Inversa (A⁻¹)":
            if f1 == c1 and np.linalg.det(mat_a) != 0: mostrar(np.linalg.inv(mat_a), "Inversa:")
            else: st.error("❌ No tiene inversa.")
                
    except Exception as e:
        st.error(f"❌ Error: {e}")

# --- SECCIÓN EXTRA: JUEGO DE LA SERPIENTE (FUERA DE LA LÓGICA ANTERIOR) ---
st.write("---")
with st.expander("🎮 ¿Cansado de las matrices? ¡Modo Desafío Ajustado!"):
    st.markdown("### 🐍 Snake: Control Total")
    st.info("Velocidad inicial reducida. La dificultad aumenta cada 2 puntos.")
    
    snake_game_html = """
    <div style="text-align:center">
        <canvas id="snakeGame" width="400" height="400" style="border:3px solid #28B463; background-color: #000; outline: none; border-radius: 10px;" tabindex="1"></canvas>
    </div>
    <script>
        const canvas = document.getElementById('snakeGame');
        const ctx = canvas.getContext('2d');
        let box = 20;
        let snake, food, d, nextD, gameSpeed, gameLoop, obstacles, score;

        function resetGame() {
            snake = [{x: 10 * box, y: 10 * box}];
            d = null; 
            nextD = null;
            score = 0;
            gameSpeed = 180;
            obstacles = [];
            generateFood();
            if(gameLoop) clearTimeout(gameLoop);
            draw();
        }

        function generateFood() {
            food = {x: Math.floor(Math.random() * 19 + 1) * box, y: Math.floor(Math.random() * 19 + 1) * box};
            for(let cell of snake) { if(food.x == cell.x && food.y == cell.y) return generateFood(); }
            for(let obs of obstacles) { if(food.x == obs.x && food.y == obs.y) return generateFood(); }
        }

        function addObstacle() {
            let newObs = {x: Math.floor(Math.random() * 19 + 1) * box, y: Math.floor(Math.random() * 19 + 1) * box};
            if((newObs.x == food.x && newObs.y == food.y) || 
               snake.some(s => s.x == newObs.x && s.y == newObs.y)) {
                return addObstacle();
            }
            obstacles.push(newObs);
        }

        canvas.addEventListener('click', () => { canvas.focus(); });

        window.addEventListener('keydown', function(e) {
            if(["ArrowUp","ArrowDown","ArrowLeft","ArrowRight"].indexOf(e.code) > -1) {
                e.preventDefault();
                if(e.keyCode == 37 && d != 'RIGHT') nextD = 'LEFT';
                else if(e.keyCode == 38 && d != 'DOWN') nextD = 'UP';
                else if(e.keyCode == 39 && d != 'LEFT') nextD = 'RIGHT';
                else if(e.keyCode == 40 && d != 'UP') nextD = 'DOWN';
            }
        }, false);

        function draw() {
            ctx.fillStyle = 'black';
            ctx.fillRect(0, 0, 400, 400);
            ctx.fillStyle = '#566573';
            for(let obs of obstacles) { ctx.fillRect(obs.x, obs.y, box, box); }
            for(let i = 0; i < snake.length; i++) {
                ctx.fillStyle = (i == 0) ? '#2ecc71' : '#27ae60';
                ctx.beginPath();
                ctx.arc(snake[i].x + box/2, snake[i].y + box/2, box/2 - 1, 0, 2 * Math.PI);
                ctx.fill();
                if(i == 0) {
                    ctx.fillStyle = "white";
                    ctx.beginPath();
                    ctx.arc(snake[i].x + box/4, snake[i].y + box/4, 2, 0, 2 * Math.PI);
                    ctx.arc(snake[i].x + 3*box/4, snake[i].y + box/4, 2, 0, 2 * Math.PI);
                    ctx.fill();
                }
            }
            ctx.fillStyle = '#e74c3c';
            ctx.beginPath();
            ctx.arc(food.x + box/2, food.y + box/2, box/2 - 2, 0, 2 * Math.PI);
            ctx.fill();
            ctx.fillStyle = "white";
            ctx.font = "16px Arial";
            ctx.fillText("Puntos: " + score, 10, 20);
            if (!nextD && !d) {
                gameLoop = setTimeout(draw, gameSpeed);
                return;
            }
            d = nextD;
            let snakeX = snake[0].x;
            let snakeY = snake[0].y;
            if( d == 'LEFT') snakeX -= box;
            if( d == 'UP') snakeY -= box;
            if( d == 'RIGHT') snakeX += box;
            if( d == 'DOWN') snakeY += box;
            for(let obs of obstacles) {
                if(snakeX == obs.x && snakeY == obs.y) { resetGame(); return; }
            }
            if(snakeX == food.x && snakeY == food.y) {
                score++;
                generateFood();
                if(score >= 5) addObstacle();
                if(score % 2 == 0 && gameSpeed > 70) gameSpeed -= 10; 
            } else {
                snake.pop();
            }
            let newHead = {x: snakeX, y: snakeY};
            if(snakeX < 0 || snakeX >= 400 || snakeY < 0 || snakeY >= 400 || collision(newHead, snake)) {
                resetGame();
                return;
            }
            snake.unshift(newHead);
            gameLoop = setTimeout(draw, gameSpeed);
        }

        function collision(head, array) {
            for(let i = 0; i < array.length; i++) {
                if(head.x == array[i].x && head.y == array[i].y) return true;
            }
            return false;
        }
        resetGame();
    </script>
    """
    st.components.v1.html(snake_game_html, height=450)