#!/usr/bin/env python3
"""
Веб-приложение для обнаружения деревьев - Главная точка входа
Двухэтапное обнаружение: Деревья + Дефекты
"""

import streamlit as st
from PIL import Image
import cv2
import numpy as np
from pathlib import Path
import tempfile
import json
import torch

# Fix for PyTorch 2.6+ weights_only security change
try:
    from ultralytics.nn.tasks import DetectionModel

    torch.serialization.add_safe_globals([DetectionModel])
except Exception:
    pass  # Older PyTorch versions don't have this

from two_stage_detection import TwoStageDetector

# Конфигурация страницы
st.set_page_config(
    page_title="Обнаружение деревьев и дефектов", page_icon="🌲", layout="wide"
)


@st.cache_resource
def load_detector(tree_model_path, defect_model_path):
    """Загрузить детектор с кэшированием"""
    try:
        detector = TwoStageDetector(tree_model_path, defect_model_path)
        return detector, None
    except Exception as e:
        return None, str(e)


def find_models():
    """Найти обученные модели"""
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
    defect_model_alt = (
        script_dir
        / "runs"
        / "defects"
        / "tree_defects_detection"
        / "weights"
        / "best.pt"
    )

    # Use alternative if primary doesn't exist
    if not defect_model.exists() and defect_model_alt.exists():
        defect_model = defect_model_alt

    return (
        str(tree_model) if tree_model.exists() else None,
        str(defect_model) if defect_model.exists() else None,
    )


def format_results_html(results):
    """Форматировать результаты в HTML для лучшего отображения"""
    html = "<div style='font-family: monospace;'>"

    for tree in results["trees"]:
        # Заголовок дерева
        tree_color = "#2ecc71" if not tree["defects"] else "#e74c3c"
        html += f"<div style='margin-bottom: 20px; padding: 15px; border-left: 4px solid {tree_color}; background-color: #f8f9fa;'>"
        html += (
            f"<h4 style='margin: 0 0 10px 0; color: {tree_color};'>🌲 {tree['id']}</h4>"
        )
        html += f"<p style='margin: 5px 0;'><b>Тип:</b> {tree['type']}</p>"
        html += f"<p style='margin: 5px 0;'><b>Уверенность:</b> {tree['confidence']:.1%}</p>"

        if "type_confidence" in tree:
            html += f"<p style='margin: 5px 0;'><b>Уверенность типа:</b> {tree['type_confidence']:.1%}</p>"

        if tree["defects"]:
            html += f"<p style='margin: 10px 0 5px 0;'><b>⚠️ Дефекты ({len(tree['defects'])}):</b></p>"
            html += "<ul style='margin: 0; padding-left: 20px;'>"
            for defect in tree["defects"]:
                html += f"<li>{defect['type']} (уверенность: {defect['confidence']:.1%})</li>"
            html += "</ul>"
        else:
            html += "<p style='margin: 10px 0 0 0; color: #27ae60;'>✓ Дефекты не обнаружены</p>"

        html += "</div>"

    if results["unmatched_defects"]:
        html += "<div style='margin-top: 20px; padding: 15px; border-left: 4px solid #f39c12; background-color: #fef5e7;'>"
        html += f"<h4 style='margin: 0 0 10px 0; color: #f39c12;'>⚠️ Несопоставленные дефекты ({len(results['unmatched_defects'])})</h4>"
        html += "<ul style='margin: 0; padding-left: 20px;'>"
        for defect in results["unmatched_defects"]:
            html += (
                f"<li>{defect['class']} (уверенность: {defect['confidence']:.1%})</li>"
            )
        html += "</ul>"
        html += "</div>"

    html += "</div>"
    return html


