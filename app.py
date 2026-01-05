import streamlit as st
import sympy as sp

# --- CONFIGURACIÓN DE PÁGINA ---
# Aquí cambiamos el nombre que aparece en la pestaña del navegador
st.set_page_config(page_title="Ecuación Diferencial Lineal de Orden 2", page_icon="∫")

# --- TÍTULO PRINCIPAL ---
st.title("Ecuación Diferencial Lineal de Orden 2")
st.markdown("Resuelve ecuaciones homogéneas de la forma: $a y'' + b y' + c y = 0$")

# --- 1. ENTRADA DE DATOS ---
st.subheader("1. Ingrese los coeficientes")

col1, col2, col3 = st.columns(3)

with col1:
    a_input = st.text_input("Coeficiente a (y'')", value="1")
with col2:
    b_input = st.text_input("Coeficiente b (y')", value="0")
with col3:
    c_input = st.text_input("Coeficiente c (y)", value="0")

def format_number(n):
    """Formatea números complejos o reales para mostrar."""
    return str(sp.simplify(n)).replace("**", "^").replace("*", "·")

# Botón para resolver
if st.button("Resolver Ecuación", type="primary"):
    try:
        # Validación y Conversión
        try:
            a_val = sp.S(a_input)
            b_val = sp.S(b_input)
            c_val = sp.S(c_input)
        except Exception:
            st.error("Los coeficientes deben ser expresiones matemáticas válidas (ej: 1, -5, 3/2, sqrt(2)).")
            st.stop()

        if a_val == 0:
            st.error("El coeficiente 'a' no puede ser cero en una ecuación de segundo orden.")
            st.stop()

        # --- 2. ECUACIÓN CARACTERÍSTICA ---
        m = sp.symbols("m")
        ec = a_val * m ** 2 + b_val * m + c_val
        
        st.subheader("2. Ecuación Característica")
        st.latex(f"{sp.latex(ec)} = 0")

        # --- CÁLCULO DE RAÍCES ---
        roots = sp.solve(ec, m)
        
        # Manejo seguro de índices de raíces
        if len(roots) == 0:
             st.error("No se encontraron raíces.")
             st.stop()
        elif len(roots) == 1:
             r1, r2 = roots[0], roots[0]
        else:
             r1, r2 = roots[0], roots[1]
        
        st.subheader("3. Raíces")
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            st.info(f"r1 = {format_number(r1)}")
        with col_r2:
            st.info(f"r2 = {format_number(r2)}")

        # --- 4. SOLUCIÓN GENERAL ---
        st.subheader("4. Solución General")
        
        y_c = None
        explicacion = ""

        # CASO 1: Complejas Conjugadas (Parte imaginaria distinta de 0)
        if sp.im(r1) != 0:
            alpha = sp.re(r1)
            beta = sp.Abs(sp.im(r1))
            
            lat_alpha = sp.latex(alpha)
            lat_beta = sp.latex(beta)
            
            # Si alpha es 0, no ponemos e^0x
            exp_part = f"e^{{{lat_alpha}x}}" if alpha != 0 else ""
            trig_part = f"(C_1 \\cos({lat_beta}x) + C_2 \\sin({lat_beta}x))"
            
            sol_latex = f"y_c = {exp_part} {trig_part}"
            explicacion = "Caso: Raíces complejas conjugadas ($r = \\alpha \\pm \\beta i$)"

        # CASO 2: Reales Repetidas
        elif r1 == r2:
            r_val = sp.latex(r1)
            exp_part = f"e^{{{r_val}x}}" if r1 != 0 else ""
            
            if r1 == 0:
                 sol_latex = "y_c = C_1 + C_2 x"
            else:
                 sol_latex = f"y_c = C_1 {exp_part} + C_2 x {exp_part}"
            
            explicacion = "Caso: Raíces reales repetidas."

        # CASO 3: Reales Distintas
        else:
            r1_val = sp.latex(r1)
            r2_val = sp.latex(r2)
            
            term1 = f"e^{{{r1_val}x}}" if r1 != 0 else "1"
            term2 = f"e^{{{r2_val}x}}" if r2 != 0 else "1"
            
            sol_latex = f"y_c = C_1 {term1} + C_2 {term2}"
            explicacion = "Caso: Raíces reales distintas."

        st.success(explicacion)
        st.latex(sol_latex)

    except Exception as e:
        st.error(f"Ocurrió un error: {e}")

# --- SECCIÓN DEL AUTOR ---
st.markdown("---") # Línea divisoria horizontal
st.markdown("### Créditos")
# REEMPLAZA "TU NOMBRE AQUÍ" CON TU NOMBRE REAL O ALIAS
st.markdown("**Autor:** [Elka Natalia Magaña Fierro]") 
st.caption("Desarrollado con Python y Streamlit para la resolución de Ecuaciones Diferenciales.")
