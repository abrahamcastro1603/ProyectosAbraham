# English Speaking Tutor (Versión A1-B1) - Gemini 3.5 Flash Lite

Aplicación de escritorio desarrollada en Python con **Tkinter**, **Google Gemini 3.5 Flash Lite**, **Edge-TTS** y persistencia en **SQLite**. Esta variante está optimizada profesionalmente para cubrir los niveles CEFR de **A1 hasta B1** (Principiante a Intermedio).

---

## 🚀 Características Principales
- **IA de Vanguardia:** Integración oficial con `gemini-3.5-flash-lite` para razonamiento y retroalimentación gramatical inteligente.
- **Variante A1-B1:** Diseñada específicamente para estudiantes que inician o consolidan sus bases en inglés.
- **Voces Nativas Neuronales:** Síntesis de voz en tiempo real con `edge-tts` (acentos US y UK con control de velocidad).
- **Persistencia SQLite:** Almacenamiento automático de cada sesión y corrección en `tutor_ingles.db`.
- **Interfaz Responsiva:** Adaptable a cualquier resolución de pantalla con desplazamiento vertical integrado.

---

## 📦 Requisitos de Instalación

1. Clona o descarga este repositorio.
2. Instala las dependencias necesarias mediante pip:
   ```bash
   pip install -r requirements.txt
   ```
   *(Nota: Asegúrate de tener PyAudio instalado para la captura de micrófono).*

---

## ⚙️ Configuración

1. Crea un archivo llamado `.env` en la raíz del proyecto (puedes basarte en `.env.example`).
2. Agrega tu clave de API de Google AI Studio:
   ```env
   GEMINI_API_KEY=AIzaSyTuClaveRealDeAIStudioAqui
   ```

---

## ▶️ Ejecución

```bash
python tutor_ingles.py
```

---

## 📄 Licencia

Este proyecto está licenciado bajo los términos de la **Apache License 2.0**. 
Creador original: **JESUS ABRAHAM CASTRO TORRES**. Consulta el archivo `LICENSE` para más detalles.
