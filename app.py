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
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="OCR + Traductor + Audio",
    page_icon="🔊",
    layout="wide"
)


# =========================================================
# CARPETA PARA AUDIOS
# =========================================================

if not os.path.exists("temp"):
    os.mkdir("temp")


# =========================================================
# ELIMINAR AUDIOS ANTIGUOS
# =========================================================

def remove_files(n):
    mp3_files = glob.glob("temp/*.mp3")

    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400

        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)


remove_files(7)


# =========================================================
# TRADUCTOR
# =========================================================

translator = Translator()


# =========================================================
# FUNCIÓN TEXTO → TRADUCCIÓN → AUDIO
# =========================================================

def text_to_speech(input_language, output_language, text, tld):

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
    clean_name = "".join(
        c for c in text[:20]
        if c.isalnum() or c in (" ", "_", "-")
    ).strip()

    if not clean_name:
        clean_name = "audio"

    # Evitar espacios y caracteres problemáticos
    clean_name = clean_name.replace(" ", "_")

    file_path = f"temp/{clean_name}.mp3"

    tts.save(file_path)

    return clean_name, trans_text


# =========================================================
# TÍTULO
# =========================================================

st.title("Reconocimiento Óptico de Caracteres")

st.subheader(
    "Elige la fuente de la imagen, esta puede venir de la cámara "
    "o cargando un archivo"
)


# =========================================================
# VARIABLES
# =========================================================

text = ""


# =========================================================
# SIDEBAR - CÁMARA
# =========================================================

with st.sidebar:

    st.subheader("Procesamiento para Cámara")

    filtro = st.radio(
        "Filtro para imagen con cámara",
        ("Sí", "No")
    )


# =========================================================
# CÁMARA
# =========================================================

cam_ = st.checkbox("Usar Cámara")

img_file_buffer = None

if cam_:

    img_file_buffer = st.camera_input(
        "Toma una Foto"
    )


# =========================================================
# CARGAR IMAGEN
# =========================================================

bg_image = st.file_uploader(
    "Cargar Imagen:",
    type=["png", "jpg", "jpeg"]
)


# =========================================================
# OCR DE IMAGEN CARGADA
# =========================================================

if bg_image is not None:

    st.image(
        bg_image,
        caption="Imagen cargada",
        use_container_width=True
    )

    # Leer directamente desde memoria
    bytes_data = bg_image.getvalue()

    img_cv = cv2.imdecode(
        np.frombuffer(bytes_data, np.uint8),
        cv2.IMREAD_COLOR
    )

    if img_cv is not None:

        # Convertir BGR → RGB
        img_rgb = cv2.cvtColor(
            img_cv,
            cv2.COLOR_BGR2RGB
        )

        # OCR
        text = pytesseract.image_to_string(
            img_rgb
        )

        st.subheader("Texto reconocido")

        if text.strip():
            st.write(text)
        else:
            st.warning(
                "No se encontró texto en la imagen."
            )

    else:

        st.error(
            "No se pudo leer la imagen."
        )


# =========================================================
# OCR DE CÁMARA
# =========================================================

if img_file_buffer is not None:

    bytes_data = img_file_buffer.getvalue()

    cv2_img = cv2.imdecode(
        np.frombuffer(bytes_data, np.uint8),
        cv2.IMREAD_COLOR
    )

    if cv2_img is not None:

        # ---------------------------------------------
        # FILTRO
        # ---------------------------------------------

        if filtro == "Sí":

            cv2_img = cv2.bitwise_not(
                cv2_img
            )

        # ---------------------------------------------
        # BGR → RGB
        # ---------------------------------------------

        img_rgb = cv2.cvtColor(
            cv2_img,
            cv2.COLOR_BGR2RGB
        )

        # Mostrar imagen procesada
        st.image(
            img_rgb,
            caption="Imagen procesada",
            use_container_width=True
        )

        # ---------------------------------------------
        # OCR
        # ---------------------------------------------

        text = pytesseract.image_to_string(
            img_rgb
        )

        st.subheader("Texto reconocido")

        if text.strip():

            st.write(text)

        else:

            st.warning(
                "No se encontró texto en la imagen."
            )


# =========================================================
# SIDEBAR - TRADUCCIÓN
# =========================================================

