import streamlit as st
import os
import time
import glob
import cv2
import numpy as np
import pytesseract
from PIL import Image
from gtts import gTTS
from googletrans import Translator


# =========================================================
# CONFIGURACIÓN DE LA PÁGINA
# =========================================================

st.set_page_config(
    page_title="Biblioteca Lingua",
    page_icon="📚",
    layout="wide"
)


# =========================================================
# ESTILOS
# =========================================================

st.markdown("""
<style>

    /* Fondo general */
    .stApp {
        background-color: #f7f9fc;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #eef3f8;
    }

    /* Títulos */
    h1 {
        color: #17324d;
        font-weight: 700;
    }

    h2 {
        color: #17324d;
    }

    h3 {
        color: #17324d;
    }

    /* Botones azules */
    .stButton > button {
        background-color: #1976d2;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        font-weight: 600;
        width: 100%;
        transition: 0.2s;
    }

    .stButton > button:hover {
        background-color: #125ca8;
        color: white;
        border: none;
    }

    /* Tarjetas */
    .card {
        background-color: white;
        padding: 22px;
        border-radius: 12px;
        border: 1px solid #e1e7ee;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        margin-bottom: 18px;
    }

    .card-title {
        color: #1976d2;
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .library-label {
        color: #1976d2;
        font-size: 15px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }

    .description {
        color: #5f6b76;
        font-size: 16px;
        line-height: 1.6;
    }

    /* Línea */
    hr {
        border-color: #dce4ec;
    }

</style>
""", unsafe_allow_html=True)


# VARIABLES

text = " "


# TRADUCCIÓN + TEXTO A VOZ

def text_to_speech(input_language, output_language, text, tld):

    translation = translator.translate(
        text,
        src=input_language,
        dest=output_language
    )

    trans_text = translation.text

    tts = gTTS(
        trans_text,
        lang=output_language,
        tld=tld,
        slow=False
    )

    try:
        my_file_name = text[0:20]
        my_file_name = "".join(
            c for c in my_file_name
            if c.isalnum() or c in (" ", "_", "-")
        ).strip()

        if my_file_name == "":
            my_file_name = "audio"

    except:
        my_file_name = "audio"

    os.makedirs("temp", exist_ok=True)

    tts.save(f"temp/{my_file_name}.mp3")

    return my_file_name, trans_text


# ELIMINAR AUDIOS ANTIGUOS

def remove_files(n):

    mp3_files = glob.glob("temp/*mp3")

    if len(mp3_files) != 0:

        now = time.time()
        n_days = n * 86400

        for f in mp3_files:

            if os.stat(f).st_mtime < now - n_days:

                os.remove(f)

                print("Deleted ", f)


remove_files(7)


# CARPETA TEMPORAL

try:
    os.mkdir("temp")
except:
    pass


# TRANSLATOR

translator = Translator()


# SESSION STATE

if "text" not in st.session_state:
    st.session_state.text = ""

if "image" not in st.session_state:
    st.session_state.image = None

if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""


# ENCABEZADO

st.title("📚 Biblioteca Lingua")

