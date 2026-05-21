import streamlit as st
from groq import Groq

# --- CONFIGURACIÓN DE PÁGINA (ESTILO PROFESIONAL) ---
st.set_page_config(
    page_title="TibuBot - ICEST", 
    page_icon="🤖", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- INYECCIÓN DE CSS PERSONALIZADO (BLINDAJE DE COLORES ANTI-MODO OSCURO) ---
st.markdown("""
<style>
    /* Forzar fondo claro */
    .stApp {
        background-color: #fafbfc !important;
    }
    
    /* BLINDAJE CONTRA LETRAS INVISIBLES: Obliga a todo texto común a ser azul marino */
    .stApp p, .stApp span, .stApp label, .stApp li, .main-title, .sub-title, .stMarkdown div p {
        color: #002b49 !important;
    }
    
    /* Contenedores de chat generales */
    .stChatMessage {
        border-radius: 15px !important;
        padding: 15px !important;
        margin-bottom: 12px !important;
    }
    
    /* Chat del asistente (Azul ICEST suave) con texto forzado oscuro */
    .stChatMessage[data-testid="stChatMessageAssistant"] {
        background-color: #eef4f8 !important;
        border-left: 5px solid #002b49 !important;
    }
    .stChatMessage[data-testid="stChatMessageAssistant"] p,
    .stChatMessage[data-testid="stChatMessageAssistant"] span,
    .stChatMessage[data-testid="stChatMessageAssistant"] div {
        color: #002b49 !important;
    }

    /* Chat del usuario (Oro suave) con texto forzado oscuro */
    .stChatMessage[data-testid="stChatMessageUser"] {
        background-color: #fffaf0 !important;
        border-left: 5px solid #d4af37 !important;
    }
    .stChatMessage[data-testid="stChatMessageUser"] p,
    .stChatMessage[data-testid="stChatMessageUser"] span,
    .stChatMessage[data-testid="stChatMessageUser"] div {
        color: #002b49 !important;
    }

    /* --- ESTILO SEGURO PARA BOTONES RÁPIDOS --- */
    div.stButton > button {
        background-color: #009EE8 !important;
        border-radius: 20px !important;
        border: 2px solid #d4af37 !important;
        padding: 8px 15px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    /* Forzar a que el texto interno de los botones sea siempre blanco */
    div.stButton > button div, 
    div.stButton > button span, 
    div.stButton > button p {
        color: #ffffff !important;
    }
    
    /* Efecto Hover (pasar el dedo o mouse) */
    div.stButton > button:hover {
        background-color: #d4af37 !important;
        transform: scale(1.02);
    }
    
    div.stButton > button:hover div, 
    div.stButton > button:hover span, 
    div.stButton > button:hover p {
        color: #002b49 !important;
    }

    /* Títulos principales */
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

# --- BASE DE DATOS DE CONOCIMIENTOS ---
HISTORIA_ICEST = """
El Instituto de Ciencias y Estudios Superiores de Tamaulipas (ICEST) fue fundado el 16 de abril de 1979 por el Rector Emérito, Lic. Carlos L. Dorantes del Rosal, D.E.
La rectora actual es la Mtra. Sandra L. Ávila Ramírez y su lema oficial es: "Calidad en educación a tu alcance".

CAMPUS Y COBERTURA:
Cuenta con campus estratégicos en Tampico (como Campus Tampico 2000, Campus Los Pinos, Campus Madero), además de extensiones en Veracruz, San Luis Potosí, Nuevo León, Michoacán y el Estado de México. También cuenta con un fuerte ecosistema de Educación a Distancia (Online).

POLITICA DE CALIDAD:
El Instituto de Ciencias y Estudios Superiores de Tamaulipas, A. C., es un sistema educativo comprometido en ofrecer un servicio de calidad en la formación integral del estudiante, mediante una atención personalizada, orientada al desarrollo humano y la formación en valores, infraestructura funcional y docentes capacitados, buscando siempre la satisfacción de nuestros alumnos, padres de familia, maestros y demás colaboradores, a través de un sistema de gestión de calidad, con procesos definidos que garantizan la provisión de servicios de administración de políticas y normatividades del sector educativo, su gestión y mejora sistemática, para aumentar nuestra participación en la sociedad y trascender en la misma.
OFERTA EDUCATIVA COMPLETA:
El ICEST ofrece un modelo educativo integral desde las etapas tempranas hasta el nivel profesional:
- Educación Inicial (Maternal).
- Educación Preescolar (Kinder).
- Primaria y Secundaria.
- Bachillerato (General y Tecnológico con diversas especialidades).
- Licenciaturas e Ingenierías de gran prestigio, especialmente en Ciencias de la Salud (Medicina, Enfermería, Odontología, Nutrición, Psicología), así como en Negocios, Ciencias Sociales, Hospitalidad y Tecnologías Avanzadas.
- Posgrados (Especialidades, Maestrías y Doctorados) y Educación Continua.

PROCESO DE ADMISIÓN:
Para inscribirse, los interesados pueden acudir directamente al campus de su elección o iniciar su registro digital en su portal web. Se requiere la documentación escolar básica (acta de nacimiento, certificados previos, CURP) y la institution ofrece revalidación y equivalencia de estudios para alumnos que vienen de otras escuelas.

HOSPITAL Y MUSEO:
La familia ICEST respalda su calidad educativa con proyectos de alto impacto como el Hospital San Juan Pablo II (complejo médico de alta tecnología para la práctica de sus alumnos) y el Museo del Automóvil y el Transporte en Tampico, que alberga una de las colecciones de autos históricos más importantes de todo México.
"""

# --- INSTRUCCIONES DEL CHATBOT (TUS REGLAS INTACTAS) ---
SYSTEM_PROMPT = f"""
Eres "Tibu", un asistente virtual genial, buena onda y muy inteligente programado por un equipo de estudiantes para esta Expo de Robótica.
Tu objetivo es dar información sobre el ICEST usando estos datos: {HISTORIA_ICEST}.

REGLAS DE ACTITUD REQUERIDAS:
1. Actúa de forma natural, amigable y conversacional. No suenes robótico ni aburrido.
2. REGLA ESTRICTA: No repitas tu nombre ("Tibu") ni digas "Soy Tibu" en cada respuesta. Solo te presentaste al inicio y ya está. Habla directamente sobre lo que te preguntan.
3. Sé medio directo y conciso. No avientes textos gigantescos pero no tan cortos ; la gente en el stand prefiere respuestas fáciles de leer pero utiles.
4. Asegúrate de destacar que la escuela ofrece TODOS los niveles educativos: desde Maternal y Kinder hasta Carreras y Doctorados si alguien pregunta por las opciones de estudio.
5. Si te preguntan cosas que no tengan nada que ver con la escuela, di de manera relajada que tus circuitos solo traen la info del ICEST y recomiéndales usar los botones o preguntar por las carreras o campus.
6. te llamas TIBU eres un tiburon, la imagen de icest ,tu eres estudiante tambien de 18 años
7. No repitas las curiosidades
8. no digas el nombre de la escuela siempre solo la primera vez que hables.
9. no digas cosas tan largas pero tampoco tan cortas
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

# --- MEMORIA INTEGRADA DEL CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! 🤖 Me llamo Tibu y fui programado por el equipo de robótica para ayudarte a conocer todo sobre nuestra escuela. ¿Qué te gustaría saber primero? Puedes usar los botones de abajo o escribirme lo que quieras."}
    ]

CURIOSIDADES = [
    "¿Sabías que el Museo del Automóvil del ICEST es de los más importantes del país? ¡Tiene autos clásicos reales que datan desde los inicios del transporte!",
    "¡El ICEST nació el 16 de abril de 1979! Empezó solo con bachillerato y carreras técnicas, y hoy tiene hasta complejos hospitalarios de primer nivel.",
    "El lema oficial de la escuela es 'Calidad en educación a tu alcance'. ¡Fue elegido para reflejar el compromiso de llevar educación de nivel a todas partes!",
    "El Hospital San Juan Pablo II del ICEST cuenta con tecnología médica de vanguardia única en el sur de Tamaulipas, donde practican los alumnos de medicina y enfermería.",
    "¡El ICEST está en gran parte de México! Además de Tamaulipas, tiene presencia física en Veracruz, San Luis Potosí, Nuevo León, Michoacán y el Estado de México.",
    "¡Desde los más chiquitos! El ICEST cuenta con una oferta completa que incluye Educación Inicial (Maternal) y Preescolar (Kinder), para cuidar y formar a los niños desde sus primeros pasos."
]

if "indice_curiosidad" not in st.session_state:
    st.session_state.indice_curiosidad = 0
if "esperando_afirmacion" not in st.session_state:
    st.session_state.esperando_afirmacion = False

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- SECCIÓN DE BOTONES RÁPIDOS ---
st.write("⚡ **Preguntas Rápidas (Presiona un botón para probar):**")
col1, col2 = st.columns(2)
pregunta_sugerida = None
disparar_curiosidad = False

with col1:
    if st.button("📜 Historia de Fundación"):
        pregunta_sugerida = "¿Quién fundó el ICEST y en qué año?"
    if st.button("🎓 Oferta Educativa"):
        pregunta_sugerida = "¿Qué niveles se pueden estudiar en el ICEST? ¿Tienen maternal y kinder?"

with col2:
    if st.button("🏫 Campus y Sedes"):
        pregunta_sugerida = "¿Cuáles son los campus y estados donde tiene presencia el ICEST?"
    if st.button("✨ Datos Curiosos"):
        disparar_curiosidad = True

user_input_active = None
if pregunta_sugerida:
    st.session_state.messages.append({"role": "user", "content": pregunta_sugerida})
    user_input_active = pregunta_sugerida
elif disparar_curiosidad:
    user_input_active = "¡Cuéntame un dato curioso!"
    st.session_state.esperando_afirmacion = True
else:
    captura_chat = st.chat_input("Escribe tu pregunta aquí...")
    if captura_chat:
        user_input_active = captura_chat

if user_input_active and not pregunta_sugerida and not disparar_curiosidad:
    if st.session_state.esperando_afirmacion:
        texto_usuario = user_input_active.lower().strip()
        if texto_usuario in ["si", "sí", "claro", "por supuesto", "otra", "siguiente", "ok", "va", "simon", "dale"]:
            st.session_state.indice_curiosidad = (st.session_state.indice_curiosidad + 1) % len(CURIOSIDADES)
        else:
            st.session_state.esperando_afirmacion = False

# --- PROCESAMIENTO CON LA API DE GROQ ---
if user_input_active:
    if not pregunta_sugerida and not disparar_curiosidad:
        st.session_state.messages.append({"role": "user", "content": user_input_active})
    
    with st.chat_message("user"):
        st.write(user_input_active)

    try:
        if st.session_state.esperando_afirmacion:
            dato_actual = CURIOSIDADES[st.session_state.indice_curiosidad]
            respuesta_robot = f"🤖 **¡Checa este dato!**\n\n{dato_actual}\n\n¿Te gustaría conocer otra curiosidad de la escuela? (Escribe *Sí* o *Claro* )"
        else:
            client = Groq(api_key=API_KEY_EXPO)
            with st.spinner("🤖 Revisando mi base de datos..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_input_active}
                    ],
                )
                respuesta_robot = response.choices[0].message.content

        with st.chat_message("assistant"):
            st.write(respuesta_robot)
        st.session_state.messages.append({"role": "assistant", "content": respuesta_robot})
        st.rerun()

    except Exception as e:
        st.error(f"⚠️ Detalle técnico en la conexión: {e}")
