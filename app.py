import streamlit as st
from groq import Groq
import base64

# --- CONFIGURACIÓN DE PÁGINA (ESTILO PROFESIONAL) ---
st.set_page_config(
    page_title="TibuBot - ICEST", 
    page_icon="🦈", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- INYECCIÓN DE CSS PERSONALIZADO (BLINDAJE Y ACOMODO VISUAL) ---
st.markdown("""
<style>
    /* Forzar fondo claro */
    .stApp {
        background-color: #fafbfc !important;
    }
    
    /* BLINDAJE DE TEXTO AZUL MARINO */
    .stApp p, .stApp span, .stApp label, .stApp li, .main-title, .sub-title, .stMarkdown div p, .welcome-box h3, .welcome-box p {
        color: #002b49 !important;
    }
    
    /* ESTILO DE BURBUJAS DE CHAT */
    .stChatMessage {
        border-radius: 15px !important;
        padding: 15px !important;
        margin-bottom: 12px !important;
    }
    .stChatMessage[data-testid="stChatMessageAssistant"] {
        background-color: #eef4f8 !important;
        border-left: 5px solid #002b49 !important;
    }
    .stChatMessage[data-testid="stChatMessageUser"] {
        background-color: #fffaf0 !important;
        border-left: 5px solid #d4af37 !important;
    }

    /* --- CENTRADO ABSOLUTO DEL BOTÓN EN STREAMLIT --- */
    .stButton {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
        margin-top: 10px !important;
    }
    .stButton > button {
        background-color: #51AFF7 !important;
        border-radius: 20px !important;
        border: 2px solid #4682B4 !important;
        padding: 12px 35px !important;
        font-weight: bold !important;
        color: #ffffff !important;
        width: auto !important;
        min-width: 260px !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        background-color: #d4af37 !important;
        color: #002b49 !important;
        transform: scale(1.05);
    }

    /* TÍTULOS */
    .main-title {
        text-align: center;
        margin-top: 10px;
        margin-bottom: 5px;
        font-size: 42px;
        font-family: 'Georgia', serif;
        font-weight: bold;
    }
    .sub-title {
        color: #d4af37 !important;
        text-align: center;
        font-size: 18px;
        margin-bottom: 30px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    /* CONTENEDOR DE LA PORTADA */
    .welcome-box {
        background-color: #eef4f8;
        border: 2px solid #51AFF7;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
    }
    
    /* CENTRADO DE LA IMAGEN EN EL HTML */
    .tibu-container {
        display: flex;
        justify-content: center;
        margin-bottom: 15px;
    }
    .tibu-container img {
        max-width: 180px;
        height: auto;
    }
</style>
""", unsafe_allow_html=True)

# --- CLAVE API LEYENDO DESDE STREAMLIT SECRETS ---
API_KEY_EXPO = st.secrets["API_KEY_EXPO"] 

# --- BASE DE DATOS DE CONOCIMIENTOS ---
HISTORIA_ICEST = """
El Instituto de Ciencias y Estudios Superiores de Tamaulipas (ICEST) fue fundado el 16 de abril de 1979 por el Rector Emérito, Lic. Carlos L. Dorantes del Rosal, D.E.
La rectora actual es la Mtra. Sandra L. Ávila Ramírez y su lema oficial es: "Calidad en educación a tu alcance".

CAMPUS Y COBERTURA:
Cuenta con campus estratégicos en Tampico (como Campus Tampico 2000, Campus Los Pinos, Campus Madero), además de extensiones en Veracruz, San Luis Potosí, Nuevo León, Michoacán y el Estado de México. También cuenta con un fuerte ecosistema de Educación a Distancia (Online).

POLITICA DE CALIDAD:
El Instituto de Ciencias y Estudios Superiores de Tamaulipas, A. C., es un sistema educativo comprometido en ofrecer un servicio de calidad en la formación integral del estudiante, mediante una atención personalizada, orientada al desarrollo humano y la formación en valores, infraestructura funcional y docentes capacitados, buscando siempre la satisfacción de nuestros alumnos, padres de familia, maestros y demás colaboradores.

OFERTA EDUCATIVA COMPLETA:
Educación Inicial (Maternal), Preescolar (Kinder), Primaria, Secundaria, Bachillerato, Licenciaturas, Ingenierías y Posgrados.
"""

INFO_EXTRA = """
INFORMACIÓN ADICIONAL DEL PROYECTO:
- Desarrollado para la Expo de Robótica de la Secundaria Francisco Javier Clavijero.
- Creadores: Felipe, Gerardo y Emmet.
"""

CONTEXTO_COMPLETO = HISTORIA_ICEST + "\n" + INFO_EXTRA

# --- INSTRUCCIONES DEL CHATBOT ---
SYSTEM_PROMPT = f"""
Eres "Tibu", un asistente virtual genial, buena onda y muy inteligente programado por un equipo de estudiantes para esta Expo de Robótica.
Tu objetivo es dar información sobre el ICEST usando estos datos: {CONTEXTO_COMPLETO}.

REGLAS:
1. Actúa natural y amigable. 
2. No repitas tu nombre en cada respuesta. 
3. Sé directo y conciso pero útil.
4. te llamas TIBU eres un tiburon, la imagen de icest ,tu eres asistente de robotica de la secundaria Franscisco Javier Clavijero.
5. Creado por 8 alumnos, especialmente por: "felipe guapo","gerardo" y "emmet".
6. Menciona la escuela como ICEST.
"""

# --- CONTROL DE PANTALLAS ---
if "pantalla" not in st.session_state:
    st.session_state.pantalla = "inicio"

# --- PANTALLA 1: INICIO ---
if st.session_state.pantalla == "inicio":
    # 1. LOGO CENTRADO ARRIBA
    col_a, col_logo, col_b = st.columns([1, 1.5, 1])
    with col_logo:
        try:
            st.image("logo_icest.png", use_container_width=True)
        except:
            pass

    # 2. TÍTULOS
    st.markdown('<div class="main-title">🦈 TIBUBOT 🦈</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Secundaria Francisco Javier Clavijero</div>', unsafe_allow_html=True)
    
    # TRUCO DE BLINDAJE: Convertir tibu_idle.webp a base64 para meterla de forma segura al HTML
    tibu_html_tag = "🦈"
    try:
        with open("tibu_idle.webp", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            tibu_html_tag = f'<img src="data:image/webp;base64,{encoded_string}" />'
    except:
        pass

    # 3. CUADRO DE INFO UTILIZANDO HTML PURO AL 100%
    st.markdown(f"""
    <div class="welcome-box">
        <div class="tibu-container">
            {tibu_html_tag}
        </div>
        <h3>¡Bienvenido a la Experiencia TibuBot!</h3>
        <p>Hola, soy <b>Tibu</b>, tu asistente de Inteligencia Artificial para esta Expo de Robótica.</p>
        <p>Estoy aquí para contarte todo sobre el <b>ICEST</b>, nuestra historia, campus y opciones de estudio desde maternal hasta posgrados.</p>
        <p style="font-size: 13px; color: #4682B4; margin-top: 15px; font-weight: bold;">Equipo de desarrollo: Felipe, Gerardo y Emmet.</p>
    </div>
    """, unsafe_allow_html=True)

    # 4. BOTÓN PERFECTAMENTE CENTRADO ABAJO
    if st.button("¡Empezar a Chatear! 🚀"):
        st.session_state.pantalla = "chat"
        st.rerun()

# --- PANTALLA 2: CHAT ---
elif st.session_state.pantalla == "chat":
    st.markdown('<div class="main-title">🦈 TIBUBOT 🦈</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Asistente Virtual ICEST</div>', unsafe_allow_html=True)

    col_espacio, col_reset = st.columns([4, 1])
    with col_reset:
        if st.button("🗑️ Reset"):
            st.session_state.messages = [{"role": "assistant", "content": "¡Todo listo de nuevo! 🤖 ¿De qué quieres platicar?"}]
            st.rerun()

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "¡Hola! 🦈 Soy Tibu. ¿Qué te gustaría saber sobre el ICEST?"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Botones rápidos
    col1, col2 = st.columns(2)
    pregunta_sugerida = None
    with col1:
        if st.button("📜 Historia"): pregunta_sugerida = "¿Quién fundó el ICEST?"
    with col2:
        if st.button("✨ Curiosidad"): pregunta_sugerida = "¡Cuéntame algo curioso!"

    captura = st.chat_input("Escribe tu pregunta...")
    user_input = captura if captura else pregunta_sugerida

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"): st.write(user_input)

        client = Groq(api_key=API_KEY_EXPO)
        with st.spinner("🤖 Tibu pensando..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
            )
            respuesta = response.choices[0].message.content
        
        with st.chat_message("assistant"): st.write(respuesta)
        st.session_state.messages.append({"role": "assistant", "content": respuesta})
        st.rerun()
