import streamlit as st
from PIL import Image
import os

# Configuración de la página
st.set_page_config(
    page_title="Simulador Educativo",
    page_icon="🎓",
    layout="centered"
)

# Datos de los reactivos
reactivos = [
    {
        "pregunta": "Un virus se reproduce de acuerdo con la siguiente tabulación. ¿Qué cantidad de virus habrá el noveno día?",
        "opciones": ["2 880", "1 944", "52 488"],
        "respuesta_correcta": 0,
        "area": "Pensamiento Matemático",
        "imagen": "imagenes/tabla_virus.png",
        "explicacion": "El virus se multiplica por 3 cada día: Día 1: 8, Día 2: 24, Día 3: 72, Día 4: 216... Día 9: 8 × 3^8 = 2,880"
    }
]

# Inicializar estado de la sesión
if 'pregunta_actual' not in st.session_state:
    st.session_state.pregunta_actual = 0
if 'respuesta_seleccionada' not in st.session_state:
    st.session_state.respuesta_seleccionada = None
if 'mostrar_resultado' not in st.session_state:
    st.session_state.mostrar_resultado = False

def mostrar_pregunta():
    reactivo = reactivos[st.session_state.pregunta_actual]
    
    # Título principal
    st.title("🎓 SIMULADOR EDUCATIVO")
    st.markdown("---")
    
    # Mostrar imagen si existe
    if "imagen" in reactivo and os.path.exists(reactivo["imagen"]):
        try:
            imagen = Image.open(reactivo["imagen"])
           st.image(imagen, caption="Tabla de datos", use_container_width=True)
        except Exception as e:
            st.warning(f"No se pudo cargar la imagen: {reactivo['imagen']}")
    else:
        st.info("📊 **Datos de la tabla:**\n\n• Día 1: 8 virus\n• Día 2: 24 virus\n• Día 3: 72 virus\n• Día 4: 216 virus")
    
    # Mostrar pregunta
    st.subheader("📝 Pregunta:")
    st.write(reactivo["pregunta"])
    
    # Área de selección
    st.subheader("🔘 Selecciona tu respuesta:")
    
    opciones_con_letras = [f"{chr(65+i)}) {opcion}" for i, opcion in enumerate(reactivo["opciones"])]
    
    respuesta = st.radio(
        "Opciones:",
        options=range(len(reactivo["opciones"])),
        format_func=lambda x: opciones_con_letras[x],
        key="respuesta_radio"
    )
    
    st.session_state.respuesta_seleccionada = respuesta
    
    # Botones
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✅ Verificar Respuesta", type="primary"):
            st.session_state.mostrar_resultado = True
    
    with col2:
        if st.button("🔄 Limpiar"):
            st.session_state.respuesta_seleccionada = None
            st.session_state.mostrar_resultado = False
            st.rerun()
    
    with col3:
        if st.button("🎲 Nueva Pregunta"):
            # Para cuando agregues más preguntas
            st.info("Próximamente más reactivos...")

def mostrar_resultado():
    if st.session_state.mostrar_resultado and st.session_state.respuesta_seleccionada is not None:
        reactivo = reactivos[st.session_state.pregunta_actual]
        respuesta_usuario = st.session_state.respuesta_seleccionada
        respuesta_correcta = reactivo["respuesta_correcta"]
        
        st.markdown("---")
        
        if respuesta_usuario == respuesta_correcta:
            st.success("🎉 ¡CORRECTO!")
            st.balloons()
            st.write(f"**La respuesta correcta es:** {chr(65+respuesta_correcta)}) {reactivo['opciones'][respuesta_correcta]}")
        else:
            st.error("❌ Incorrecto")
            st.write(f"**La respuesta correcta es:** {chr(65+respuesta_correcta)}) {reactivo['opciones'][respuesta_correcta]}")
        
        # Mostrar explicación
        if "explicacion" in reactivo:
            st.info(f"**📚 Explicación:** {reactivo['explicacion']}")

def main():
    # Sidebar con información
    with st.sidebar:
        st.header("📊 Información")
        st.write(f"**Área:** {reactivos[st.session_state.pregunta_actual]['area']}")
        st.write(f"**Pregunta:** {st.session_state.pregunta_actual + 1} de {len(reactivos)}")
        
        st.markdown("---")
        st.subheader("ℹ️ Acerca de")
        st.write("Simulador educativo desarrollado en Python con Streamlit.")
        st.write("Incluye reactivos de opción múltiple con soporte para imágenes.")
        
        st.markdown("---")
        st.subheader("🚀 Funcionalidades")
        st.write("• Reactivos interactivos")
        st.write("• Soporte para imágenes")
        st.write("• Explicaciones detalladas")
        st.write("• Interfaz web responsiva")
    
    # Contenido principal
    mostrar_pregunta()
    mostrar_resultado()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "Desarrollado con ❤️ usando Streamlit | "
        "<a href='https://github.com/felixmosunga/simulador-educativo-de-Python' target='_blank'>Ver en GitHub</a>"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
