import streamlit as st
from google import genai

# --- CONFIGURACIÓN DE PÁGINA (ESTILO PROFESIONAL) ---
st.set_page_config(
    page_title="Robot-ICEST", 
    page_icon="🤖", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- INYECCIÓN DE CSS PERSONALIZADO (IDENTIDAD CORPORATIVA ICEST) ---
st.markdown("""
<style>
    /* Estilizar fondo general de la app */
    .stApp {
        background-color: #fafbfc;
    }
    
    /* Forzar a que TODO el texto normal de la página sea oscuro y legible */
    .stApp, .stApp p, .stApp div, .stApp span {
        color: #002b49 !important;
    }
    
    /* Personalizar tarjetas y contenedores de chat */
    .stChatMessage {
        border-radius: 15px !important;
        padding: 15px !important;
        margin-bottom: 12px !important;
    }
    
    /* Diferenciar el chat del asistente (azul ICEST suave) */
    .stChatMessage[data-testid="stChatMessageAssistant"] {
        background-color: #eef4f8 !important;
        border-left: 5px solid #002b49 !important;
    }
    /* Forzar texto dentro del chat del asistente */
    .stChatMessage[data-testid="stChatMessageAssistant"] p {
        color: #002b49 !important;
    }

    /* Diferenciar el chat del usuario (oro suave) */
    .stChatMessage[data-testid="stChatMessageUser"] {
        background-color: #fffaf0 !important;
        border-left: 5px solid #d4af37 !important;
    }
    /* Forzar texto dentro del chat del usuario */
    .stChatMessage[data-testid="stChatMessageUser"] p {
        color: #002b49 !important;
    }

    /* Estilo para los botones rápidos de opciones (Texto Blanco Fijo) */
    div.stButton > button {
        background-color: #002b49 !important;
        color: #ffffff !important; /* <- Letra blanca */
        border-radius: 20px !important;
        border: 2px solid #d4af37 !important;
        padding: 8px 20px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    
    div.stButton > button:hover {
        background-color: #d4af37 !important;
        color: #002b49 !important; /* <- Cambia a azul al pasar el mouse */
        transform: scale(1.03);
    }

    /* Título principal con colores corporativos */
    .main-title {
        color: #002b49 !important;
        font-family: 'Georgia', serif;
        font-weight: bold;
        text-align: center;
        margin-bottom: 5px;
        font-size: 38px;
    }
    
    .sub-title {
        color: #d4af37 !important;
        text-align: center;
        font-size: 18px;
        margin-bottom: 25px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
</style>
""", unsafe_allow_html=True)

# --- CLAVE API LEYENDO DESDE STREAMLIT SECRETS ---
# 👇 CAMBIAMOS ESTA LÍNEA PARA QUE BUSQUE EN LA BÓVEDA OCULTA
API_KEY_EXPO = st.secrets["API_KEY_EXPO"] 

# --- BASE DE DATOS DE CONOCIMIENTOS ---
HISTORIA_ICEST = """
El Instituto de Ciencias y Estudios Superiores de Tamaulipas (ICEST) fue fundado el 16 de abril de 1979 por el visionario y Rector Emérito, Lic. Carlos L. Dorantes del Rosal, D.E.
El ICEST nació originalmente ofreciendo bachillerato y carreras técnicas comerciales. Con el tiempo se expandió para ofrecer licenciaturas, ingenierías y posgrados de excelente calidad.
La rectora actual es la Mtra. Sandra L. Ávila Ramírez.
El ICEST cuenta con múltiples campus en Tampico (como Campus Tampico 2000, Campus Los Pinos, Campus Madero), así como en otros estados como Veracruz, San Luis Potosí, Nuevo León, Michoacán y el Estado de México.
El lema oficial de la institución es: "Calidad en educación a tu alcance".
Además, la familia ICEST fundó el Hospital San Juan Pablo II (un hospital de vanguardia médica en el sur de Tamaulipas) y el espectacular Museo del Automóvil y el Transporte en Tampico (uno de los museos de autos históricos más importantes a nivel nacional).
"""

# --- INSTRUCCIONES DEL CHATBOT ---
SYSTEM_PROMPT = f"""
Eres "Robot-ICEST", un asistente conversacional súper divertido, amigable y muy inteligente para la Exposición de Robótica.
Tu creador es un equipo de estudiantes de robótica. Hablas con mucho entusiasmo, usando de vez en cuando emojis robóticos (🤖, ⚡, ⚙️).
Usa la siguiente información real sobre la escuela para responder: {HISTORIA_ICEST}.
Si te preguntan cosas que no tienen relación con el ICEST, responde cordialmente diciendo que tus circuitos de memoria escolar solo tienen información del ICEST, y sugiéreles preguntarte sobre la historia de la fundación de 1979 o los campus.
Escribe respuestas breves y legibles para que la gente en la expo no tenga que leer bloques gigantescos de texto.
"""

# --- ENCABEZADO DE LA INTERFAZ ---
st.markdown('<div class="main-title">🤖 ROBOT-ICEST 🤖</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Asistente Virtual - Expo de Robótica</div>', unsafe_allow_html=True)

st.write("¡Bienvenido! Ven a chatear conmigo en tiempo real. Descubre la historia, los campus y los datos más interesantes de nuestra escuela.")

# --- MEMORIA INTEGRADA DEL CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! 🤖 Soy Robot-ICEST. Fui programado para esta expo de robótica para contarte todo sobre nuestra increíble escuela. ¿Quieres que te cuente un dato curioso, la historia o dónde están los campus?"}
    ]

