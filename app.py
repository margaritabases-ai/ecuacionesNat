import streamlit as st
import sympy as sp

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Tutor EDO 2do Orden", page_icon="📝")

# --- TÍTULO ---
st.title("Differential Equation Solver")
st.write("### Resolución paso a paso de: $a y'' + b y' + c y = 0$")

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
            st.error("El coeficiente 'a' no puede ser 0.")
            st.stop()

        # --- PASO 1: ECUACIÓN CARACTERÍSTICA ---
        st.header("Paso 1: La Ecuación Característica")
        st.info("""
        **¿De dónde sale esto?** Suponemos que la solución tiene la forma $y = e^{mx}$. Al sustituir esta función y sus derivadas en la ecuación original, 
        obtenemos una ecuación de segundo grado en términos de $m$.
        """)
        
        ec_carac = a*m**2 + b*m + c
        st.latex(f"{sp.latex(ec_carac)} = 0")

        # --- PASO 2: RAÍCES ---
        st.header("Paso 2: Cálculo de las raíces")
        st.write("Resolvemos para $m$ usando la fórmula general:")
        
        disc = b**2 - 4*a*c
        roots = sp.solve(ec_carac, m)
        
        st.latex(f"m = \\frac{{-({sp.latex(b)}) \\pm \\sqrt{{{sp.latex(b)}^2 - 4({sp.latex(a)})({sp.latex(c)})}}}}{{2({sp.latex(a)})}}")
        st.write(f"El discriminante es: $\\Delta = {sp.latex(disc)}$")

        # --- PASO 3: ANÁLISIS DE SOLUCIONES INDIVIDUALES ---
        st.header("Paso 3: Conjunto Fundamental ($y_1$ y $y_2$)")
        
        y1, y2 = None, None

        # CASO 1: Reales Distintas
        if disc > 0:
            r1, r2 = roots[0], roots[1]
            y1 = sp.exp(r1 * x)
            y2 = sp.exp(r2 * x)
            
            st.success("**Caso: Raíces Reales y Distintas**")
            st.write(f"Las raíces son $m_1 = {sp.latex(r1)}$ y $m_2 = {sp.latex(r2)}$.")
            st.markdown("""
            Como las raíces son diferentes, cada una genera una solución exponencial independiente. 
            El conjunto fundamental es:
            """)
            
        # CASO 2: Reales Repetidas
        elif disc == 0:
            r = roots[0]
            y1 = sp.exp(r * x)
            y2 = x * sp.exp(r * x)
            
            st.success("**Caso: Raíces Reales Repetidas**")
            st.write(f"Solo existe una raíz única: $m = {sp.latex(r)}$.")
            st.markdown("""
            Si usáramos $e^{mx}$ dos veces, las soluciones no serían independientes. 
            Por lo tanto, multiplicamos la segunda solución por **$x$** para que el conjunto sea linealmente independiente.
            """)

        # CASO 3: Complejas
        else:
            alpha = sp.re(roots[0])
            beta = sp.Abs(sp.im(roots[0]))
            y1 = sp.exp(alpha * x) * sp.cos(beta * x)
            y2 = sp.exp(alpha * x) * sp.sin(beta * x)
            
            st.success("**Caso: Raíces Complejas Conjugadas**")
            st.write(f"Las raíces son complejas: $m = {sp.latex(alpha)} \\pm {sp.latex(beta)}i$.")
            st.markdown(f"""
            Usando la **Identidad de Euler**, convertimos las exponenciales complejas en funciones reales. 
            La parte real ($\\alpha = {sp.latex(alpha)}$) va en la exponencial, y la imaginaria ($\\beta = {sp.latex(beta)}$) dentro del seno y coseno.
            """)

        # Mostrar y1 y y2 en cuadros destacados
        c1, c2 = st.columns(2)
        with c1:
            st.help(f"y_1(x) = {sp.latex(y1)}")
        with c2:
            st.help(f"y_2(x) = {sp.latex(y2)}")

        # --- PASO 4: SOLUCIÓN GENERAL ---
        st.header("Paso 4: Solución General")
        st.write("Combinamos las soluciones individuales multiplicándolas por constantes arbitrarias $C_1$ y $C_2$:")
        
        c1_sym, c2_sym = sp.symbols('C1 C2')
        sol_final = c1_sym*y1 + c2_sym*y2
        
        st.balloons()
        st.markdown(f"### ✨ Solución final:")
        st.latex(f"y(x) = {sp.latex(sol_final)}")

    except Exception as e:
        st.error(f"Hubo un problema con la expresión ingresada: {e}")

# --- PIE DE PÁGINA ---
st.markdown("---")
st.caption("Desarrollado por: Elka Natalia Magaña Fierro | Herramienta Educativa de Matemáticas")
