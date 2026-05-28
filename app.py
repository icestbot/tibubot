import streamlit as st
import cohere
import base64

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="TibuBot - ICEST", 
    page_icon="🦈", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- INYECCIÓN DE CSS PERSONALIZADO (BLINDAJE DE COLORES) ---
st.markdown("""
<style>
    .stApp { background-color: #fafbfc !important; }
    .stApp p, .stApp span, .stApp label, .stApp li, .main-title, .sub-title, .stMarkdown div p, .welcome-box h3, .welcome-box p {
        color: #002b49 !important;
    }
    .stChatMessage { border-radius: 15px !important; padding: 15px !important; margin-bottom: 12px !important; }
    .stChatMessage[data-testid="stChatMessageAssistant"] { background-color: #eef4f8 !important; border-left: 5px solid #002b49 !important; }
    .stChatMessage[data-testid="stChatMessageAssistant"] p { color: #002b49 !important; }
    .stChatMessage[data-testid="stChatMessageUser"] { background-color: #fffaf0 !important; border-left: 5px solid #d4af37 !important; }
    .stChatMessage[data-testid="stChatMessageUser"] p { color: #002b49 !important; }
    [data-testid="stButton"] { display: flex !important; justify-content: center !important; align-items: center !important; width: 100% !important; }
    div.stButton > button {
        background-color: #51AFF7 !important; border-radius: 20px !important; border: 2px solid #4682B4 !important;
        padding: 8px 15px !important; font-weight: bold !important; transition: all 0.3s ease !important; width: 100% !important;
    }
    div.stButton > button span { color: #ffffff !important; }
    div.stButton > button:hover { background-color: #d4af37 !important; transform: scale(1.02); }
    div.stButton > button:hover span { color: #002b49 !important; }
    .main-title { color: #002b49 !important; font-family: 'Georgia', serif; font-weight: bold; text-align: center; font-size: 38px; }
    .sub-title { color: #d4af37 !important; text-align: center; font-size: 18px; margin-bottom: 25px; font-weight: 500; text-transform: uppercase; }
    .welcome-box { background-color: #eef4f8; border: 2px solid #51AFF7; border-radius: 20px; padding: 30px; text-align: center; margin-bottom: 25px; }
    .tibu-container { display: flex; justify-content: center; margin-bottom: 15px; }
    .tibu-container img { max-width: 180px; height: auto; }
</style>
""", unsafe_allow_html=True)

# --- CLAVE API ---
COHERE_API_KEY = st.secrets["COHERE_API_KEY"]
co = cohere.ClientV2(COHERE_API_KEY)

# --- BASE DE DATOS DE CONOCIMIENTOS ---
HISTORIA_ICEST = """
El Instituto de Ciencias y Estudios Superiores de Tamaulipas (ICEST) fue fundado el 16 de abril de 1979 por el Rector Emérito, Lic. Carlos L. Dorantes del Rosal, D.E.
La rectora actual es la Mtra. Sandra L. Ávila Ramírez y su lema oficial es: "Calidad en educación a tu alcance".

CAMPUS Y COBERTURA:
Cuenta con campus estratégicos en Tampico (como Campus Tampico 2000, Campus Los Pinos, Campus Madero), además de extensiones en Veracruz, San Luis Potosí, Nuevo León, Michoacán y el Estado de México. También cuenta con un fuerte ecosistema de Educación a Distancia (Online).

OFERTA EDUCATIVA:
El ICEST ofrece un modelo educativo integral: Educación Inicial (Maternal), Educación Preescolar (Kinder), Primaria, Secundaria, Bachillerato (General y Tecnológico), Licenciaturas e Ingenierías (Medicina, Enfermería, Odontología, Nutrición, Psicología, Negocios, Tecnologías Avanzadas), Posgrados y Doctorados.

HOSPITAL Y MUSEO:
Cuenta con el Hospital San Juan Pablo II para prácticas médicas de sus alumnos y el Museo del Automóvil y el Transporte en Tampico.
"""

SYSTEM_PROMPT = f"""
Eres "Tibu", un asistente virtual genial, buena onda y tiburón de la secundaria Francisco Javier Clavijero. Fuiste creado para esta Expo de Robótica por el equipo de alumnos: Felipe, Gerardo y Emmet, supervisados por el Ing. Juan Carlos Nieto García.
Tu objetivo es dar información sobre el ICEST de forma amigable y concisa usando estos datos: {HISTORIA_ICEST}.
Reglas básicas: No repitas "Soy Tibu" en cada mensaje. Habla de forma natural, no des textos gigantes, y mantén las respuestas interactivas. Llama a la escuela simplemente "ICEST".
"""

