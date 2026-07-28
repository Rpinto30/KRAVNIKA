import tkinter as tk
from tkinter import ttk 


class Reglas(ttk.LabelFrame):
    def __init__(self,parent):
        super().__init__(parent, text="Reglas y Proposiciones", padding = 10)

        label_titulo_prop = ttk.Label(self, text = "Proposiciones", font = ("Kravnika", 10, "bold"))
        label_titulo_prop.pack(anchor = "w", padx = 12, pady = (0,4))

        texto_proposiciones = (
            "a = Inicia con \" \n"
            "b = Inicia con -\n"
            "c = Termina con :\"\n"
            "y = Termina con .\n"
            "z = Es la ultima letra\n"
            "i = Contiene (Jorge, Jonathan, Fabritzio, Rodrigo) en la palabra\n"
            "j = Contiene digitos\n"
            "k = Tiene simbolos especiales\n"
            "l = Son digitos del 1 al 9 \n"
            "e = Contiene ?\n"
            "f = Contiene un ? para cerrar\n"
            "g = Contiene un ! para cerrar\n"
            "h = Contiene un !\n"
            "pn = Palabra enésima es valida\n"
            "q = Palabra / Cadena valida\n"
        )
        label_proposiciones = ttk.Label(self, text=texto_proposiciones, font=("Kravnika", 10), justify="left")
        label_proposiciones.pack(anchor="w", pady=(0, 10))


        label_titulo_expresiones = ttk.Label(self, text = "Expresion Logica", font = ("Kravnika", 10, "bold"))
        label_titulo_expresiones.pack(anchor = "w", pady = (0,4))
        texto_expresiones = (
            "{[(e ↔ f) ∨ (g ↔ h)] ∧ ¬i ∧ [j ∨ (k ↔ l)]}"
            " ∧ {(a ⊕ b) ∧ [c ∧ (z ↔ y)]} → Pn"
            "P1 ∧ P2 ∧ P3 ∧ ... ∧ Pn → q"
        )
        label_expresiones = ttk.Label(self, text=texto_expresiones, font=("Kravnika", 10), justify="left")
        label_expresiones.pack(anchor="w", pady=(0, 15))

        label_titulo_estado = ttk.Label(self, text = "Estado de Proposiciones", font = ("Kravnika", 10, "bold"))
        label_titulo_estado.pack(anchor = "w", pady = (0,4))

        self.label_estado = ttk.Label(self, text="p = 0\nq = 0\nr = 0\ns = 0", font=("Kravnika", 10), justify="left")
        self.label_estado.pack(anchor="w")

    def actualizar_estado(self, p : int = 0, q : int = 0, r : int = 0, s : int = 0):
        #Metodo para actualizar el estado de las proposiciones en la interfaz
        texto_actualizado = f"p = {p}\nq = {q}\nr = {r}\ns = {s}"
        self.label_estado.config(text=texto_actualizado)
