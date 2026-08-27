import streamlit as st
import os
import time
import glob
import cv2
import numpy as np
import pytesseract
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

    /* Botones */
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

    hr {
        border-color: #dce4ec;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# CARPETA TEMPORAL
# =========================================================

os.makedirs("temp", exist_ok=True)


# =========================================================
# ELIMINAR AUDIOS ANTIGUOS
# =========================================================

def remove_files(n):

    mp3_files = glob.glob("temp/*.mp3")

    if len(mp3_files) > 0:

        now = time.time()
        n_days = n * 86400

        for f in mp3_files:

            if os.stat(f).st_mtime < now - n_days:

                try:
                    os.remove(f)
                except:
                    pass


remove_files(7)


# =========================================================
# TRANSLATOR
# =========================================================

translator = Translator()


# =========================================================
# SESSION STATE
# =========================================================

if "text" not in st.session_state:
    st.session_state.text = ""

if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

if "audio_file" not in st.session_state:
    st.session_state.audio_file = None


# =========================================================
# FUNCIÓN TRADUCCIÓN + TEXTO A VOZ
# =========================================================

def text_to_speech(
    input_language,
    output_language,
    text,
    tld
):

    # Traducir
    translation = translator.translate(
        text,
        src=input_language,
        dest=output_language
    )

    trans_text = translation.text

    # Crear audio
    tts = gTTS(
        text=trans_text,
        lang=output_language,
        tld=tld,
        slow=False
    )

    # Crear nombre seguro
    my_file_name = text[:20]

    my_file_name = "".join(
        c for c in my_file_name
        if c.isalnum() or c in (" ", "_", "-")
    ).strip()

    if my_file_name == "":
        my_file_name = "audio"

    my_file_name = my_file_name.replace(" ", "_")

    # Ruta
    file_path = f"temp/{my_file_name}.mp3"

    # Guardar
    tts.save(file_path)

    return file_path, trans_text


# =========================================================
# ENCABEZADO
# =========================================================

st.title("📚 Biblioteca Lingua")

st.markdown(
    """
    <div class="card">

        LECTURA · TRADUCCIÓN · PRONUNCIACIÓN
        
        Explora tus libros en cualquier idioma

        Escanea una página de un libro o carga una imagen.
        La aplicación reconocerá el texto, lo traducirá al
        idioma seleccionado y te permitirá escucharlo.

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# VARIABLES
# =========================================================

# MUY IMPORTANTE:
# Se inicializan para evitar NameError
bg_image = None
img_file_buffer = None


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 📚 Biblioteca Lingua")

    st.markdown("### 📷 Fuente de lectura")

    # -----------------------------------------------------
    # FILTRO
    # -----------------------------------------------------

    filtro = st.radio(
        "Filtro para imagen con cámara",
        ("Sí", "No")
    )

    # -----------------------------------------------------
    # CÁMARA
    # -----------------------------------------------------

    cam_ = st.checkbox(
        "Usar Cámara"
    )

    st.markdown("---")

    # =====================================================
    # PARÁMETROS DE TRADUCCIÓN
    # =====================================================

    st.markdown(
        "### 🌐 Parámetros de traducción"
    )


    # =====================================================
    # IDIOMA DE ENTRADA
    # =====================================================

    in_lang = st.selectbox(
        "Seleccione el lenguaje de entrada",
        (
            "Inglés",
            "Español",
            "Francés",
            "Alemán",
            "Danés",
            "Bengalí",
            "Coreano",
            "Mandarín",
            "Japonés"
        )
    )


    input_languages = {

        "Inglés": "en",
        "Español": "es",
        "Francés": "fr",
        "Alemán": "de",
        "Danés": "da",
        "Bengalí": "bn",
        "Coreano": "ko",
        "Mandarín": "zh-cn",
        "Japonés": "ja"
    }


    input_language = input_languages[in_lang]


    # =====================================================
    # IDIOMA DE SALIDA
    # =====================================================

    out_lang = st.selectbox(
        "Seleccione el lenguaje de salida",
        (
            "Inglés",
            "Español",
            "Francés",
            "Alemán",
            "Danés",
            "Bengalí",
            "Coreano",
            "Mandarín",
            "Japonés"
        )
    )


    output_languages = {

        "Inglés": "en",
        "Español": "es",
        "Francés": "fr",
        "Alemán": "de",
        "Danés": "da",
        "Bengalí": "bn",
        "Coreano": "ko",
        "Mandarín": "zh-cn",
        "Japonés": "ja"
    }


    output_language = output_languages[out_lang]


    # =====================================================
    # ACENTO / VARIANTE
    # =====================================================

    st.markdown(
        "### 🎙️ Acento / variante regional"
    )


    # =====================================================
    # INGLÉS
    # =====================================================

    if out_lang == "Inglés":

        accent = st.selectbox(
            "Seleccione el acento",
            (
                "Default",
                "India",
                "Reino Unido",
                "Estados Unidos",
                "Canadá",
                "Australia",
                "Irlanda",
                "Sudáfrica"
            )
        )


        accent_tlds = {

            "Default": "com",
            "India": "co.in",
            "Reino Unido": "co.uk",
            "Estados Unidos": "com",
            "Canadá": "ca",
            "Australia": "com.au",
            "Irlanda": "ie",
            "Sudáfrica": "co.za"
        }


        tld = accent_tlds[accent]


    # =====================================================
    # ESPAÑOL
    # =====================================================

    elif out_lang == "Español":

        accent = st.selectbox(
            "Seleccione el dialecto",
            (
                "Español general",
                "España",
                "México",
                "Colombia",
                "Argentina",
                "Chile",
                "Perú"
            )
        )


        accent_tlds = {

            "Español general": "com",
            "España": "es",
            "México": "com.mx",
            "Colombia": "com.co",
            "Argentina": "com.ar",
            "Chile": "cl",
            "Perú": "com.pe"
        }


        tld = accent_tlds[accent]


    # =====================================================
    # FRANCÉS
    # =====================================================

    elif out_lang == "Francés":

        accent = st.selectbox(
            "Seleccione el acento",
            (
                "Francés estándar",
                "Francia",
                "Canadá"
            )
        )


        if accent == "Canadá":
            tld = "ca"
        else:
            tld = "fr"


    # =====================================================
    # ALEMÁN
    # =====================================================

    elif out_lang == "Alemán":

        accent = st.selectbox(
            "Seleccione el acento",
            (
                "Alemán estándar",
                "Alemania",
                "Austria",
                "Suiza"
            )
        )


        if accent == "Austria":

            tld = "at"

        elif accent == "Suiza":

            tld = "ch"

        else:

            tld = "de"


    # =====================================================
    # DANÉS
    # =====================================================

    elif out_lang == "Danés":

        accent = st.selectbox(
            "Seleccione el acento",
            (
                "Danés estándar",
                "Dinamarca"
            )
        )

        tld = "dk"


    # =====================================================
    # COREANO
    # =====================================================

    elif out_lang == "Coreano":

        accent = st.selectbox(
            "Seleccione el acento",
            (
                "Coreano estándar",
                "Corea del Sur"
            )
        )

        tld = "co.kr"


    # =====================================================
    # MANDARÍN
    # =====================================================

    elif out_lang == "Mandarín":

        accent = st.selectbox(
            "Seleccione la variante",
            (
                "Mandarín estándar",
                "China continental",
                "Taiwán"
            )
        )


        if accent == "Taiwán":

            tld = "tw"

        else:

            tld = "cn"


    # =====================================================
    # JAPONÉS
    # =====================================================

    elif out_lang == "Japonés":

        accent = st.selectbox(
            "Seleccione el acento",
            (
                "Japonés estándar",
                "Japón"
            )
        )

        tld = "co.jp"


    # =====================================================
    # BENGALÍ
    # =====================================================

    elif out_lang == "Bengalí":

        accent = st.selectbox(
            "Seleccione el acento",
            (
                "Bengalí estándar",
                "Bangladesh"
            )
        )

        tld = "com"


    # =====================================================
    # MOSTRAR TEXTO
    # =====================================================

    display_output_text = st.checkbox(
        "Mostrar texto traducido",
        value=True
    )


# =========================================================
# FUENTE DE IMAGEN
# =========================================================

if cam_:

    # =====================================================
    # CÁMARA
    # =====================================================

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

    # =====================================================
    # SUBIR IMAGEN
    # =====================================================

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
        type=[
            "png",
            "jpg",
            "jpeg"
        ]
    )


# =========================================================
# PROCESAMIENTO DE IMAGEN CARGADA
# =========================================================

if bg_image is not None:

    st.markdown(
        """
        <div class="card">
            <div class="card-title">
                📖 Página seleccionada
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


    # Mostrar imagen
    st.image(
        bg_image,
        caption="Imagen cargada",
        use_container_width=True
    )


    # -----------------------------------------------------
    # Leer imagen
    # -----------------------------------------------------

    bytes_data = bg_image.getvalue()

    img_cv = cv2.imdecode(
        np.frombuffer(
            bytes_data,
            np.uint8
        ),
        cv2.IMREAD_COLOR
    )


    if img_cv is not None:

        # -------------------------------------------------
        # FILTRO
        # -------------------------------------------------

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


        # -------------------------------------------------
        # CONVERTIR A RGB
        # -------------------------------------------------

        img_rgb = cv2.cvtColor(
            img_cv,
            cv2.COLOR_BGR2RGB
        )


        # -------------------------------------------------
        # OCR
        # -------------------------------------------------

        text = pytesseract.image_to_string(
            img_rgb
        )


        st.session_state.text = text


# =========================================================
# PROCESAMIENTO DE CÁMARA
# =========================================================

if img_file_buffer is not None:

    # -----------------------------------------------------
    # Leer imagen
    # -----------------------------------------------------

    bytes_data = img_file_buffer.getvalue()

    cv2_img = cv2.imdecode(
        np.frombuffer(
            bytes_data,
            np.uint8
        ),
        cv2.IMREAD_COLOR
    )


    if cv2_img is not None:

        # -------------------------------------------------
        # FILTRO
        # -------------------------------------------------

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


        # -------------------------------------------------
        # RGB
        # -------------------------------------------------

        img_rgb = cv2.cvtColor(
            cv2_img,
            cv2.COLOR_BGR2RGB
        )


        # -------------------------------------------------
        # Mostrar imagen
        # -------------------------------------------------

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
            caption="Imagen procesada",
            use_container_width=True
        )


        # -------------------------------------------------
        # OCR
        # -------------------------------------------------

        text = pytesseract.image_to_string(
            img_rgb
        )


        st.session_state.text = text


# =========================================================
# TEXTO RECONOCIDO
# =========================================================

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
        "📖 Carga una página o toma una fotografía "
        "para reconocer el texto."
    )


