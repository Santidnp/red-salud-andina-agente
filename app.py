
import streamlit as st
from agente import responder

# Configuración de la página
st.set_page_config(
    page_title="Red Salud Andina",
    page_icon="🏥",
    layout="centered"
)

# Encabezado
st.title("🏥 Red Salud Andina")
st.caption("Asistente virtual de orientación al paciente")

st.info(
    "Puedo ayudarte con información sobre citas, "
    "sedes, horarios, requisitos, autorizaciones y costos. "
    "No tengo acceso a información personal ni puedo "
    "agendar citas o brindar consejo médico."
)

# Inicializar historial de conversación
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Mensaje de bienvenida
if not st.session_state.mensajes:
    with st.chat_message("assistant"):
        st.write(
            "¡Hola! 👋 Soy el asistente virtual de "
            "Red Salud Andina. ¿En qué puedo ayudarte?"
        )

# Mostrar mensajes anteriores
for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["role"]):
        st.write(mensaje["content"])

# Entrada del usuario
pregunta = st.chat_input("Escribe tu pregunta aquí...")

if pregunta:

    # Guardar historial antes de la nueva pregunta
    historial = st.session_state.mensajes.copy()

    # Mostrar pregunta del usuario
    with st.chat_message("user"):
        st.write(pregunta)

    st.session_state.mensajes.append({
        "role": "user",
        "content": pregunta
    })

    # Generar respuesta
    with st.chat_message("assistant"):
        with st.spinner("Consultando información..."):
            try:
                respuesta = responder(pregunta, historial)
                if not respuesta:
                    respuesta = (
                        "No pude generar una respuesta. "
                        "Puedes contactar a un asesor al "
                        "(601) 555 0100."
                    )
            except Exception:
                respuesta = (
                    "En este momento no puedo procesar "
                    "tu consulta. Puedes comunicarte con "
                    "un asesor al (601) 555 0100."
                )

        st.write(respuesta)

    # Guardar respuesta
    st.session_state.mensajes.append({
        "role": "assistant",
        "content": respuesta
    })

# Barra lateral
with st.sidebar:
    st.header("Información")

    st.write("**Red Salud Andina**")
    st.write("Orientación sobre servicios de salud.")

    st.divider()

    st.write("**Atención con asesor**")
    st.write("📞 (601) 555 0100")
    st.write("📱 WhatsApp: +57 300 555 0100")

    st.caption(
        "Lunes a viernes: 7:00 a 19:00\n\n"
        "Sábados: 8:00 a 14:00"
    )

    st.divider()

    if st.button("🗑️ Nueva conversación"):
        st.session_state.mensajes = []
        st.rerun()