def main():
    # Заголовок
    st.title("🌲 Система обнаружения деревьев и дефектов")
    st.markdown(
        "Двухэтапное обнаружение: сначала обнаруживаются деревья, затем идентифицируются дефекты в каждом дереве"
    )
    st.markdown("---")

    # Боковая панель
    with st.sidebar:
        st.header("⚙️ Конфигурация")

        # Статус моделей
        st.subheader("Модели")
        tree_model, defect_model = find_models()

        if tree_model and defect_model:
            st.success("✅ Модель деревьев")
            st.success("✅ Модель дефектов")
            detector, error = load_detector(tree_model, defect_model)
            if error:
                st.error(f"Ошибка загрузки моделей: {error}")
                detector = None
        else:
            if not tree_model:
                st.error("❌ Модель деревьев не найдена")
                st.info("Обучить: `python train_cpu.py`")
            if not defect_model:
                st.error("❌ Модель дефектов не найдена")
                st.info("Обучить: `python train_defects.py`")
            detector = None

        st.markdown("---")

        # Настройки обнаружения
        st.subheader("Настройки обнаружения")
        tree_conf = st.slider("Уверенность для деревьев", 0.05, 0.95, 0.25, 0.05)
        defect_conf = st.slider("Уверенность для дефектов", 0.05, 0.95, 0.20, 0.05)

        st.markdown("---")

        # Информация
        st.subheader("ℹ️ Классы обнаружения")
        with st.expander("Типы деревьев (2)"):
            st.markdown(
                """
            - Куст
            - Дуб
            """
            )

        with st.expander("Типы дефектов (12)"):
            st.markdown(
                """
            - Трещина, Мёртвый куст, Мёртвое дерево
            - Сухая крона, Наклонённое дерево
            - Отмеченное дерево, Товарное дерево
            - Отмеченное дерево (вариант)
            - Гниль, Повреждение ствола
            - Гниль ствола, Дупло
            """
            )

    # Основной контент
    if detector is None:
        st.error("❌ Модели недоступны. Пожалуйста, сначала обучите обе модели.")

        col1, col2 = st.columns(2)
        with col1:
            st.code("python train_cpu.py", language="bash")
            st.caption("Обучить модель обнаружения деревьев")
        with col2:
            st.code("python train_defects.py", language="bash")
            st.caption("Обучить модель обнаружения дефектов")
        return

    # Загрузчик файлов
    st.header("📁 Загрузить изображение")
    uploaded_file = st.file_uploader(
        "Выберите файл изображения",
        type=["jpg", "jpeg", "png"],
        help="Выберите изображение для обнаружения деревьев и их дефектов",
    )

    if uploaded_file is not None:
        # Загрузить изображение
        image = Image.open(uploaded_file)

        # Временно сохранить
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            image.save(tmp_file.name)
            tmp_path = tmp_file.name

        # Отобразить оригинальное изображение
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("📷 Исходное изображение")
            st.image(image, width=600)

        with col2:
            st.subheader("🎯 Результаты обнаружения")

            if st.button(
                "🚀 Запустить обнаружение", type="primary", use_container_width=True
            ):
                with st.spinner("Выполняется двухэтапное обнаружение..."):
                    try:
                        # Выполнить обнаружение
                        results = detector.detect(tmp_path, tree_conf, defect_conf)

                        # Создать визуализацию
                        vis_img = detector.visualize(tmp_path, results)
                        vis_img_rgb = cv2.cvtColor(vis_img, cv2.COLOR_BGR2RGB)

                        # Отобразить
                        st.image(vis_img_rgb, width=600)

                        # Сохранить в состояние сессии
                        st.session_state["results"] = results
                        st.session_state["vis_img"] = vis_img

                    except Exception as e:
                        st.error(f"Ошибка при обнаружении: {str(e)}")

        # Показать результаты, если доступны
        if "results" in st.session_state:
            results = st.session_state["results"]

            st.markdown("---")
            st.subheader("📊 Сводка обнаружения")

            # Сводные метрики
            col_a, col_b, col_c, col_d = st.columns(4)

            with col_a:
                st.metric("Всего деревьев", results["total_trees"])

            with col_b:
                st.metric("Всего дефектов", results["total_defects"])

            with col_c:
                healthy_trees = sum(1 for t in results["trees"] if not t["defects"])
                st.metric("Здоровых деревьев", healthy_trees)

            with col_d:
                unhealthy_trees = results["total_trees"] - healthy_trees
                st.metric("Деревьев с дефектами", unhealthy_trees)

            # Детальные результаты
            st.markdown("---")
            st.subheader("📋 Подробные результаты")

            # Отобразить форматированные результаты
            html_results = format_results_html(results)
            st.markdown(html_results, unsafe_allow_html=True)

            # Опции загрузки
            st.markdown("---")
            st.subheader("💾 Скачать результаты")

            col_dl1, col_dl2 = st.columns(2)

            with col_dl1:
                # Скачать изображение
                if "vis_img" in st.session_state:
                    vis_img = st.session_state["vis_img"]
                    is_success, buffer = cv2.imencode(".jpg", vis_img)
                    if is_success:
                        st.download_button(
                            label="Скачать размеченное изображение",
                            data=buffer.tobytes(),
                            file_name=f"detected_{uploaded_file.name}",
                            mime="image/jpeg",
                            use_container_width=True,
                        )

            with col_dl2:
                # Скачать JSON
                json_str = json.dumps(results, indent=2, ensure_ascii=False)
                st.download_button(
                    label="Скачать результаты JSON",
                    data=json_str,
                    file_name=f"results_{Path(uploaded_file.name).stem}.json",
                    mime="application/json",
                    use_container_width=True,
                )

        # Очистка
        try:
            Path(tmp_path).unlink()
        except:
            pass

    else:
        st.info("👆 Пожалуйста, загрузите изображение для начала работы")


if __name__ == "__main__":
    main()
