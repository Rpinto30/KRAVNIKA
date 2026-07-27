#Entrada Usuario/Historial Cadenas
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os


# Ruta al ejecutable compilado
RUTA_EJECUTABLE = os.path.join("..", "Automate", "automate")

# Palabras que el programa de C++ imprime para indicar el resultado.
# Ajustarlos como el automata lo indique
TEXTO_VALIDA = "valida"
TEXTO_INVALIDA = "invalida"


def ejecutar_automata(cadena: str) -> tuple[bool, str]:
    """
    Ejecuta el programa de C++ de forma INTERACTIVA: lo arranca, le manda
    la cadena por stdin (como si la tecleraras en consola) y espera a que
    termine para leer lo que imprimió (stdout).
    Devuelve (es_valida, mensaje_completo_del_programa).
    """
    try:
        proceso = subprocess.Popen(
            [RUTA_EJECUTABLE],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # communicate() envía la cadena (+ salto de línea, como un Enter)
        # y espera a que el programa termine
        stdout_salida, stderr_salida = proceso.communicate(
            input=cadena + "\n", timeout=5
        )

        salida = (stdout_salida or "").strip()
        salida_lower = salida.lower()

        if TEXTO_VALIDA.lower() in salida_lower:
            return True, salida
        elif TEXTO_INVALIDA.lower() in salida_lower:
            return False, salida
        else:
            #si no se reconoce el texto imprimimos el texto desconocido
            return False, f"(salida no reconocida) {salida}"

    except FileNotFoundError:
        return False, (
            f"No se encontró el ejecutable en '{RUTA_EJECUTABLE}'. "
            "Revisa la ruta y que el programa esté compilado."
        )
    except subprocess.TimeoutExpired:
        proceso.kill()
        return False, "El programa tardó demasiado en responder."
    except Exception as e:
        return False, f"Error inesperado: {e}"


class AplicacionAutomata(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Validador de Cadenas - Autómata KRAVNIKA")
        self.geometry("520x480")
        self.resizable(False, False)

        self.historial = []  #lista de (cadena, resultado_texto)

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

        # Resultado actual
        self.label_resultado = ttk.Label(
            self, text="", font=("Segoe UI", 12, "bold")
        )
        self.label_resultado.pack(pady=(4, 10))

        #history
        ttk.Label(self, text="Historial:").pack(anchor="w", padx=12)

        frame_historial = ttk.Frame(self)
        frame_historial.pack(fill="both", expand=True, padx=12, pady=(4, 12))

        columnas = ("cadena", "resultado")
        self.tabla_historial = ttk.Treeview(
            frame_historial, columns=columnas, show="headings", height=12
        )
        self.tabla_historial.heading("cadena", text="Cadena")
        self.tabla_historial.heading("resultado", text="Resultado")
        self.tabla_historial.column("cadena", width=260)
        self.tabla_historial.column("resultado", width=200)
        self.tabla_historial.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            frame_historial, orient="vertical", command=self.tabla_historial.yview
        )
        self.tabla_historial.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        #limpiar history
        ttk.Button(
            self, text="Limpiar historial", command=self.limpiar_historial
        ).pack(pady=(0, 12))

    def validar_cadena(self):
        cadena = self.entry_cadena.get().strip()

        if not cadena:
            messagebox.showwarning("Aviso", "Escribe una cadena antes de validar.")
            return

        #deshabilitamos el botón 
        #ayudando el envio de varias cadenas
        self.boton_validar.config(state="disabled")
        self.update_idletasks()

        es_valida, mensaje = ejecutar_automata(cadena)

        self.boton_validar.config(state="normal")

        if es_valida:
            texto_resultado = "✅ Válida"
            self.label_resultado.config(text=texto_resultado, foreground="green")
        else:
            texto_resultado = "❌ Inválida"
            self.label_resultado.config(text=texto_resultado, foreground="red")
#Agregar pantalla de historial
        self.tabla_historial.insert(
            "", 0, values=(cadena, "Válida" if es_valida else "Inválida")
        )
        self.historial.append((cadena, es_valida))

        self.entry_cadena.delete(0, tk.END)
        self.entry_cadena.focus()

    def limpiar_historial(self):
        respuesta = messagebox.askyesno(
            "Confirmar", "¿Seguro que quieres borrar todo el historial?"
        )
        if respuesta:
            self.tabla_historial.delete(*self.tabla_historial.get_children())
            self.historial.clear()
            self.label_resultado.config(text="")


if __name__ == "__main__":
    app = AplicacionAutomata()
    app.mainloop()