#Entrada Usuario/Historial Cadenas
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import subprocess
import os
from reglas import Reglas
import json

# Ruta al ejecutable compilado
PARENT_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_EJECUTABLE = os.path.join(PARENT_DIR, "Automate", "output.exe")

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
            cwd=os.path.dirname(RUTA_EJECUTABLE)
        )

        stdout_salida, stderr_salida = proceso.communicate(
            input=cadena + "\n", timeout=5
        )

        salida = (stdout_salida or "").strip()
        salida_lower = salida.lower()

        print(salida)

        if salida == '1':
            print('yaaaaaaaaaaaaaaa')
            return True, salida
        elif salida == '0':
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
        self.geometry("1600x920")
        self.resizable(True, True)

        self.historial = [] 
        self.in_kravnika = True
        self.actual_str = ""
        self._construir_widgets()

    def _construir_widgets(self):
        padding = {"padx": 12, "pady": 8}
        
        top_frame_right = ttk.Frame(self)
        top_frame_right.pack()
        
        ttk.Label(top_frame_right, text="K\"RAVNIKA", font=('Kravnika', 50)).pack(expand=True, anchor="center", pady=(15,0))
        ttk.Label(top_frame_right, text="KRAVNIKA", font=('Arial', 13, 'bold')).pack(expand=True, anchor="center", pady=(0, 30))
        
        main_container = ttk.Frame(self)
        main_container.pack(fill="both", expand=True, padx=12, pady=12)

        self.panel_reglas = Reglas(main_container)
        self.panel_reglas.pack(side =tk.LEFT, fill="both", expand=True, padx=(0,10), pady=5)

        global_frame_right = ttk.Frame(main_container)
        global_frame_right.pack(side=tk.LEFT, fill="both", expand=True, padx=(10, 0))
        
        global_frame_jorge = ttk.Frame(main_container)
        global_frame_jorge.pack(side=tk.RIGHT, fill="both", expand=True, padx=(10, 0))
                
        raw_img = Image.open(os.path.join(PARENT_DIR, "kravnika_creator.png"))
        resized_img = raw_img.resize((350, 550), Image.Resampling.LANCZOS)
        tk_img = ImageTk.PhotoImage(resized_img) 
        label = tk.Label(global_frame_jorge, image=tk_img)
        label.pack(expand= True, fill='both')
        label.image = tk_img 
        
        frame_entrada = ttk.Frame(global_frame_right)
        frame_entrada.pack(fill="x", **padding)

        ttk.Label(frame_entrada, text="Cadena a validar:").pack(anchor="w")

        self.entry_cadena = ttk.Entry(frame_entrada, font=("Kravnika", 30))
        self.entry_cadena.pack(fill="x", pady=(4, 8))
        self.entry_cadena.bind("<Return>", lambda event: self.validar_cadena())

        self.boton_validar = ttk.Button(
            frame_entrada, text="Validar", command=self.validar_cadena
        )
        self.boton_validar.pack(anchor="e")

        # Resultado actual
        self.label_resultado = ttk.Label(
            global_frame_right, text="", font=("Segoe UI", 12, "bold")
        )
        self.label_resultado.pack(pady=(4, 10))

        #history
        ttk.Label(global_frame_right, text="Historial:").pack(anchor="w", padx=12)

        frame_historial = ttk.Frame(global_frame_right)
        frame_historial.pack(fill="both", expand=True, padx=12, pady=(4, 12))

        columnas = ("cadena")
        self.tabla_historial = ttk.Treeview(
            frame_historial, columns=columnas, show="headings", height=12
        )
        
        self.tabla_historial.heading("cadena", text="Cadena")
        #self.tabla_historial.heading("resultado", text="Resultado")
        self.tabla_historial.column("cadena", width=260)
        #self.tabla_historial.column("resultado", width=200)
        self.tabla_historial.pack(side="left", fill="both", expand=True)

        style = ttk.Style()
        style.configure("Treeview", rowheight=30, font = ('Kravnika', 30)) 
        self.tabla_historial.tag_configure("valid", foreground="green")
        self.tabla_historial.tag_configure("invalid", foreground="red")

        scrollbar = ttk.Scrollbar(
            frame_historial, orient="vertical", command=self.tabla_historial.yview
        )
        self.tabla_historial.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        frame_funtions = ttk.Frame(frame_historial)
        frame_funtions.pack(fill="y", padx=12)

        def change_lenguague():
            if self.in_kravnika:
                style.configure("Treeview", rowheight=30, font = ('Console', 15)) 
                lenguage.config(text="Kravnika")
                self.in_kravnika = False
                
                for n,item in enumerate(self.tabla_historial.get_children()):
                    print(self.historial[n][0].replace(':', ' '))
                    self.tabla_historial.item(item, values= (self.historial[n][0].replace(':', '_').replace('\"','')))
            else:
                style.configure("Treeview", rowheight=30, font = ('Kravnika', 30)) 
                lenguage.config(text="Español")
                self.in_kravnika = True
                for n,item in enumerate(self.tabla_historial.get_children()):
                                    self.tabla_historial.item(item, values= (self.historial[n][0]))
        
        lenguage = ttk.Button(
                frame_historial, text="Español", width=15, command=  change_lenguague)
        lenguage.pack(anchor='center',fill='y')
        
        #limpiar history
        ttk.Button(
            frame_historial, text="Limpiar historial", width=15, command=self.limpiar_historial
        ).pack(pady=(0, 0), fill='y')
        

    def validar_cadena(self):
        cadena = self.entry_cadena.get().strip()
        self.actual_str = cadena
        if not cadena:
            messagebox.showwarning("Aviso", "Escribe una cadena antes de validar.")
            return
        self.actual_str
        self.boton_validar.config(state="disabled")
        self.update_idletasks()

        es_valida, mensaje = ejecutar_automata(cadena)

        self.boton_validar.config(state="normal")

        if es_valida == 1:
            texto_resultado = "✅ La cadena es valida"
            self.label_resultado.config(text=texto_resultado, foreground="green")
        else:
            texto_resultado = "❌ La cadena no es valida"
            self.label_resultado.config(text=texto_resultado, foreground="red")

        #pantalla historial
        texto_res = "Válida" if es_valida else "Inválida"
        tag_res = "valid" if es_valida else "invalid"

        self.tabla_historial.insert("", "end", values=(cadena), tags=(tag_res))

                
        self.historial.append((cadena, es_valida))

        self.entry_cadena.delete(0, tk.END)
        self.entry_cadena.focus()
        self.calc_proposition()
    
    def calc_proposition(self):
        with open(os.path.join(PARENT_DIR, "Automate", "proposition.json"), "r") as file:
            data = json.load(file)
            all_text = ""
            phrases = ""
            for pra in data['sentences']:
                words = ""
                for n, wor in enumerate(pra['words']):
                    words += self.panel_reglas.set_text_word(
                        n+1,
                        wor['content'],
                        wor['output'],
                        wor['init_quotation'],
                        wor['init_hyphen'],
                        wor['contain_names'],
                        wor['have_digits'],
                        wor['have_special_charts_digits'],
                        wor['next_special_chart_between_19']
                    )
                #words = [self.panel_reglas.set_text_word for x in pra['words']]
                
                phrases += self.panel_reglas.set_phrases(
                    pra['content'],
                    pra['output'],
                    words,
                    pra['init_interogation'],
                    pra['end_interogation'],
                    pra['init_exclamation'],
                    pra['end_exclamation']
                )
            all_text = self.panel_reglas.set_text_propositions(
                self.actual_str,
                data['output'],
                phrases
            )
        
        self.panel_reglas.label_estado.config(text=all_text)
            #self.panel_reglas.actualizar_estado(
                
            #)
        
        print(all_text)
        
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