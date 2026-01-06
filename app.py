import streamlit as st
import sympy as sp

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Solucionador de EDO 2do Orden", page_icon="📝", layout="centered")

# --- TÍTULO Y CONTEXTO ---
st.title("Ecuación Diferencial Lineal de Orden 2")
st.markdown("""
Esta herramienta resuelve ecuaciones de la forma:  
$$a y'' + b y' + c y = 0$$
Mostrando el paso a paso del **Conjunto Fundamental de Soluciones**.
""")

# --- 1. ENTRADA DE DATOS EN EL LATERAL ---
with st.sidebar:
    st.header("Coeficientes")
    a_in = st.text_input("Coeficiente a (y'')", value="1")
    b_in = st.text_input("Coeficiente b (y')", value="-4")
    c_in = st.text_input("Coeficiente c (y)", value="4")
    resolver = st.button("Resolver Paso a Paso", type="primary")

if resolver:
    try:
        # Convertir entradas a símbolos de Sympy
        a = sp.S(a_in)
        b = sp.S(b_in)
        c = sp.S(c_in)
        x = sp.symbols('x')

        if a == 0:
            st.error("Si a=0, la ecuación no es de segundo orden.")
            st.stop()

        # --- PASO 1: ECUACIÓN CARACTERÍSTICA ---
        st.subheader("1. Ecuación Característica")
        m = sp.symbols('m')
        eq_carac = a*m**2 + b*m + c
        st.write("Sustituimos la propuesta $y = e^{mx}$ para obtener:")
        st.latex(f"{sp.latex(eq_carac)} = 0")

        # --- PASO 2: DISCRIMINANTE Y RAÍCES ---
        st.subheader("2. Cálculo de Raíces")
        disc = b**2 - 4*a*c
        st.write(f"Discriminante: $\\Delta = {sp.latex(b)}^2 - 4({sp.latex(a)})({sp.latex(c)}) = {sp.latex(disc)}$")
        
        roots = sp.solve(eq_carac, m)
        
        # --- PASO 3: DETERMINACIÓN DE y1 y y2 ---
        st.subheader("3. Conjunto Fundamental de Soluciones")
        
        y1, y2 = None, None
        tipo_caso = ""

        # CASO 1: Reales Distintas
        if disc > 0:
            r1, r2 = roots[0], roots[1]
            tipo_caso = "Raíces reales y distintas"
            y1 = sp.exp(r1 * x)
            y2 = sp.exp(r2 * x)
            st.write(f"Como $\\Delta > 0$, tenemos dos raíces reales: $r_1 = {sp.latex(r1)}$ y $r_2 = {sp.latex(r2)}$")

        # CASO 2: Reales Repetidas
        elif disc == 0:
            r = roots[0]
            tipo_caso = "Raíces reales repetidas"
            y1 = sp.exp(r * x)
            y2 = x * sp.exp(r * x)
            st.write(f"Como $\\Delta = 0$, hay una raíz repetida: $r = {sp.latex(r)}$")
            st.write("Para que las soluciones sean linealmente independientes, multiplicamos la segunda por $x$.")

        # CASO 3: Complejas
        else:
            alpha = sp.re(roots[0])
            beta = sp.Abs(sp.im(roots[0]))
            tipo_caso = "Raíces complejas conjugadas"
            y1 = sp.exp(alpha * x) * sp.cos(beta * x)
            y2 = sp.exp(alpha * x) * sp.sin(beta * x)
            st.write(f"Como $\\Delta < 0$, las raíces son complejas: $r = {sp.latex(alpha)} \\pm {sp.latex(beta)}i$")

        # Mostrar y1 y y2 claramente
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**$y_1(x) = {sp.latex(y1)}$**")
        with col2:
            st.info(f"**$y_2(x) = {sp.latex(y2)}$**")

        # --- PASO 4: SOLUCIÓN GENERAL ---
        st.subheader("4. Solución General")
        st.write(f"Basado en el caso de **{tipo_caso}**, la solución es la combinación lineal $y(x) = C_1 y_1 + C_2 y_2$:")
        
        sol_gen = sp.symbols('C1')*y1 + sp.symbols('C2')*y2
        st.success(f"### $y(x) = {sp.latex(sol_gen)}$")

    except Exception as e:
        st.error(f"Error en el proceso: {e}")

# --- SECCIÓN DEL AUTOR ---
st.markdown("---")
st.markdown("**Autor:** Elka Natalia Magaña Fierro")
