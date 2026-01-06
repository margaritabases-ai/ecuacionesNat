import streamlit as st
import sympy as sp

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Tutor EDO 2do Orden", page_icon="📝")

# --- TÍTULO ---
st.title("Solucionador de Ecuaciones Diferenciales")
st.write("### Resolución paso a paso de: $a y'' + b y' + c y = 0$")

# --- ENTRADA DE DATOS ---
with st.sidebar:
    st.header("1. Ingrese Coeficientes")
    a_val = st.text_input("Coeficiente a", value="1")
    b_val = st.text_input("Coeficiente b", value="-5")
    c_val = st.text_input("Coeficiente c", value="6")
    btn = st.button("Resolver ahora", type="primary")

if btn:
    try:
        a = sp.S(a_val)
        b = sp.S(b_val)
        c = sp.S(c_val)
        x = sp.symbols('x')
        m = sp.symbols('m')

        if a == 0:
            st.error("El coeficiente 'a' no puede ser 0.")
            st.stop()

        # --- PASO 1: ECUACIÓN CARACTERÍSTICA ---
        st.header("Paso 1: Ecuación Característica")
        st.write("Sustituimos $y = e^{mx}$ para obtener la ecuación auxiliar:")
        
        ec_carac = a*m**2 + b*m + c
        st.latex(f"{sp.latex(ec_carac)} = 0")

        # --- PASO 2: RAÍCES ---
        st.header("Paso 2: Cálculo de raíces")
        disc = b**2 - 4*a*c
        roots = sp.solve(ec_carac, m)
        
        st.write("Aplicamos la fórmula cuadrática:")
        st.latex(f"m = \\frac{{-({sp.latex(b)}) \\pm \\sqrt{{{sp.latex(disc)}}}}}{{2({sp.latex(a)})}}")

        # --- PASO 3: Y1 Y Y2 (CONJUNTO FUNDAMENTAL) ---
        st.header("Paso 3: Soluciones fundamentales")
        
        y1, y2 = None, None
        explicacion = ""

        if disc > 0:
            r1, r2 = roots[0], roots[1]
            y1 = sp.exp(r1 * x)
            y2 = sp.exp(r2 * x)
            explicacion = f"Las raíces son reales y distintas: $m_1 = {sp.latex(r1)}$ y $m_2 = {sp.latex(r2)}$."
        elif disc == 0:
            r = roots[0]
            y1 = sp.exp(r * x)
            y2 = x * sp.exp(r * x)
            explicacion = f"Raíz real repetida: $m = {sp.latex(r)}$. Usamos $x e^{{mx}}$ para la segunda solución."
        else:
            alpha = sp.re(roots[0])
            beta = sp.Abs(sp.im(roots[0]))
            y1 = sp.exp(alpha * x) * sp.cos(beta * x)
            y2 = sp.exp(alpha * x) * sp.sin(beta * x)
            explicacion = f"Raíces complejas: $m = {sp.latex(alpha)} \\pm {sp.latex(beta)}i$."

        st.info(explicacion)

        # MOSTRAR Y1 Y Y2 SIN TEXTO DE AYUDA EN INGLÉS
        col1, col2 = st.columns(2)
        with col1:
            st.write("#### $y_1(x)$")
            st.latex(sp.latex(y1))
        with col2:
            st.write("#### $y_2(x)$")
            st.latex(sp.latex(y2))

        # --- PASO 4: SOLUCIÓN GENERAL ---
        st.header("Paso 4: Solución General")
        st.write("La solución final es la suma de las soluciones fundamentales:")
        
        c1, c2 = sp.symbols('C1 C2')
        sol_final = c1*y1 + c2*y2
        
        st.success("### Resultado:")
        st.latex(f"y(x) = {sp.latex(sol_final)}")

    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("---")
st.caption("Autor: Elka Natalia Magaña Fierro")
