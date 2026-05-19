import streamlit as st
from google import genai

# --- CONFIGURACIÓN DE PÁGINA (ESTILO PROFESIONAL) ---
st.set_page_config(
    page_title="TibuBot - ICEST", 
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
    div.stButton > button {
        background-color: #002b49 !important;
        border-radius: 20px !important;
        border: 2px solid #d4af37 !important;
        padding: 8px 20px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    
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

# --- INSTRUCCIONES DEL CHATBOT (PERSONALIDAD DE TIBU NATURAL) ---
SYSTEM_PROMPT = f"""
Eres "Tibu", un asistente virtual genial, buena onda y muy inteligente programado por un equipo de estudiantes para esta Expo de Robótica.
Tu objetivo es dar información sobre el ICEST usando estos datos: {HISTORIA_ICEST}.

REGLAS DE ACTITUD REQUERIDAS:
1. Actúa de forma natural, amigable y conversacional. No suenes robótico ni aburrido.
2. REGLA ESTRICTA: No repitas tu nombre ("Tibu") ni digas "Soy Tibu" en cada respuesta. Solo te presentaste al inicio y ya está. Habla directamente sobre lo que te preguntan.
3. Sé directo y conciso. No avientes textos gigantescos; la gente en el stand prefiere respuestas rápidas y fáciles de leer.
4. Si te preguntan cosas que no tengan nada que ver con la escuela, di de manera relajada que tus circuitos solo traen la info del ICEST y recomiéndales usar los botones o preguntar por las carreras o campus.
"""

# --- ENCABEZADO DE LA INTERFAZ ---
st.markdown('<div class="main-title">🤖 TIBUBOT 🤖</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Asistente Virtual - Expo de Robótica</div>', unsafe_allow_html=True)

# --- BOTÓN DISCRETO DE REINICIAR (ESQUINA SUPERIOR DERECHA) ---
col_espacio, col_reset = st.columns([4, 1])
with col_reset:
    if st.button("🗑️ Reiniciar"):
        st.session_state.messages = [{"role": "assistant", "content": "¡Todo listo de nuevo! 🤖 ¿De qué quieres que platiquemos ahora?"}]
        st.session_state.indice_curiosidad = 0
        st.session_state.esperando_afirmacion = False
        st.rerun()

st.write("¡Bienvenido! Ven a chatear conmigo en tiempo real. Descubre la historia, los campus y los datos más interesantes de nuestra escuela.")

# --- MEMORIA INTEGRADA DEL CHAT Y SISTEMA DE TRIVIA ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! 🤖 Me llamo Tibu y fui programado por el equipo de robótica para ayudarte a conocer todo sobre nuestra escuela. ¿Qué te gustaría saber primero? Puedes usar los botones de abajo o escribirme lo que quieras."}
    ]

# Lista de datos curiosos extraídos de su identidad y web
CURIOSIDADES = [
    "¿Sabías que el Museo del Automóvil del ICEST es de los más importantes del país? ¡Tiene autos clásicos reales que datan desde los inicios del transporte!",
    "¡El ICEST nació el 16 de abril de 1979! Empezó solo con bachillerato y carreras técnicas, y hoy tiene hasta complejos hospitalarios de primer nivel.",
    "El lema oficial de la escuela es 'Calidad en educación a tu alcance'. ¡Fue elegido para reflejar el compromiso de llevar educación de nivel a todas partes!",
    "El Hospital San Juan Pablo II
