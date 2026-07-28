import tkinter as tk
from tkinter import ttk 


class Reglas(ttk.LabelFrame):
    def __init__(self,parent):
        super().__init__(parent, padding = 10)

        label_resumen = ttk.Label(self, text = "Resumen", font = ("Console", 14, "bold"))
        label_resumen.pack(anchor = "w", pady = (0,8))


        frame_expresiones = ttk.Frame(self, padding=10)
        frame_expresiones.pack(side=tk.TOP, fill="both", expand=True, padx=12, pady=12)

        label_titulo_expresiones = ttk.Label(frame_expresiones, text = "Expresion Logica", font = ("Console", 10, "bold"))
        label_titulo_expresiones.pack(anchor = "w", pady = (0,4))
        texto_expresiones = (
            "{[(e ↔ f) ∨ (g ↔ h)] ∧ ¬i ∧ [j ∨ (k ↔ l)]}\n"
            " ∧ {(a ⊻ b) ∧ [c ∧ (z ↔ y)]} → Pn\n"
            "P1 ∧ P2 ∧ P3 ∧ ... ∧ Pn → q"
        )
        label_expresiones = ttk.Label(frame_expresiones, text=texto_expresiones, font=("Console", 15), justify="left")
        label_expresiones.pack(anchor="w", pady=(0, 15))

        separador = ttk.Separator(frame_expresiones, orient="horizontal")
        separador.pack(fill="x", pady=6)

        label_titulo_estado = ttk.Label(frame_expresiones, text = "Estado de Proposiciones", font = ("Console", 14, "bold"))
        label_titulo_estado.pack(anchor = "w", pady = (0,4))

        frame_scroll_estado = ttk.Frame(frame_expresiones)
        frame_scroll_estado.pack(fill="x", expand=False)

        canvas_estado = tk.Canvas(frame_expresiones, highlightthickness=0, width=280, height=80)
        scroll_estado = ttk.Scrollbar(frame_expresiones, orient="vertical", command=canvas_estado.yview)
        
        scroll_frame_estado = ttk.Frame(canvas_estado)
        scroll_frame_estado.bind(
            "<Configure>",
            lambda e: canvas_estado.configure(scrollregion=canvas_estado.bbox("all"))
        )

        canvas_estado.create_window((0, 0), window=scroll_frame_estado, anchor="nw")
        canvas_estado.configure(yscrollcommand=scroll_estado.set)

        canvas_estado.pack(side="left", fill="both", expand=True)
        scroll_estado.pack(side="right", fill="y")

        texto_estado_inicial = (
            "a = 0\nb = 0\nc = 0\ny = 0\nz = 0\n"
            "i = 0\nj = 0\nk = 0\nl = 0\ne = 0\n"
            "f = 0\ng = 0\nh = 0\npn = 0\nq = 0"
        )
        self.label_estado = ttk.Label(scroll_frame_estado, text="Registra una palabra para iniciar...", font=("Console", 14), justify="left")
        self.label_estado.pack(anchor="nw", padx=5)

        lbl_reglas = ttk.Label(self, text="Reglas", font=("Console", 16, "bold"))
        lbl_reglas.pack(anchor="w", pady=(15, 8))
        frame_proposiciones = ttk.Frame(self)
        frame_proposiciones.pack(side=tk.TOP, fill="both", expand=True, pady=(10, 0))

        canvas = tk.Canvas(frame_proposiciones, highlightthickness=0, width=280, height=120)
        scrollbar = ttk.Scrollbar(frame_proposiciones, orient="vertical", command=canvas.yview)
        
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        texto_proposiciones = (
            "a = Inicia con \" \n"
            "b = Inicia con -\n"
            "c = Termina con :\n"
            "y = Termina con .\n"
            "z = Es la ultima letra\n"
            "i = Contiene: Jorge, Jonathan, Fabritzio, Rodrigo\n"
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
        label_proposiciones = ttk.Label(scrollable_frame, text=texto_proposiciones, font=("Console", 12), justify="left")
        label_proposiciones.pack(anchor="w", pady=(0, 10), expand=True)


        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    #THIRD, SET WORDS
    def set_text_word(self, n,
                    content,
                    output,
                    init_quotation, 
                    init_hyphen,
                    contain_names,
                    have_digits,
                    have_special_symbols,
                    digit19):
        return  f"""
        P{n}: {content}
        {{( ¬{contain_names} ∧ [{have_digits} ∨ ({have_special_symbols} ↔ {digit19})])}}
        ∧ {{({init_quotation} ⊻ {init_hyphen})}} → {output}
        P{n} = {output}
--------------------------------
"""
                
    #Sin uso
    """a= {init_quotation}
        b= {init_hyphen}
        i = {contain_names}
        j = {have_digits}
        k = {have_special_symbols}
        l = {digit19}
    """
                
    # SECODS, SET PHRASES
    def set_phrases(self, content, 
                    output, words,
                    open_interogation,
                    close_interogation,
                    open_exclamation,
                    close_exclamation):
        return f"""
> Oracion: {content}
    Cierra signos de interrogacion: {open_interogation}
    Aprertura signos de interrogacion: {close_interogation}
    Aprertura signos de exclamación: {open_exclamation}
    Cierra signos de exclamación: {close_exclamation}
    
    Palabras: 
    {words}
==============================
"""
    
    # FIRST, SET PROPOSITION TEXT
    def set_text_propositions(self, content, output, prhases):
        return f"""
● {content}
{prhases}
salida final: {output}
                    """
                
