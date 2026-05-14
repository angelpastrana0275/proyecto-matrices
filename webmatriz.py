
import streamlit as st
import numpy as np
# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Calculadora de Matrices Pro", 
    page_icon="🧮", 
    layout="wide"
)
 
# --- ESTILOS PERSONALIZADOS (Opcional para que se vea mejor) ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES DE LÓGICA MATEMÁTICA ---
def mostrar_matriz_estetica(M, titulo):
    st.write(f"**{titulo}**")
    st.dataframe(np.array(M))

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

# --- CUERPO PRINCIPAL ---
st.title("🧮 Calculadora de Matrices Universitaria")
st.info("Ingresa los valores de tus matrices abajo y presiona el botón para calcular.")

# --- SECCIÓN DE ENTRADA DE DATOS ---
col_mat_a, col_mat_b = st.columns(2)

with col_mat_a:
    st.subheader("Matriz A")
    A = []
    for i in range(f1):
        cols = st.columns(c1)
        fila = []
        for j in range(c1):
            with cols[j]:
                val = st.number_input(f"A[{i+1},{j+1}]", value=0.0, key=f"A_{i}_{j}")
                fila.append(val)
        A.append(fila)

B = None
# Operaciones que requieren una segunda matriz B
if opcion in ["Suma (A + B)", "Resta (A - B)", "Multiplicación (A x B)"]:
    with col_mat_b:
        st.subheader("Matriz B")
        # Ajuste de dimensiones para B
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
                    val = st.number_input(f"B[{i+1},{j+1}]", value=0.0, key=f"B_{i}_{j}")
                    fila.append(val)
            B.append(fila)

# --- ENTRADA PARA ESCALAR O VECTOR ---
escalar = 1.0
vector = []
if opcion == "Matriz x Escalar":
    escalar = st.sidebar.number_input("Introduce el Escalar:", value=1.0)
elif opcion == "Matriz x Vector":
    st.sidebar.subheader("Vector v")
    for i in range(c1):
        vector.append(st.sidebar.number_input(f"v[{i+1}]", value=0.0, key=f"v_{i}"))

# --- BOTÓN Y LÓGICA DE CÁLCULO ---
st.write("---")
if st.button("🚀 REALIZAR OPERACIÓN"):
    try:
        mat_a = np.array(A)
        
        if opcion == "Suma (A + B)":
            res = mat_a + np.array(B)
            mostrar_matriz_estetica(res, "Resultado de la Suma:")
            
        elif opcion == "Resta (A - B)":
            res = mat_a - np.array(B)
            mostrar_matriz_estetica(res, "Resultado de la Resta:")
            
        elif opcion == "Multiplicación (A x B)":
            res = np.dot(mat_a, np.array(B))
            mostrar_matriz_estetica(res, "Resultado de A x B:")
            
        elif opcion == "Transpuesta (Aᵀ)":
            res = mat_a.T
            mostrar_matriz_estetica(res, "Matriz A Transpuesta:")
            
        elif opcion == "Matriz x Vector":
            res = np.dot(mat_a, np.array(vector))
            st.write("**Resultado de A x v:**")
            st.write(res)
            
        elif opcion == "Matriz x Escalar":
            res = mat_a * escalar
            mostrar_matriz_estetica(res, f"Resultado de A * {escalar}:")
            
        elif opcion == "Inversa (A⁻¹)":
            if f1 == c1:
                res = np.linalg.inv(mat_a)
                mostrar_matriz_estetica(res, "Matriz Inversa:")
            else:
                st.error("❌ Solo las matrices cuadradas tienen inversa.")
                
    except Exception as e:
        st.error(f"❌ Error en el cálculo: {e}")