# Mostrar historial de conversación
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- SECCIÓN DE BOTONES RÁPIDOS ---
st.write("⚡ **Preguntas Rápidas (Presiona un botón para probar):**")
col1, col2, col3 = st.columns(3)

pregunta_sugerida = None

with col1:
    if st.button("📜 Historia de Fundación"):
        pregunta_sugerida = "¿Quién fundó el ICEST y en qué año?"
with col2:
    if st.button("🏫 Campus y Sedes"):
        pregunta_sugerida = "¿Cuáles son los campus que tiene el ICEST?"
with col3:
    if st.button("🚗 Museo del Automóvil"):
        pregunta_sugerida = "¿Qué relación tiene el ICEST con el Museo del Automóvil?"

# Lógica si presionaron un botón sugerido
if pregunta_sugerida:
    st.session_state.messages.append({"role": "user", "content": pregunta_sugerida})
    user_input_active = pregunta_sugerida
else:
    user_input_active = st.chat_input("Pregúntale algo a Robot-ICEST...")

# --- PROCESAMIENTO E INTERACCIÓN CON GEMINI ---
if user_input_active:
    if not pregunta_sugerida:
        st.session_state.messages.append({"role": "user", "content": user_input_active})
        with st.chat_message("user"):
            st.write(user_input_active)
    else:
        with st.chat_message("user"):
            st.write(user_input_active)

    # Llamada al cerebro de Inteligencia Artificial (Gemini)
    try:
        client = genai.Client(api_key=API_KEY_EXPO)
        
        with st.spinner("🤖 Consultando mi base de datos..."):
            prompt_final = f"{SYSTEM_PROMPT}\n\nPregunta del visitante: {user_input_active}\nRespuesta del Robot-ICEST:"
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt_final
            )
            
            respuesta_robot = response.text

        # Mostrar respuesta en pantalla y guardar en memoria
        with st.chat_message("assistant"):
            st.write(respuesta_robot)
        st.session_state.messages.append({"role": "assistant", "content": respuesta_robot})
        
        if pregunta_sugerida:
            st.rerun()

    except Exception as e:
        st.error(f"⚠️ Error de Conexión: {e}")
