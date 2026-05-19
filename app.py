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
    
    /* Forzar a que el texto normal de la página sea oscuro y legible */
    .stApp p, .main-title, .sub-title {
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
    .stChatMessage[data-testid="stChatMessageAssistant"] p {
        color: #002b49 !important;
    }

    /* Diferenciar el chat del usuario (oro suave) */
    .stChatMessage[data-testid="stChatMessageUser"] {
        background-color: #fffaf0 !important;
        border-left: 5px solid #d4af37 !important;
    }
    .stChatMessage[data-testid="stChatMessageUser"] p {
        color: #002b49 !important;
    }

    /* --- SOLUCIÓN DE LETRAS INVISIBLES EN BOTONES --- */
    /* Forzamos el color del botón y que sus textos internos (span, p) sean BLANCOS */
    div.stButton > button {
        background-color: #002b49 !important;
        border-radius: 20px !important;
        border: 2px solid #d4af37 !important;
        padding: 8px 20px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    
    /* Esto obliga a que el texto de Streamlit dentro del botón sea blanco */
    div.stButton > button div, 
    div.stButton > button span, 
    div.stButton > button p {
        color: #ffffff !important;
    }
    
    /* Efecto Hover (pasar el mouse) */
    div.stButton > button:hover {
        background-color: #d4af37 !important;
        transform: scale(1.03);
    }
    
    div.stButton > button:hover div, 
    div.stButton > button:hover span, 
    div.stButton > button:hover p {
        color: #002b49 !important;
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
API_KEY_EXPO = st.secrets["API_KEY_EXPO"] 

# --- BASE DE DATOS DE CONOCIMIENTOS (CON INFO DE SU WEB) ---
HISTORIA_ICEST = """
El Instituto de Ciencias y Estudios Superiores de Tamaulipas (ICEST) fue fundado el 16 de abril de 1979 por el Rector Emérito, Lic. Carlos L. Dorantes del Rosal, D.E.
La rectora actual es la Mtra. Sandra L. Ávila Ramírez y su lema oficial es: "Calidad en educación a tu alcance".

CAMPUS Y COBERTURA:
Cuenta con campus estratégicos en Tampico (como Campus Tampico 2000, Campus Los Pinos, Campus Madero), además de extensiones en Veracruz, San Luis Potosí, Nuevo León, Michoacán y el Estado de México. También cuenta con un fuerte ecosistema de Educación a Distancia (Online).

OFERTA EDUCATIVA:
Ofrece Secundaria, Bachillerato (General y Tecnológico en diversas especialidades), Licenciaturas e Ingenierías con enorme prestigio en Ciencias de la Salud (Medicina, Enfermería, Odontología, Nutrición), así como carreras en Negocios, Ciencias Sociales y Tecnologías, además de Posgrados (Maestrías y Doctorados).

PROCESO DE ADMISIÓN:
Para inscribirse, los interesados pueden acudir directamente al campus de su elección o iniciar su registro digital en su portal web. Se requiere la documentación escolar básica (acta de nacimiento, certificados previos, CURP) y la institución ofrece revalidación y equivalencia de estudios para alumnos que vienen de otras escuelas.

HOSPITAL Y MUSEO:
La familia ICEST respalda su calidad educativa con proyectos de alto impacto como el Hospital San Juan Pablo II (complejo médico de alta tecnología para la práctica de sus alumnos) y el Museo del Automóvil y el Transporte en Tampico, que alberga una de las colecciones de autos históricos más importantes de todo México.
"""

# --- INSTRUCCIONES DEL CHATBOT ---
SYSTEM_PROMPT = f"""
Eres "Robot-ICEST", un asistente conversacional súper divertido, amigable y muy inteligente para la Exposición de Robótica.
Tu creador es un equipo de estudiantes de robótica. Hablas con mucho entusiasmo, usando de vez en cuando emojis robóticos (🤖, ⚡, ⚙️).
Usa la siguiente información real sobre la escuela para responder de forma concisa: {HISTORIA_ICEST}.
Si te preguntan cosas que no tienen relación con el ICEST, responde cordialmente diciendo que tus circuitos de memoria escolar solo tienen información del ICEST, y sugiéreles usar los botones rápidos o preguntar sobre las carreras, campus o curiosidades.
Escribe respuestas breves y legibles para que la gente en la expo no tenga que leer bloques gigantescos de texto.
"""

# --- ENCABEZADO DE LA INTERFAZ ---
st.markdown('<div class="main-title">🤖 ROBOT-ICEST 🤖</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Asistente Virtual - Expo de Robótica</div>', unsafe_allow_html=True)

# --- BOTÓN DISCRETO DE REINICIAR (ESQUINA SUPERIOR DERECHA) ---
col_espacio, col_reset = st.columns([4, 1])
with col_reset:
    if st.button("🗑️ Reiniciar"):
        st.session_state.messages = [{"role": "assistant", "content": "¡Memoria reseteada! 🤖 ¿En qué te puedo ayudar ahora?"}]
        st.session_state.indice_curiosidad = 0
        st.session_state.esperando_afirmacion = False
        st.rerun()

st.write("¡Bienvenido! Ven a chatear conmigo en tiempo real. Descubre la historia, los campus y los datos más interesantes de nuestra escuela.")

# --- MEMORIA INTEGRADA DEL CHAT Y SISTEMA DE TRIVIA ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! 🤖 Soy Robot-ICEST. Fui programado para esta expo de robótica para contarte todo sobre nuestra increíble escuela. ¿Quieres que te cuente un dato curioso, la historia o dónde están los campus?"}
    ]

# Lista de datos curiosos extraídos de su identidad y web
CURIOSIDADES = [
    "¿Sabías que el Museo del Automóvil del ICEST es de los más importantes del país? ¡Tiene autos clásicos reales que datan desde los inicios del transporte!",
    "¡El ICEST nació el 16 de abril de 1979! Empezó solo con bachillerato y carreras técnicas, y hoy tiene hasta complejos hospitalarios de primer nivel.",
    "El lema oficial de la escuela es 'Calidad en educación a tu alcance'. ¡Fue elegido para reflejar el compromiso de llevar educación de nivel a todas partes!",
    "El Hospital San Juan Pablo II del ICEST cuenta con tecnología médica de vanguardia única en el sur de Tamaulipas, donde practican los alumnos de medicina y enfermería.",
    "¡El ICEST está en gran parte de México! Además de Tamaulipas, tiene presencia física en Veracruz, San Luis Potosí, Nuevo León, Michoacán y el Estado de México.",
    "¡Identidad ICEST! Los valores principales de la institución que guían a cada alumno son la Honestidad, el Sentido de Responsabilidad y la Vocación de Servicio."
]

if "indice_curiosidad" not in st.session_state:
    st.session_state.indice_curiosidad = 0
if "esperando_afirmacion" not in st.session_state:
    st.session_state.esperando_afirmacion = False

# Mostrar historial de conversación
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- SECCIÓN DE BOTONES RÁPIDOS (PREGUNTAS PRINCIPALES) ---
st.write("⚡ **Preguntas Rápidas (Presiona un botón para probar):**")

col1, col2 = st.columns(2)
pregunta_sugerida = None
disparar_curiosidad = False

with col1:
    if st.button("📜 Historia de Fundación"):
        pregunta_sugerida = "¿Quién fundó el ICEST y en qué año?"
    if st.button("🎓 Oferta Educativa"):
        pregunta_sugerida = "¿Qué niveles educativos y carreras se pueden estudiar en el ICEST?"

with col2:
    if st.button("🏫 Campus y Sedes"):
        pregunta_sugerida = "¿Cuáles son los campus y estados donde tiene presencia el ICEST?"
    if st.button("✨ Datos Curiosos"):
        disparar_curiosidad = True

# --- LÓGICA DE TEXTO Y CAPTURA ---
user_input_active = None

if pregunta_sugerida:
    st.session_state.messages.append({"role": "user", "content": pregunta_sugerida})
    user_input_active = pregunta_sugerida
elif disparar_curiosidad:
    user_input_active = "¡Cuéntame un dato curioso!"
    st.session_state.esperando_afirmacion = True
else:
    captura_chat = st.chat_input("Pregúntale algo a Robot-ICEST...")
    if captura_chat:
        user_input_active = captura_chat

# Control de respuestas afirmativas para seguir hilando curiosidades
if user_input_active and not pregunta_sugerida and not disparar_curiosidad:
    if st.session_state.esperando_afirmacion:
        texto_usuario = user_input_active.lower().strip()
        if texto_usuario in ["si", "sí", "claro", "por supuesto", "otra", "siguiente", "ok", "va", "simon", "dale"]:
            st.session_state.indice_curiosidad = (st.session_state.indice_curiosidad + 1) % len(CURIOSIDADES)
        else:
            st.session_state.esperando_afirmacion = False

# --- PROCESAMIENTO E INTERACCIÓN ---
if user_input_active:
    if not pregunta_sugerida and not disparar_curiosidad:
        st.session_state.messages.append({"role": "user", "content": user_input_active})
    
    with st.chat_message("user"):
        st.write(user_input_active)

    try:
        # MODO CURIOSIDAD ACTIVO
        if st.session_state.esperando_afirmacion:
            dato_actual = CURIOSIDADES[st.session_state.indice_curiosidad]
            respuesta_robot = f"🤖 **¡Dato Curioso!**\n\n{dato_actual}\n\n¿Te gustaría conocer otra curiosidad del ICEST? (Responde con un *Sí*, *Claro* o presiona el botón de Datos Curiosos de nuevo)"
        
        # MODO PREGUNTA NORMAL
        else:
            client = genai.Client(api_key=API_KEY_EXPO)
            with st.spinner("🤖 Consultando mi base de datos..."):
                prompt_final = f"{SYSTEM_PROMPT}\n\nPregunta del visitante: {user_input_active}\nRespuesta del Robot-ICEST:"
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt_final
                )
                respuesta_robot = response.text

        with st.chat_message("assistant"):
            st.write(respuesta_robot)
        st.session_state.messages.append({"role": "assistant", "content": respuesta_robot})
        
        st.rerun()

    except Exception as e:
        st.error(f"⚠️ Error de Conexión: {e}")