# =========================================================
# BOTÓN TRADUCIR Y ESCUCHAR
# =========================================================

st.markdown("---")


if st.button(
    "🔊 Traducir y escuchar"
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

                audio_path, output_text = text_to_speech(
                    input_language,
                    output_language,
                    st.session_state.text,
                    tld
                )


                st.session_state.translated_text = output_text
                st.session_state.audio_file = audio_path


            st.success(
                "¡Traducción completada!"
            )


            # =================================================
            # RESULTADOS
            # =================================================

            col1, col2 = st.columns(2)


            # -------------------------------------------------
            # TRADUCCIÓN
            # -------------------------------------------------

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


            # -------------------------------------------------
            # AUDIO
            # -------------------------------------------------

            with col2:

                st.markdown(
                    """
                    <div class="card-title">
                        🔊 Escuchar traducción
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                if (
                    st.session_state.audio_file
                    and os.path.exists(
                        st.session_state.audio_file
                    )
                ):

                    with open(
                        st.session_state.audio_file,
                        "rb"
                    ) as audio_file:

                        audio_bytes = audio_file.read()


                    st.audio(
                        audio_bytes,
                        format="audio/mp3"
                    )


        except Exception as e:

            st.error(
                "No se pudo realizar la traducción "
                "o generar el audio."
            )

            st.exception(e)