st.markdown(
    """
    <div class="card">

        <div class="library-label">
            LECTURA · TRADUCCIÓN · PRONUNCIACIÓN
        </div>

        <h2>Explora tus libros en cualquier idioma</h2>

        <p class="description">
            Escanea una página de un libro o carga una imagen.
            La aplicación reconocerá el texto, lo traducirá al
            idioma seleccionado y te permitirá escucharlo.
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


# SIDEBAR

with st.sidebar:

    st.markdown("## 📚 Biblioteca Lingua")

    st.markdown("### 📷 Fuente de lectura")

    # FILTRO

    filtro = st.radio(
        "Filtro para imagen con cámara",
        ('Sí', 'No')
    )

    # CÁMARA

    cam_ = st.checkbox("Usar Cámara")

    st.markdown("---")

    # PARÁMETROS DE TRADUCCIÓN

    st.markdown("### 🌐 Parámetros de traducción")

    # IDIOMA DE ENTRADA

    in_lang = st.selectbox(
        "Seleccione el lenguaje de entrada",
        (
            "Ingles",
            "Español",
            "Francés",
            "Alemán",
            "Danés",
            "Bengali",
            "koreano",
            "Mandarin",
            "Japones"
        ),
    )

    if in_lang == "Ingles":

        input_language = "en"

    elif in_lang == "Español":

        input_language = "es"

    elif in_lang == "Francés":

        input_language = "fr"

    elif in_lang == "Alemán":

        input_language = "de"

    elif in_lang == "Danés":

        input_language = "da"

    elif in_lang == "Bengali":

        input_language = "bn"

    elif in_lang == "koreano":

        input_language = "ko"

    elif in_lang == "Mandarin":

        input_language = "zh-cn"

    elif in_lang == "Japones":

        input_language = "ja"


    # IDIOMA DE SALIDA

    out_lang = st.selectbox(
        "Seleccione el lenguaje de salida",
        (
            "Ingles",
            "Español",
            "Francés",
            "Alemán",
            "Danés",
            "Bengali",
            "koreano",
            "Mandarin",
            "Japones"
        ),
    )

    if out_lang == "Ingles":

        output_language = "en"

    elif out_lang == "Español":

        output_language = "es"

    elif out_lang == "Francés":

        output_language = "fr"

    elif out_lang == "Alemán":

        output_language = "de"

    elif out_lang == "Danés":

        output_language = "da"

    elif out_lang == "Bengali":

        output_language = "bn"

    elif out_lang == "koreano":

        output_language = "ko"

    elif out_lang == "Mandarin":

        output_language = "zh-cn"

    elif out_lang == "Japones":

        output_language = "ja"


    # ACENTO / DIALECTO

    st.markdown("### 🎙️ Acento / variante regional")


    # INGLÉS

    if out_lang == "Ingles":

        english_accent = st.selectbox(
            "Seleccione el acento",
            (
                "Default",
                "India",
                "United Kingdom",
                "United States",
                "Canada",
                "Australia",
                "Ireland",
                "South Africa"
            ),
        )

        if english_accent == "Default":

            tld = "com"

        elif english_accent == "India":

            tld = "co.in"

        elif english_accent == "United Kingdom":

            tld = "co.uk"

        elif english_accent == "United States":

            tld = "com"

        elif english_accent == "Canada":

            tld = "ca"

        elif english_accent == "Australia":

            tld = "com.au"

        elif english_accent == "Ireland":

            tld = "ie"

        elif english_accent == "South Africa":

            tld = "co.za"


    # ESPAÑOL

    elif out_lang == "Español":

        spanish_accent = st.selectbox(
            "Seleccione el acento",
            (
                "Español general",
                "España",
                "México",
                "Colombia",
                "Argentina",
                "Chile",
                "Perú"
            ),
        )

        if spanish_accent == "España":

            tld = "es"

        elif spanish_accent == "México":

            tld = "com.mx"

        elif spanish_accent == "Colombia":

            tld = "com.co"

        elif spanish_accent == "Argentina":

            tld = "com.ar"

        elif spanish_accent == "Chile":

            tld = "cl"

        elif spanish_accent == "Perú":

            tld = "com.pe"

        else:

            tld = "com"


    # FRANCÉS

    elif out_lang == "Francés":

        french_accent = st.selectbox(
            "Seleccione el acento",
            (
                "Francés general",
                "Francia",
                "Canadá"
            ),
        )

        if french_accent == "Canadá":

            tld = "ca"

        else:

            tld = "fr"


    # ALEMÁN

    elif out_lang == "Alemán":

        german_accent = st.selectbox(
            "Seleccione el acento",
            (
                "Alemán general",
                "Alemania",
                "Austria",
                "Suiza"
            ),
        )

        if german_accent == "Austria":

            tld = "at"

        elif german_accent == "Suiza":

            tld = "ch"

        else:

            tld = "de"


    # DANÉS

    elif out_lang == "Danés":

        danish_accent = st.selectbox(
            "Seleccione el acento",
            (
                "Danés estándar",
                "Dinamarca"
            ),
        )

        tld = "dk"


    # COREANO
    elif out_lang == "koreano":

        st.selectbox(
            "Seleccione el acento",
            (
                "Coreano estándar",
                "Corea del Sur"
            ),
        )

        tld = "co.kr"


    # MANDARÍN

    elif out_lang == "Mandarin":

        chinese_accent = st.selectbox(
            "Seleccione el acento",
            (
                "Mandarín estándar",
                "China",
                "Taiwán"
            ),
        )

        if chinese_accent == "Taiwán":

            tld = "tw"

        else:

            tld = "cn"


    # JAPONÉS

    elif out_lang == "Japones":

        st.selectbox(
            "Seleccione el acento",
            (
                "Japonés estándar",
                "Japón"
            ),
        )

        tld = "co.jp"


    # BENGALÍ

    elif out_lang == "Bengali":

        st.selectbox(
            "Seleccione el acento",
            (
                "Bengalí estándar",
                "Bangladesh"
            ),
        )

        tld = "com"


    # OPCIÓN MOSTRAR TEXTO

    display_output_text = st.checkbox(
        "Mostrar texto traducido",
        value=True
    )


# FUENTE DE IMAGEN

if cam_:

    # CÁMARA

    st.markdown(
        """
        <div class="card-title">
            📷 Capturar página
        </div>
        """,
        unsafe_allow_html=True
    )

    img_file_buffer = st.camera_input(
        "Toma una foto de la página"
    )

else:

    # ARCHIVO

    st.markdown(
        """
        <div class="card-title">
            📖 Seleccionar página del libro
        </div>
        """,
        unsafe_allow_html=True
    )

    bg_image = st.file_uploader(
        "Cargar Imagen:",
        type=["png", "jpg", "jpeg"]
    )

    img_file_buffer = None


# PROCESAMIENTO DE IMAGEN CARGADA

if bg_image is not None:

    uploaded_file = bg_image

    # Mostrar imagen
    st.markdown(
        """
        <div class="card-title">
            📖 Página seleccionada
        </div>
        """,
        unsafe_allow_html=True
    )

    st.image(
        uploaded_file,
        caption="Imagen cargada.",
        use_container_width=True
    )

    # Guardar imagen

    with open(uploaded_file.name, 'wb') as f:

        f.write(uploaded_file.getvalue())

    st.success(
        f"Imagen guardada como {uploaded_file.name}"
    )

    # OpenCV

    img_cv = cv2.imread(
        f'{uploaded_file.name}'
    )

    if img_cv is not None:

        # FILTRO

        if filtro == "Sí":

            gray = cv2.cvtColor(
                img_cv,
                cv2.COLOR_BGR2GRAY
            )

            img_cv = cv2.threshold(
                gray,
                0,
                255,
                cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )[1]

        # RGB

        img_rgb = cv2.cvtColor(
            img_cv,
            cv2.COLOR_BGR2RGB
        )

        # OCR

        text = pytesseract.image_to_string(
            img_rgb
        )

        st.session_state.text = text


# PROCESAMIENTO DE CÁMARA

if img_file_buffer is not None:

    # Leer imagen

    bytes_data = img_file_buffer.getvalue()

    cv2_img = cv2.imdecode(
        np.frombuffer(
            bytes_data,
            np.uint8
        ),
        cv2.IMREAD_COLOR
    )


    # Aplicar filtro

    if filtro == "Sí":

        gray = cv2.cvtColor(
            cv2_img,
            cv2.COLOR_BGR2GRAY
        )

        cv2_img = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]


    # RGB

    img_rgb = cv2.cvtColor(
        cv2_img,
        cv2.COLOR_BGR2RGB
    )


   
    # Mostrar imagen
   
    st.markdown(
        """
        <div class="card-title">
            📷 Página capturada
        </div>
        """,
        unsafe_allow_html=True
    )

    st.image(
        img_rgb,
        caption="Imagen capturada",
        use_container_width=True
    )


    # OCR

    text = pytesseract.image_to_string(
        img_rgb
    )

    st.session_state.text = text


# TEXTO RECONOCIDO


if st.session_state.text.strip():

    st.markdown("---")

    st.markdown(
        """
        <div class="card-title">
            📝 Texto reconocido
        </div>
        """,
        unsafe_allow_html=True
    )

    st.text_area(
        "Resultado del OCR",
        st.session_state.text,
        height=220
    )

else:

    st.info(
        "Carga una página o toma una fotografía para reconocer el texto."
    )


# BOTÓN DE CONVERSIÓN


st.markdown("---")

if st.button(
    "🔵 Traducir y escuchar"
):

    if not st.session_state.text.strip():

        st.warning(
            "Primero debes cargar una imagen con texto."
        )

    else:

        try:

            with st.spinner(
                "Traduciendo y generando audio..."
            ):

                result, output_text = text_to_speech(
                    input_language,
                    output_language,
                    st.session_state.text,
                    tld
                )

                st.session_state.translated_text = output_text


            st.success(
                "¡Traducción completada!"
            )

            # RESULTADOS

            col1, col2 = st.columns(2)


           
            # TRADUCCIÓN

            with col1:

                st.markdown(
                    """
                    <div class="card-title">
                        🌎 Traducción
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if display_output_text:

                    st.write(
                        st.session_state.translated_text
                    )

            
            with col2:

                st.markdown(
                    """
                    <div class="card-title">
                        🔊 Escuchar traducción
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                audio_file = open(
                    f"temp/{result}.mp3",
                    "rb"
                )

                audio_bytes = audio_file.read()

                st.audio(
                    audio_bytes,
                    format="audio/mp3",
                    start_time=0
                )


        except Exception as e:

            st.error(
                f"No se pudo realizar la traducción: {e}"
            )




 
    
    