with st.sidebar:

    st.subheader("Parámetros de traducción")


    # =====================================================
    # IDIOMA DE ENTRADA
    # =====================================================

    in_lang = st.selectbox(
        "Seleccione el lenguaje de entrada",
        (
            "Inglés",
            "Español",
            "Francés",
            "Bengalí",
            "Coreano",
            "Mandarín",
            "Japonés",
            "Alemán",
            "Danés",
        )
    )


    # Código del idioma de entrada
    input_languages = {

        "Inglés": "en",

        "Español": "es",

        "Francés": "fr",

        "Bengalí": "bn",

        "Coreano": "ko",

        "Mandarín": "zh-cn",

        "Japonés": "ja",

        "Alemán": "de",

        "Danés": "da",
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
            "Bengalí",
            "Coreano",
            "Mandarín",
            "Japonés",
            "Alemán",
            "Danés",
        )
    )


    # Código del idioma de salida
    output_languages = {

        "Inglés": "en",

        "Español": "es",

        "Francés": "fr",

        "Bengalí": "bn",

        "Coreano": "ko",

        "Mandarín": "zh-cn",

        "Japonés": "ja",

        "Alemán": "de",

        "Danés": "da",
    }


    output_language = output_languages[out_lang]


    # =====================================================
    # ACENTO / DIALECTO
    # =====================================================

    if out_lang == "Inglés":

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
                "South Africa",
            )
        )


        accent_tlds = {

            "Default": "com",

            "India": "co.in",

            "United Kingdom": "co.uk",

            "United States": "com",

            "Canada": "ca",

            "Australia": "com.au",

            "Ireland": "ie",

            "South Africa": "co.za",
        }


        tld = accent_tlds[english_accent]


    # =====================================================
    # ESPAÑOL
    # =====================================================

    elif out_lang == "Español":

        english_accent = st.selectbox(
            "Seleccione el dialecto",
            (
                "Español general",
                "España",
                "México",
                "Colombia",
                "Argentina",
                "Chile",
                "Perú",
            )
        )


        spanish_tlds = {

            "Español general": "com",

            "España": "es",

            "México": "com.mx",

            "Colombia": "com.co",

            "Argentina": "com.ar",

            "Chile": "cl",

            "Perú": "com.pe",
        }


        tld = spanish_tlds[english_accent]


    # =====================================================
    # FRANCÉS
    # =====================================================

    elif out_lang == "Francés":

        english_accent = st.selectbox(
            "Seleccione el dialecto",
            (
                "Francés estándar",
                "Francia",
                "Canadá",
            )
        )


        french_tlds = {

            "Francés estándar": "fr",

            "Francia": "fr",

            "Canadá": "ca",
        }


        tld = french_tlds[english_accent]


    # =====================================================
    # ALEMÁN
    # =====================================================

    elif out_lang == "Alemán":

        english_accent = st.selectbox(
            "Seleccione el dialecto",
            (
                "Alemán estándar",
                "Alemania",
                "Austria",
                "Suiza",
            )
        )


        german_tlds = {

            "Alemán estándar": "de",

            "Alemania": "de",

            "Austria": "at",

            "Suiza": "ch",
        }


        tld = german_tlds[english_accent]


    # =====================================================
    # DANÉS
    # =====================================================

    elif out_lang == "Danés":

        english_accent = st.selectbox(
            "Seleccione el dialecto",
            (
                "Danés estándar",
                "Dinamarca",
            )
        )


        danish_tlds = {

            "Danés estándar": "dk",

            "Dinamarca": "dk",
        }


        tld = danish_tlds[english_accent]


    # =====================================================
    # OTROS IDIOMAS
    # =====================================================

    else:

        english_accent = st.selectbox(
            "Seleccione el acento",
            (
                "Estándar",
            )
        )

        tld = "com"


    # =====================================================
    # MOSTRAR TEXTO
    # =====================================================

    display_output_text = st.checkbox(
        "Mostrar texto traducido"
    )


    # =====================================================
    # BOTÓN CONVERTIR
    # =====================================================

    if st.button(
        "🔊 Convertir",
        use_container_width=True
    ):

        if text.strip():

            try:

                result, output_text = text_to_speech(
                    input_language,
                    output_language,
                    text,
                    tld
                )


                # -----------------------------------------
                # AUDIO
                # -----------------------------------------

                audio_file = open(
                    f"temp/{result}.mp3",
                    "rb"
                )

                audio_bytes = audio_file.read()

                st.markdown(
                    "### 🔊 Tu audio:"
                )

                st.audio(
                    audio_bytes,
                    format="audio/mp3"
                )


                # -----------------------------------------
                # TEXTO TRADUCIDO
                # -----------------------------------------

                if display_output_text:

                    st.markdown(
                        "### 🌎 Texto de salida:"
                    )

                    st.write(
                        output_text
                    )


            except Exception as e:

                st.error(
                    "Ocurrió un error al traducir "
                    "o generar el audio."
                )

                st.write(e)


        else:

            st.warning(
                "Primero debes cargar una imagen "
                "o tomar una fotografía con la cámara."
            )
