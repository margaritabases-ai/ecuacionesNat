import streamlit as st
import sympy as sp

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Tutor de EDO 2do Orden", page_icon="📝")

# --- ESTILO ---
st.markdown("""
    <style>
    .teoria { background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b4b; }
    .resultado { font-size: 1.2rem; font-weight: bold; color: #1f77b4; }
    </style>
    """, unsafe_allow_html=True)

# --- TÍTULO ---
st.title("Ecuación Diferencial Lineal de Orden 2")
st.markdown("Resolución de: $a y'' + b y' + c y = 0$")

# --- ENTRADA DE DATOS ---
with st.sidebar:
    st.header("1. Ingrese Coeficientes")
    a_val = st.text_input("Coeficiente a", value="1")
    b_val = st.text_input("Coeficiente b", value="-5")
    c_val = st.text_input("Coeficiente c", value="6")
    btn = st.button("Resolver con Explicación", type="primary")

if btn:
    try:
        a = sp.S(a_val)
        b = sp.S(b_val)
        c = sp.S(c_val)
        x = sp.symbols('x')
        m = sp.symbols('m')

        if a == 0:
            st.error("Si a=0, la ecuación no es de segundo orden.")
            st.stop()

        # --- PASO 1: TEORÍA Y ECUACIÓN ---
        st.subheader("Paso 1: La Ecuación Característica")
        st.markdown("""
        <div class='teoria'>
        Para resolver esta EDO, suponemos una solución de la forma <b>y = e<sup>mx</sup></b>. 
        Al derivar e insertar en la ecuación original, obtenemos una ecuación algebraica llamada <b>Ecuación Característica</b>.
        </div>
        """, unsafe_allow_html=True)
        
        ec_carac = a*m**2 + b*m + c
        st.latex(f"{sp.latex(ec_carac)} = 0")

        # --- PASO 2: RAÍCES ---
        st.subheader("Paso 2: Cálculo de las raíces (m)")
        st.write("Usamos la fórmula cuadrática para encontrar los valores de $m$ que satisfacen la ecuación:")
        
        disc = b**2 - 4*a*c
        roots = sp.solve(ec_carac, m)
        
        st.latex(f"m = \\frac{{-{sp.latex(b)} \\pm \\sqrt{{{sp.latex(b)}^2 - 4({sp.latex(a)})({sp.latex(c)})}}}}{{2({sp.latex(a)})}}")

        # --- PASO 3: ANÁLISIS DE y1 y y2 ---
        st.subheader("Paso 3: Conjunto Fundamental de Soluciones")
        
        y1, y2 = None, None
        explicacion_caso = ""

        # CASO 1: Reales Distintas
        if disc > 0:
            r1, r2 = roots[0], roots[1]
            y1 = sp.exp(r1 * x)
            y2 = sp.exp(r2 * x)
            explicacion_caso = f"""
            Como el discriminante es <b>positivo</b> ({disc}), tenemos dos raíces reales distintas: 
            m₁ = {r1} y m₂ = {r2}. Esto genera dos soluciones linealmente independientes.
            """
            
        # CASO 2: Reales Repetidas
        elif disc == 0:
            r = roots[0]
            y1 = sp.exp(r * x)
            y2 = x * sp.exp(r * x)
            explicacion_caso = f"""
            El discriminante es <b>cero</b>. Tenemos una raíz real repetida: m = {r}. 
            Para que la segunda solución sea independiente de la primera, la teoría nos dicta multiplicar por <b>x</b>.
            """

        # CASO 3: Complejas
        else:
            alpha = sp.re(roots[0])
            beta = sp.Abs(sp.im(roots[0]))
            y1 = sp.exp(alpha * x) * sp.cos(beta * x)
            y2 = sp.exp(alpha * x) * sp.sin(beta * x)
            explicacion_caso = f"""
            El discriminante es <b>negativo</b>. Las raíces son complejas conjugadas: m = {alpha} ± {beta}i. 
            Usando la Identidad de Euler, transformamos la solución exponencial en funciones <b>Seno y Coseno</b>.
            """

        st.markdown(f"<div class='teoria'>{explicacion_caso}</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Solución y₁(x)", f"{sp.latex(y1)}")
            st.latex(f"y_1 = {sp.latex(y1)}")
        with col2:
            st.metric("Solución y₂(x)", f"{sp.latex(y2)}")
            st.latex(f"y_2 = {sp.latex(y2)}")

        # --- PASO 4: SOLUCIÓN GENERAL ---
        st.subheader("Paso 4: Solución General")
        st.write("La solución general es la combinación lineal de nuestro conjunto fundamental:")
        
        c1, c2 = sp.symbols('C1 C2')
        sol_final = c1*y1 + c2*y2
        
        st.success("Resultado Final:")
        st.latex(f"y(x) = {sp.latex(sol_final)}")

    except Exception as e:
        st.error(f"Error en los datos: {e}")

# --- AUTOR ---
st.markdown("---")
st.markdown("**Autor:** Elka Natalia Magaña Fierro")
