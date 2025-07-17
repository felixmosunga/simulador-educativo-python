import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class SimuladorEducativo:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Educativo")
        self.root.geometry("800x700")
        
        # Reactivos
        self.reactivos = [
            {
                "pregunta": "Un virus se reproduce de acuerdo con la siguiente tabulación. ¿Qué cantidad de virus habrá el noveno día?",
                "opciones": ["2 880", "1 944", "52 488"],
                "respuesta_correcta": 0,
                "area": "Pensamiento Matemático",
                "imagen": "imagenes/tabla_virus.png"
            }
        ]
        
        self.pregunta_actual = 0
        self.crear_interfaz()
        self.mostrar_pregunta()
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(main_frame, text="SIMULADOR EDUCATIVO", font=("Arial", 16, "bold"))
        titulo.pack(pady=(0, 10))
        
        # Área de la imagen
        self.imagen_label = ttk.Label(main_frame, text="")
        self.imagen_label.pack(pady=10)
        
        # Área de la pregunta
        self.pregunta_label = ttk.Label(main_frame, text="", wraplength=700, font=("Arial", 12), justify=tk.LEFT)
        self.pregunta_label.pack(pady=15)
        
        # Variable para la respuesta seleccionada
        self.respuesta_var = tk.StringVar()
        
        # Frame para opciones
        opciones_frame = ttk.LabelFrame(main_frame, text="Selecciona tu respuesta:", padding="10")
        opciones_frame.pack(pady=15, fill=tk.X)
        
        # Botones de opción
        self.radio_buttons = []
        for i in range(3):
            rb = ttk.Radiobutton(opciones_frame, text="", variable=self.respuesta_var, value=str(i))
            rb.pack(anchor=tk.W, pady=8)
            self.radio_buttons.append(rb)
        
        # Frame para botones
        botones_frame = ttk.Frame(main_frame)
        botones_frame.pack(pady=20)
        
        # Botón de responder
        self.btn_responder = ttk.Button(botones_frame, text="Verificar Respuesta", command=self.verificar_respuesta)
        self.btn_responder.pack(side=tk.LEFT, padx=10)
        
        # Botón de limpiar
        self.btn_limpiar = ttk.Button(botones_frame, text="Limpiar", command=self.limpiar_respuesta)
        self.btn_limpiar.pack(side=tk.LEFT, padx=10)
        
        # Área de resultado
        self.resultado_label = ttk.Label(main_frame, text="", font=("Arial", 12, "bold"))
        self.resultado_label.pack(pady=15)
    
    def cargar_imagen(self, ruta_imagen):
        """Carga y redimensiona una imagen"""
        try:
            if os.path.exists(ruta_imagen):
                # Cargar imagen
                imagen = Image.open(ruta_imagen)
                # Redimensionar si es necesario
                imagen = imagen.resize((400, 200), Image.Resampling.LANCZOS)
                # Convertir para tkinter
                imagen_tk = ImageTk.PhotoImage(imagen)
                return imagen_tk
            else:
                return None
        except Exception as e:
            print(f"Error al cargar imagen: {e}")
            return None
    
    def mostrar_pregunta(self):
        if self.pregunta_actual < len(self.reactivos):
            reactivo = self.reactivos[self.pregunta_actual]
            
            # Mostrar imagen si existe
            if "imagen" in reactivo:
                imagen_tk = self.cargar_imagen(reactivo["imagen"])
                if imagen_tk:
                    self.imagen_label.configure(image=imagen_tk, text="")
                    self.imagen_label.image = imagen_tk  # Mantener referencia
                else:
                    self.imagen_label.configure(image="", text="[Imagen: tabla_virus.png no encontrada]", foreground="red")
            else:
                self.imagen_label.configure(image="", text="")
            
            # Mostrar pregunta
            self.pregunta_label.configure(text=reactivo["pregunta"])
            
            # Mostrar opciones
            for i, opcion in enumerate(reactivo["opciones"]):
                self.radio_buttons[i].configure(text=f"{chr(65+i)}) {opcion}")
            
            # Limpiar selección y resultado
            self.respuesta_var.set("")
            self.resultado_label.configure(text="")
    
    def verificar_respuesta(self):
        if self.respuesta_var.get():
            reactivo = self.reactivos[self.pregunta_actual]
            respuesta_usuario = int(self.respuesta_var.get())
            
            if respuesta_usuario == reactivo["respuesta_correcta"]:
                self.resultado_label.configure(text="¡CORRECTO! 🎉\nLa respuesta es A) 2,880 virus", foreground="green")
            else:
                correcta = chr(65 + reactivo["respuesta_correcta"])
                self.resultado_label.configure(text=f"❌ Incorrecto\nLa respuesta correcta es {correcta}) 2,880 virus\n\nExplicación: El virus se multiplica por 3 cada día.", foreground="red")
        else:
            self.resultado_label.configure(text="⚠️ Por favor, selecciona una opción", foreground="orange")
    
    def limpiar_respuesta(self):
        self.respuesta_var.set("")
        self.resultado_label.configure(text="")

# Ejecutar el simulador
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = SimuladorEducativo(root)
        root.mainloop()
    except Exception as e:
        print(f"Error: {e}")
        input("Presiona Enter para cerrar...")