import asyncio
import os
import sqlite3
import threading
import time
import uuid
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    import speech_recognition as sr
except ImportError:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error de Dependencia", "Falta la librería 'SpeechRecognition'. Instálala con: pip install SpeechRecognition")
    exit(1)

try:
    import edge_tts
    import pygame
except ImportError:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error de Dependencia", "Faltan librerías de audio ('edge-tts' o 'pygame'). Instálalas con: pip install edge-tts pygame")
    exit(1)

from pydantic import BaseModel
from google import genai
from google.genai import types

DB_PATH = "tutor_ingles.db"

def inicializar_bd():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sesiones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                acento TEXT,
                nivel TEXT,
                usuario TEXT,
                correccion TEXT,
                tutor TEXT
            )
        ''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error inicializando BD: {e}")

def guardar_transaccion(acento, nivel, usuario, correccion, tutor):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO sesiones (acento, nivel, usuario, correccion, tutor) VALUES (?, ?, ?, ?, ?)",
            (acento, nivel, usuario, correccion, tutor)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error guardando en BD: {e}")

class RespuestaTutor(BaseModel):
    correccion_espanol: str
    respuesta_ingles: str

class AplicacionTutorWindows:
    def __init__(self, root):
        self.root = root
        self.root.title("English Speaking Tutor - Gemini 3.5 Flash Lite")
        self.root.geometry("750x650")
        self.root.minsize(600, 500)

        inicializar_bd()

        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            messagebox.showwarning(
                "Advertencia de API Key",
                "No se detectó 'GEMINI_API_KEY' en el entorno ni en el archivo .env."
            )
            self.client = None
        else:
            try:
                self.client = genai.Client(api_key=api_key)
            except Exception as e:
                self.client = None
                print(f"Error al inicializar cliente genai: {e}")

        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")

        self.ocupado = False
        self.historial = []
        self.ultimo_texto_tutor = ""

        try:
            pygame.mixer.init()
        except Exception as e:
            print(f"Advertencia al inicializar Pygame mixer: {e}")

        self.acentos = {
            "Estados Unidos (US) - Voz Femenina (Jenny)": {"stt": "en-US", "tts": "en-US-JennyNeural"},
            "Estados Unidos (US) - Voz Masculina (Christopher)": {"stt": "en-US", "tts": "en-US-ChristopherNeural"},
            "Reino Unido (UK) - Voz Femenina (Sonia)": {"stt": "en-GB", "tts": "en-GB-SoniaNeural"},
            "Reino Unido (UK) - Voz Masculina (Ryan)": {"stt": "en-GB", "tts": "en-GB-RyanNeural"},
        }

        # REGLA 2: Variante recortada topada de A1 hasta B1
        self.niveles = [
            "A1 - Principiante",
            "A2 - Elemental",
            "B1 - Intermedio"
        ]

        self.construir_interfaz()

    def construir_interfaz(self):
        main_canvas = tk.Canvas(self.root, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        
        self.main_frame = ttk.Frame(main_canvas, padding="10")
        
        self.main_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        canvas_window = main_canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        
        def on_canvas_configure(event):
            main_canvas.itemconfig(canvas_window, width=event.width)
        main_canvas.bind("<Configure>", on_canvas_configure)

        main_canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        panel_config = ttk.LabelFrame(self.main_frame, text="Configuración Avanzada de Tutoría (Niveles A1-B1)", padding="10")
        panel_config.pack(fill=tk.X, pady=(0, 8), expand=False)
        panel_config.columnconfigure(1, weight=1)

        ttk.Label(panel_config, text="Acento nativo:", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 10), pady=4)
        self.combo_acento = ttk.Combobox(
            panel_config,
            values=list(self.acentos.keys()),
            state="readonly",
            font=("Segoe UI", 9)
        )
        self.combo_acento.current(0)
        self.combo_acento.grid(row=0, column=1, sticky="ew", pady=4)

        ttk.Label(panel_config, text="Nivel CEFR:", font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=4)
        self.combo_nivel = ttk.Combobox(
            panel_config,
            values=self.niveles,
            state="readonly",
            font=("Segoe UI", 9)
        )
        self.combo_nivel.current(2)  # Por defecto B1
        self.combo_nivel.grid(row=1, column=1, sticky="ew", pady=4)

        ttk.Label(panel_config, text="Velocidad TTS:", font=("Segoe UI", 9, "bold")).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=4)
        
        frame_vel_inner = ttk.Frame(panel_config)
        frame_vel_inner.grid(row=2, column=1, sticky="ew", pady=4)
        frame_vel_inner.columnconfigure(0, weight=1)

        self.slider_velocidad = ttk.Scale(frame_vel_inner, from_=-50, to=50, value=0, orient=tk.HORIZONTAL)
        self.slider_velocidad.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        self.lbl_vel_val = ttk.Label(frame_vel_inner, text="0%", font=("Segoe UI", 9), width=6)
        self.lbl_vel_val.grid(row=0, column=1, sticky="e")
        self.slider_velocidad.configure(command=self.actualizar_etiqueta_velocidad)

        panel_chat = ttk.LabelFrame(self.main_frame, text="Sesión de Práctica (Guardada en SQLite)", padding="8")
        panel_chat.pack(fill=tk.BOTH, expand=True, pady=(0, 8))

        self.area_chat = scrolledtext.ScrolledText(
            panel_chat,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            state=tk.DISABLED,
            bg="#ffffff",
            relief=tk.FLAT,
            height=10,
            padx=8,
            pady=8
        )
        self.area_chat.pack(fill=tk.BOTH, expand=True)

        self.area_chat.tag_config("usuario", foreground="#005a9e", font=("Segoe UI", 10, "bold"))
        self.area_chat.tag_config("correccion", foreground="#a4262c", font=("Segoe UI", 10, "italic"))
        self.area_chat.tag_config("tutor", foreground="#107c10", font=("Segoe UI", 10, "bold"))
        self.area_chat.tag_config("info", foreground="#605e5c", font=("Segoe UI", 9))

        frame_estado = ttk.Frame(self.main_frame)
        frame_estado.pack(fill=tk.X, pady=(0, 8))

        self.lbl_estado = ttk.Label(
            frame_estado,
            text="Listo. Presiona 'Grabar mi voz' para comenzar a hablar.",
            font=("Segoe UI", 9, "bold"),
            foreground="#005a9e"
        )
        self.lbl_estado.pack(side=tk.LEFT)

        self.barra_progreso = ttk.Progressbar(frame_estado, mode="indeterminate", length=120)
        self.barra_progreso.pack(side=tk.RIGHT)

        panel_botones = ttk.Frame(self.main_frame)
        panel_botones.pack(fill=tk.X, pady=(0, 4))
        panel_botones.columnconfigure(0, weight=3)
        panel_botones.columnconfigure(1, weight=1)
        panel_botones.columnconfigure(2, weight=1)

        self.btn_grabar = ttk.Button(
            panel_botones,
            text="🎤 Grabar mi voz (Hablar en inglés)",
            command=self.iniciar_turno_grabacion
        )
        self.btn_grabar.grid(row=0, column=0, sticky="ew", ipady=6, padx=(0, 4))

        self.btn_repetir = ttk.Button(
            panel_botones,
            text="🔊 Repetir audio",
            command=self.repetir_ultimo_audio,
            state=tk.DISABLED
        )
        self.btn_repetir.grid(row=0, column=1, sticky="ew", ipady=6, padx=(0, 4))

        self.btn_limpiar = ttk.Button(
            panel_botones,
            text="🗑️ Limpiar",
            command=self.limpiar_conversacion
        )
        self.btn_limpiar.grid(row=0, column=2, sticky="ew", ipady=6)

        self.insertar_log("Sistema: ", "Bienvenido. Configura tu acento, nivel A1-B1 y velocidad, luego presiona hablar.", "info")

    def actualizar_etiqueta_velocidad(self, val):
        val_int = int(float(val))
        signo = "+" if val_int > 0 else ""
        self.lbl_vel_val.config(text=f"{signo}{val_int}%")

    def obtener_string_velocidad(self) -> str:
        val_int = int(float(self.slider_velocidad.get()))
        if val_int == 0:
            return "+0%"
        signo = "+" if val_int > 0 else ""
        return f"{signo}{val_int}%"

    def cambiar_estado_ui(self, bloqueado: bool, mensaje: str, color: str = "#005a9e"):
        def _actualizar():
            self.ocupado = bloqueado
            self.lbl_estado.config(text=mensaje, foreground=color)
            if bloqueado:
                self.btn_grabar.config(state=tk.DISABLED)
                self.btn_repetir.config(state=tk.DISABLED)
                self.combo_acento.config(state=tk.DISABLED)
                self.combo_nivel.config(state=tk.DISABLED)
                self.slider_velocidad.config(state=tk.DISABLED)
                self.barra_progreso.start(12)
            else:
                self.btn_grabar.config(state=tk.NORMAL)
                self.combo_acento.config(state="readonly")
                self.combo_nivel.config(state="readonly")
                self.slider_velocidad.config(state=tk.NORMAL)
                if self.ultimo_texto_tutor:
                    self.btn_repetir.config(state=tk.NORMAL)
                self.barra_progreso.stop()
        self.root.after(0, _actualizar)

    def insertar_log(self, titulo: str, contenido: str, tag: str):
        def _escribir():
            self.area_chat.config(state=tk.NORMAL)
            self.area_chat.insert(tk.END, titulo, tag)
            self.area_chat.insert(tk.END, f"{contenido}\n\n")
            self.area_chat.see(tk.END)
            self.area_chat.config(state=tk.DISABLED)
        self.root.after(0, _escribir)

    def limpiar_conversacion(self):
        if self.ocupado:
            return
        self.historial.clear()
        self.ultimo_texto_tutor = ""
        self.btn_repetir.config(state=tk.DISABLED)
        self.area_chat.config(state=tk.NORMAL)
        self.area_chat.delete("1.0", tk.END)
        self.area_chat.config(state=tk.DISABLED)
        self.insertar_log("Sistema: ", "Conversación reiniciada.", "info")

    def iniciar_turno_grabacion(self):
        if self.ocupado:
            return
        
        api_key_actual = os.environ.get("GEMINI_API_KEY")
        if not api_key_actual:
            messagebox.showerror(
                "Falta API Key",
                "No se detectó la variable GEMINI_API_KEY."
            )
            return

        threading.Thread(target=self.flujo_completo_turno, daemon=True).start()

    def flujo_completo_turno(self):
        seleccion_acento = self.combo_acento.get()
        config_acento = self.acentos[seleccion_acento]
        nivel_actual = self.combo_nivel.get()

        self.cambiar_estado_ui(True, "Calibrando micrófono (1 seg)...", "#d83b01")
        recognizer = sr.Recognizer()
        recognizer.pause_threshold = 1.5

        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.8)
                self.cambiar_estado_ui(True, "🟢 ¡Escuchando! Habla en inglés ahora...", "#107c10")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=30)
        except sr.WaitTimeoutError:
            self.cambiar_estado_ui(False, "No se detectó voz. Intenta presionar el botón de nuevo.", "#a4262c")
            return
        except Exception as e:
            self.cambiar_estado_ui(False, f"Error de micrófono (verifica PyAudio): {e}", "#a4262c")
            return

        self.cambiar_estado_ui(True, "Convirtiendo voz a texto...", "#005a9e")
        try:
            texto_usuario = recognizer.recognize_google(audio, language=config_acento["stt"])
        except sr.UnknownValueError:
            self.cambiar_estado_ui(False, "No se pudo entender el audio. Intenta hablar más claro.", "#a4262c")
            return
        except sr.RequestError as e:
            self.cambiar_estado_ui(False, f"Error de red en reconocimiento de voz: {e}", "#a4262c")
            return

        self.insertar_log("🗣️ Tú dijiste: ", texto_usuario, "usuario")

        self.cambiar_estado_ui(True, "🧠 Gemini 3.5 Flash Lite razonando...", "#5c2d91")
        try:
            respuesta = self.consultar_gemini(texto_usuario, seleccion_acento, nivel_actual)
        except Exception as e:
            self.insertar_log("Error de API Gemini: ", str(e), "correccion")
            self.cambiar_estado_ui(False, "Error al consultar Gemini. Revisa tu API Key.", "#a4262c")
            return

        self.insertar_log("📝 Corrección: ", respuesta.correccion_espanol, "correccion")
        self.insertar_log("🤖 Tutor: ", respuesta.respuesta_ingles, "tutor")
        self.ultimo_texto_tutor = respuesta.respuesta_ingles

        guardar_transaccion(seleccion_acento, nivel_actual, texto_usuario, respuesta.correccion_espanol, respuesta.respuesta_ingles)

        self.cambiar_estado_ui(True, "🔊 Reproduciendo respuesta del tutor...", "#005a9e")
        try:
            asyncio.run(self.reproducir_voz_local(respuesta.respuesta_ingles, config_acento["tts"]))
        except Exception as e:
            print(f"Error reproduciendo TTS: {e}")

        self.cambiar_estado_ui(False, "Listo. Presiona 'Grabar mi voz' para responder.", "#005a9e")

    def consultar_gemini(self, texto_usuario: str, nombre_acento: str, nivel: str) -> RespuestaTutor:
        self.historial.append(f"Estudiante: {texto_usuario}")
        variante = "estadounidense (US)" if "US" in nombre_acento else "británico (UK)"
        instrucciones = (
            f"Eres un profesor nativo de inglés {variante} paciente y amigable. "
            f"El estudiante tiene un nivel CEFR de '{nivel}' (variante inicial A1-B1). Adapta tu vocabulario, modismos y complejidad gramatical estrictamente a este nivel básico/intermedio. "
            "Analiza la frase del estudiante. "
            "1) En 'correccion_espanol': señala errores de gramática o vocabulario de forma breve y clara en español, "
            "sugiriendo cómo lo diría un nativo acorde a su nivel. Si la frase es correcta, felicítalo brevemente. "
            "2) En 'respuesta_ingles': responde de manera natural en inglés manteniendo la conversación y hazle una pregunta sencilla acorde a su nivel."
        )
        
        api_key = os.environ.get("GEMINI_API_KEY")
        client_instance = genai.Client(api_key=api_key)
        
        # REGLA INNEGOCIABLE: Modelo estricto gemini-3.5-flash-lite con reintentos para 503
        intentos_maximos = 3
        for intento in range(intentos_maximos):
            try:
                response = client_instance.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents="\n".join(self.historial),
                    config=types.GenerateContentConfig(
                        system_instruction=instrucciones,
                        response_mime_type="application/json",
                        response_schema=RespuestaTutor,
                        temperature=0.7
                    )
                )
                datos = RespuestaTutor.model_validate_json(response.text)
                self.historial.append(f"Tutor: {datos.respuesta_ingles}")
                return datos
            except Exception as e:
                if "503" in str(e) and intento < intentos_maximos - 1:
                    time.sleep(2 * (intento + 1))
                    continue
                raise e

    async def reproducir_voz_local(self, texto: str, voz_tts: str):
        temp_dir = os.environ.get("TEMP", ".")
        archivo_mp3 = os.path.join(temp_dir, f"tutor_voz_{uuid.uuid4().hex}.mp3")
        rate_str = self.obtener_string_velocidad()
        
        comunicador = edge_tts.Communicate(texto, voz_tts, rate=rate_str)
        await comunicador.save(archivo_mp3)
        
        try:
            pygame.mixer.music.load(archivo_mp3)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            pygame.mixer.music.stop()
        except Exception as e:
            print(f"Error en mixer pygame: {e}")
        finally:
            try:
                pygame.mixer.music.unload()
            except AttributeError:
                try:
                    pygame.mixer.music.load(os.path.join(temp_dir, "dummy_reset.mp3"))
                except Exception:
                    pass
            except Exception:
                pass

        for _ in range(3):
            try:
                if os.path.exists(archivo_mp3):
                    os.remove(archivo_mp3)
                break
            except PermissionError:
                time.sleep(0.2)
            except Exception:
                break

    def repetir_ultimo_audio(self):
        if self.ocupado or not self.ultimo_texto_tutor:
            return
        seleccion = self.combo_acento.get()
        voz_tts = self.acentos[seleccion]["tts"]
        
        def _repetir():
            self.cambiar_estado_ui(True, "🔊 Repitiendo último mensaje...", "#005a9e")
            try:
                asyncio.run(self.reproducir_voz_local(self.ultimo_texto_tutor, voz_tts))
            except Exception as e:
                print(f"Error repitiendo audio: {e}")
            self.cambiar_estado_ui(False, "Listo. Presiona 'Grabar mi voz' para responder.", "#005a9e")
            
        threading.Thread(target=_repetir, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionTutorWindows(root)
    root.mainloop()
