"""
Mobile-Optimized Streamlit App with PWA Support
Can be installed as an app on Android/iOS
"""

import streamlit as st
from pathlib import Path
import sys

# Add parent directory to path
script_dir = Path(__file__).parent.resolve()
sys.path.insert(0, str(script_dir))

from two_stage_detection import TwoStageDetector
import cv2
import numpy as np
from PIL import Image
import io

# PWA Configuration
st.set_page_config(
    page_title="Обнаружение деревьев",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="collapsed",  # Better for mobile
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": "Система обнаружения деревьев и дефектов",
    },
)


# Add PWA manifest and service worker support
def add_pwa_support():
    """Add PWA meta tags and manifest"""
    pwa_html = """
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="apple-mobile-web-app-title" content="Детекция деревьев">
        <meta name="theme-color" content="#2E7D32">
        <link rel="manifest" href="/manifest.json">
        <link rel="apple-touch-icon" href="/static/icon-192.png">
    </head>
    """
    st.markdown(pwa_html, unsafe_allow_html=True)


# Mobile-optimized CSS
def add_mobile_styles():
    """Add mobile-friendly CSS"""
    mobile_css = """
    <style>
        /* Mobile optimizations */
        @media (max-width: 768px) {
            .stButton button {
                width: 100%;
                padding: 1rem;
                font-size: 1.1rem;
            }
            
            .stSlider {
                padding: 0.5rem 0;
            }
            
            img {
                max-width: 100%;
                height: auto;
            }
            
            /* Hide Streamlit branding on mobile */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
        }
        
        /* Full-width upload area */
        .uploadedFile {
            width: 100%;
        }
        
        /* Better touch targets */
        button, a, input {
            min-height: 44px;
            min-width: 44px;
        }
        
        /* Compact layout */
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
    </style>
    """
    st.markdown(mobile_css, unsafe_allow_html=True)


add_pwa_support()
add_mobile_styles()

# App title
st.title("🌲 Детекция деревьев")
st.markdown("*Мобильная версия*")


# Initialize detector
@st.cache_resource
def load_detector():
    """Load models with caching"""
    script_dir = Path(__file__).parent.resolve()
    tree_model = (
        script_dir / "runs" / "detect" / "tree_detection_cpu" / "weights" / "best.pt"
    )
    defect_model = (
        script_dir
        / "runs"
        / "defects"
        / "tree_defects_detection2"
        / "weights"
        / "best.pt"
    )

    return TwoStageDetector(
        tree_model_path=str(tree_model), defect_model_path=str(defect_model)
    )


try:
    detector = load_detector()
except Exception as e:
    st.error(f"⚠️ Ошибка загрузки моделей: {e}")
    st.stop()

# Simple mobile UI
st.markdown("### 📸 Загрузить фото")

uploaded_file = st.file_uploader(
    "Выберите изображение",
    type=["jpg", "jpeg", "png"],
    help="Сфотографируйте дерево или выберите из галереи",
    label_visibility="collapsed",
)

# Compact settings in expander
with st.expander("⚙️ Настройки"):
    col1, col2 = st.columns(2)
    with col1:
        tree_conf = st.slider(
            "Деревья", 0.0, 1.0, 0.25, help="Уверенность обнаружения деревьев"
        )
    with col2:
        defect_conf = st.slider(
            "Дефекты", 0.0, 1.0, 0.25, help="Уверенность обнаружения дефектов"
        )

if uploaded_file is not None:
    # Show loading spinner
    with st.spinner("🔍 Анализ изображения..."):
        # Load image
        image = Image.open(uploaded_file)
        img_array = np.array(image)

        # Run detection
        results = detector.detect(
            img_array, tree_conf_threshold=tree_conf, defect_conf_threshold=defect_conf
        )

        # Display results
        annotated_img = results["annotated_image"]

        # Show image (full width on mobile)
        st.image(
            annotated_img, use_container_width=True, caption="Результаты обнаружения"
        )

        # Compact metrics
        st.markdown("### 📊 Результаты")

        col1, col2, col3 = st.columns(3)
        col1.metric("Деревья", results["tree_count"])
        col2.metric("Дефекты", results["defect_count"])
        col3.metric("Всего", results["tree_count"] + results["defect_count"])

        # Detection details in expandable section
        if results["detections"]:
            with st.expander(f"🔍 Детали ({len(results['detections'])} обнаружений)"):
                for i, det in enumerate(results["detections"], 1):
                    conf_percent = det["confidence"] * 100
                    st.markdown(
                        f"**{i}.** {det['class_name']} "
                        f"({det['type']}) - {conf_percent:.1f}%"
                    )

        # Download button
        # Convert to bytes for download
        img_pil = Image.fromarray(annotated_img)
        buf = io.BytesIO()
        img_pil.save(buf, format="JPEG", quality=95)
        buf.seek(0)

        st.download_button(
            label="📥 Скачать результат",
            data=buf,
            file_name=f"detection_{uploaded_file.name}",
            mime="image/jpeg",
            use_container_width=True,
        )

        # Share button hint
        st.info(
            '💡 Используйте кнопку "Поделиться" в браузере для отправки результатов'
        )

else:
    # Instructions when no image
    st.info(
        """
    👆 Загрузите фотографию дерева
    
    **Советы:**
    - Используйте камеру телефона
    - Фотографируйте с расстояния 2-5 метров
    - Убедитесь в хорошем освещении
    - Дерево должно быть в центре кадра
    """
    )

# Installation hint
st.markdown("---")
with st.expander("📱 Установить как приложение"):
    st.markdown(
        """
    ### Установка на телефон:
    
    **Android (Chrome):**
    1. Нажмите меню (⋮)
    2. Выберите "Установить приложение"
    3. Нажмите "Установить"
    
    **iOS (Safari):**
    1. Нажмите кнопку "Поделиться"
    2. Выберите "На экран Домой"
    3. Нажмите "Добавить"
    
    После установки приложение будет доступно с главного экрана!
    """
    )
