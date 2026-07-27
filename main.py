
















#Entrada Usuario/Historial Cadenas
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
 
 
# Ruta al ejecutable compilado en C++.
#RUTA_EJECUTABLE = os.path.join("Automate", "automate.cpp")
RUTA_EJECUTABLE = r"C:\Users\rodri\OneDrive\Documentos\KRAVNIKA\Automate\output.exe"
print(RUTA_EJECUTABLE)

ENVIAR_COMO_ARGUMENTO = True #AL trabajar con codigo binario/ cambira por std::cin >> cadena y se cambia a False
 
#Ajustar textpo segun la modificación compañero
TEXTO_VALIDA = "valida"
TEXTO_INVALIDA = "invalida"
 
 
def ejecutar_automata(cadena: str) -> tuple[bool, str]:
    try:
        if ENVIAR_COMO_ARGUMENTO:
            resultado = subprocess.run(
                [RUTA_EJECUTABLE, cadena],
                capture_output=True,
                text=True,
                timeout=5,
            )
        else:
            resultado = subprocess.run(
                [RUTA_EJECUTABLE],
                input=cadena,
                capture_output=True,
                text=True,
                timeout=5,
            )
 
        salida = (resultado.stdout or "").strip()
        salida_lower = salida.lower()
 
        if TEXTO_VALIDA.lower() in salida_lower:
            return True, salida
        elif TEXTO_INVALIDA.lower() in salida_lower:
            return False, salida
        else:
            # Si no se reconoce el texto imprimimos el desconocimiento del mismo
            return False, f"(salida no reconocida) {salida}"
 
    except FileNotFoundError:
        return False, (
            f"No se encontró el ejecutable en '{RUTA_EJECUTABLE}'. "
            "Revisa la ruta y que el programa esté compilado."
        )
    except subprocess.TimeoutExpired:
        return False, "El programa tardó demasiado en responder."
    except Exception as e:
        return False, f"Error inesperado: {e}"
 
 
print(ejecutar_automata("Hola mundo"))
 
class AplicacionAutomata(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Validador de Cadenas - Autómata KRAVNIKA")
        self.geometry("520x480")
        self.resizable(False, False)
 
        self.historial = []  # lista de (cadena, resultado_texto)
 
        self._construir_widgets()
 
    def _construir_widgets(self):
        padding = {"padx": 12, "pady": 8}
 
        # Entrada Us.
        frame_entrada = ttk.Frame(self)
        frame_entrada.pack(fill="x", **padding)
 
        ttk.Label(frame_entrada, text="Cadena a validar:").pack(anchor="w")
 
        self.entry_cadena = ttk.Entry(frame_entrada, font=("Consolas", 12))
        self.entry_cadena.pack(fill="x", pady=(4, 8))
        self.entry_cadena.bind("<Return>", lambda event: self.validar_cadena())
 
        self.boton_validar = ttk.Button(
            frame_entrada, text="Validar", command=self.validar_cadena
        )
        self.boton_validar.pack(anchor="e")