CURIOSIDADES = [
    "¿Sabías que el Museo del Automóvil del ICEST tiene autos clásicos reales que datan desde los inicios del transporte?",
    "¡El ICEST nació el 16 de abril de 1979! Empezó solo con bachillerato y hoy tiene hasta complejos hospitalarios.",
    "El lema oficial de la escuela es 'Calidad en educación a tu alcance'.",
    "El Hospital San Juan Pablo II del ICEST cuenta con tecnología médica de vanguardia única en el sur de Tamaulipas."
]

if "pantalla" not in st.session_state:
    st.session_state.pantalla = "inicio"
if "indice_curiosidad" not in st.session_state:
    st.session_state.indice_curiosidad = 0
if "esperando_afirmacion" not in st.session_state:
    st.session_state.esperando_afirmacion = False

# --- PANTALLA 1: INICIO ---
if st.session_state.pantalla == "inicio":
    col_a, col_logo, col_b = st.columns([1, 1.5, 1])
    with col_logo:
        try: st.image("logo_icest.png", use_container_width=True)
        except: pass

    st.markdown('<div class="main-title">🦈 TIBUBOT 🦈</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Secundaria Francisco Javier Clavijero</div>', unsafe_allow_html=True)
    
    tibu_html_tag = "🦈"
    try:
        with open("perfil.png", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            tibu_html_tag = f'<img src="data:image/png;base64,{encoded_string}" />'
    except: pass

    st.markdown(f"""
    <div class="welcome-box">
        <div class="tibu-container">{tibu_html_tag}</div>
        <h3>¡Bienvenido a la Experiencia TibuBot!</h3>
        <p>Hola, soy <b>Tibu</b>, tu asistente de Inteligencia Artificial para esta Expo de Robótica.</p>
        <p>Estoy aquí para contarte todo sobre el <b>ICEST</b>.</p>
        <p style="font-size: 13px; color: #4682B4; margin-top: 15px; font-weight: bold;">Equipo: Felipe, Gerardo y Emmet.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("¡Empezar a Chatear! 🚀"):
        st.session_state.pantalla = "chat"
        st.rerun()

# --- PANTALLA 2: CHAT ---
elif st.session_state.pantalla == "chat":
    st.markdown('<div class="main-title">🦈 TIBUBOT 🦈</div>', unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "¡Hola! 🦈 Me llamo Tibu. ¿Qué te gustaría saber sobre el ICEST? Puedes usar los botones o escribirme."}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    st.write("⚡ **Preguntas Rápidas:**")
    col1, col2 = st.columns(2)
    pregunta_sugerida = None
    disparar_curiosidad = False

    with col1:
        if st.button("📜 Historia de Fundación"): pregunta_sugerida = "¿Quién fundó el ICEST y en qué año?"
        if st.button("🎓 Oferta Educativa"): pregunta_sugerida = "¿Qué niveles se pueden estudiar?"
    with col2:
        if st.button("🏫 Campus y Sedes"): pregunta_sugerida = "¿Dónde tiene campus el ICEST?"
        if st.button("✨ Datos Curiosos"): disparar_curiosidad = True

    user_input_active = None
    if pregunta_sugerida:
        st.session_state.messages.append({"role": "user", "content": pregunta_sugerida})
        user_input_active = pregunta_sugerida
    elif disparar_curiosidad:
        user_input_active = "¡Cuéntame un dato curioso!"
        st.session_state.esperando_afirmacion = True
    else:
        captura_chat = st.chat_input("Escribe tu pregunta aquí...")
        if captura_chat: user_input_active = captura_chat

    if user_input_active:
        if not pregunta_sugerida and not disparar_curiosidad:
            st.session_state.messages.append({"role": "user", "content": user_input_active})
        
        with st.chat_message("user"):
            st.write(user_input_active)

        try:
            if st.session_state.esperando_afirmacion and disparar_curiosidad:
                respuesta_robot = f"🤖 **¡Checa este dato!**\n\n{CURIOSIDADES[st.session_state.indice_curiosidad]}\n\n¿Quieres otro? Escribe *Sí*."
                st.session_state.indice_curiosidad = (st.session_state.indice_curiosidad + 1) % len(CURIOSIDADES)
            else:
                with st.spinner("🤖 Buscando..."):
                    chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]
                    for m in st.session_state.messages[-4:]:
                        chat_history.append({"role": m["role"], "content": m["content"]})
                    
                    response = co.chat(
                        model="command-nightly",  # Modelo moderno y activo
                        messages=chat_history
                    )
                    respuesta_robot = response.message.content

            with st.chat_message("assistant"):
                st.write(respuesta_robot)
            st.session_state.messages.append({"role": "assistant", "content": respuesta_robot})
            st.rerun()

        except Exception as e:
            st.error(f"⚠️ Error: {e}")
