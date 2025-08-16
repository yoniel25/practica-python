import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import operaciones_matematicas as operaciones
import math

class Calculadora:
    def __init__(self, ventana_raiz):
        self.ventana_raiz = ventana_raiz
        self.ventana_raiz.title("Calculadora Científica Pro")
        self.ventana_raiz.geometry("520x750")
        self.ventana_raiz.resizable(False, False)
        
        # Variables para almacenar datos
        self.numero_actual = tk.StringVar()
        self.numero_actual.set("0")
        self.operacion_pendiente = ""
        self.primer_numero = 0
        self.nuevo_numero = True
        self.expresion_actual = ""
        
        # Estado/calibración
        self.modo_angulo = 'RAD'  # RAD o DEG

        # Configurar el estilo
        self.configurar_estilo()
        
        # Crear la interfaz
        self.crear_interfaz()
        
    def configurar_estilo(self):
        """Configura el estilo visual de la calculadora"""
        estilo = ttk.Style()
        estilo.theme_use('clam')
        
        # Configurar colores modernos y oscuros
        self.ventana_raiz.configure(bg='#1a1a1a')
        
    def crear_interfaz(self):
        """Crea todos los elementos de la interfaz"""
        # Frame principal con padding mejorado
        frame_principal = tk.Frame(self.ventana_raiz, bg='#1a1a1a', padx=15, pady=15)
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Título de la calculadora
        self.crear_titulo(frame_principal)
        
        # Pantalla de visualización
        self.crear_pantalla(frame_principal)
        
        # Controles superiores
        self.crear_controles_superiores(frame_principal)
        
        # Botones científicos
        self.crear_botones_cientificos(frame_principal)
        
        # Botones alfabéticos
        self.crear_botones_alfabeticos(frame_principal)
        
        # Botones numéricos y operadores
        self.crear_botones_numericos(frame_principal)
        
    def crear_titulo(self, padre):
        """Crea el título de la calculadora"""
        titulo = tk.Label(
            padre,
            text="CALCULADORA CIENTÍFICA",
            font=('Arial', 16, 'bold'),
            bg='#1a1a1a',
            fg='#00ff88',
            pady=10
        )
        titulo.pack()
        
    def crear_pantalla(self, padre):
        """Crea la pantalla de visualización mejorada"""
        # Frame exterior con borde
        frame_exterior = tk.Frame(padre, bg='#00ff88', relief=tk.RAISED, bd=3)
        frame_exterior.pack(fill=tk.X, pady=(0, 15))
        
        # Frame interior con gradiente simulado
        frame_pantalla = tk.Frame(frame_exterior, bg='#0a0a0a', relief=tk.SUNKEN, bd=2)
        frame_pantalla.pack(fill=tk.BOTH, padx=3, pady=3)
        
        # Etiqueta para mostrar el número con mejor tipografía
        self.etiqueta_pantalla = tk.Label(
            frame_pantalla,
            textvariable=self.numero_actual,
            font=('Consolas', 32, 'bold'),
            bg='#0a0a0a',
            fg='#00ff88',
            anchor='e',
            padx=20,
            pady=20
        )
        self.etiqueta_pantalla.pack(fill=tk.BOTH, expand=True)
        
    def crear_controles_superiores(self, padre):
        """Crea los controles superiores con mejor diseño"""
        frame_controles = tk.Frame(padre, bg='#1a1a1a')
        frame_controles.pack(fill=tk.X, pady=(0, 10))
        
        # Botones de control superior con efectos hover
        controles_info = [
            ('Solve: x ▼', '#2d2d2d', '#3d3d3d'),
            ('RAD ▼', '#2d2d2d', '#3d3d3d', self.alternar_modo_angulo),
            ('Trig.', '#2d2d2d', '#3d3d3d'),
            ('Hyp.', '#2d2d2d', '#3d3d3d')
        ]
        
        for i, info in enumerate(controles_info):
            if len(info) == 4:  # Con comando
                texto, color_normal, color_hover, comando = info
                boton = tk.Button(
                    frame_controles,
                    text=texto,
                    font=('Arial', 11, 'bold'),
                    bg=color_normal,
                    fg='#ffffff',
                    relief=tk.FLAT,
                    bd=0,
                    padx=12,
                    pady=8,
                    command=comando
                )
            else:  # Sin comando
                texto, color_normal, color_hover = info
                boton = tk.Button(
                    frame_controles,
                    text=texto,
                    font=('Arial', 11, 'bold'),
                    bg=color_normal,
                    fg='#ffffff',
                    relief=tk.FLAT,
                    bd=0,
                    padx=12,
                    pady=8
                )
            
            # Efectos hover
            boton.bind('<Enter>', lambda e, b=boton, c=color_hover: b.configure(bg=c))
            boton.bind('<Leave>', lambda e, b=boton, c=color_normal: b.configure(bg=c))
            
            boton.pack(side=tk.LEFT, padx=3, expand=True, fill=tk.X)
            
        # Guardar referencia al botón de modo
        self.boton_modo = frame_controles.winfo_children()[1]
            
        # Botones de navegación y calcular con mejor diseño
        frame_nav = tk.Frame(padre, bg='#1a1a1a')
        frame_nav.pack(fill=tk.X, pady=(0, 10))
        
        # Botón izquierda
        btn_izq = tk.Button(
            frame_nav,
            text='←',
            font=('Arial', 14, 'bold'),
            bg='#4a148c',
            fg='white',
            relief=tk.RAISED,
            bd=2,
            padx=15,
            pady=8,
            command=self.retroceso
        )
        btn_izq.pack(side=tk.LEFT, padx=3)
        
        # Efectos hover para botón izquierda
        btn_izq.bind('<Enter>', lambda e: btn_izq.configure(bg='#6a1b9a'))
        btn_izq.bind('<Leave>', lambda e: btn_izq.configure(bg='#4a148c'))
        
        # Botón calcular
        btn_calc = tk.Button(
            frame_nav,
            text='Calcular',
            font=('Arial', 13, 'bold'),
            bg='#00695c',
            fg='white',
            relief=tk.RAISED,
            bd=2,
            padx=25,
            pady=8,
            command=self.resolver_expresion
        )
        btn_calc.pack(side=tk.LEFT, padx=3, expand=True, fill=tk.X)
        
        # Efectos hover para botón calcular
        btn_calc.bind('<Enter>', lambda e: btn_calc.configure(bg='#00796b'))
        btn_calc.bind('<Leave>', lambda e: btn_calc.configure(bg='#00695c'))
        
        # Botón derecha
        btn_der = tk.Button(
            frame_nav,
            text='→',
            font=('Arial', 14, 'bold'),
            bg='#4a148c',
            fg='white',
            relief=tk.RAISED,
            bd=2,
            padx=15,
            pady=8,
            command=self.limpiar
        )
        btn_der.pack(side=tk.LEFT, padx=3)
        
        # Efectos hover para botón derecha
        btn_der.bind('<Enter>', lambda e: btn_der.configure(bg='#6a1b9a'))
        btn_der.bind('<Leave>', lambda e: btn_der.configure(bg='#4a148c'))
        
    def crear_botones_cientificos(self, padre):
        """Crea los botones científicos con mejor diseño"""
        frame_cientificos = tk.Frame(padre, bg='#1a1a1a')
        frame_cientificos.pack(fill=tk.X, pady=(0, 10))
        
        # Configurar grid 5x4
        for i in range(5):
            frame_cientificos.grid_columnconfigure(i, weight=1)
        for i in range(4):
            frame_cientificos.grid_rowconfigure(i, weight=1)
        
        # Botones científicos (4 filas x 5 columnas) con colores mejorados
        botones_cientificos = [
            # Fila 1 - Funciones trigonométricas
            ('sin', '#2e7d32', '#4caf50'), ('cos', '#2e7d32', '#4caf50'), ('tan', '#2e7d32', '#4caf50'), 
            ('log', '#1565c0', '#2196f3'), ('ln', '#1565c0', '#2196f3'),
            # Fila 2 - Funciones matemáticas
            ('√', '#ff6f00', '#ff9800'), ('x^y', '#ff6f00', '#ff9800'), ('1/x', '#ff6f00', '#ff9800'), 
            ('10^x', '#1565c0', '#2196f3'), ('|x|', '#ff6f00', '#ff9800'),
            # Fila 3 - Operadores de comparación
            ('≥', '#6a1b9a', '#8e24aa'), ('>', '#6a1b9a', '#8e24aa'), ('<', '#6a1b9a', '#8e24aa'), 
            ('≤', '#6a1b9a', '#8e24aa'), ('%', '#d32f2f', '#f44336'),
            # Fila 4 - Constantes y paréntesis
            ('e', '#1976d2', '#2196f3'), ('i', '#1976d2', '#2196f3'), ('π', '#1976d2', '#2196f3'), 
            ('(', '#424242', '#616161'), (')', '#424242', '#616161')
        ]
        
        for i, (texto, color_normal, color_hover) in enumerate(botones_cientificos):
            fila = i // 5
            columna = i % 5
            self.crear_boton_cientifico(frame_cientificos, texto, fila, columna, color_normal, color_hover)
            
    def crear_botones_alfabeticos(self, padre):
        """Crea los botones alfabéticos con mejor diseño"""
        frame_alfabeticos = tk.Frame(padre, bg='#1a1a1a')
        frame_alfabeticos.pack(fill=tk.X, pady=(0, 10))
        
        # Configurar grid 5x2
        for i in range(5):
            frame_alfabeticos.grid_columnconfigure(i, weight=1)
        for i in range(2):
            frame_alfabeticos.grid_rowconfigure(i, weight=1)
        
        # Letras (2 filas x 5 columnas) con colores mejorados
        letras = [
            # Fila 1
            'q', 'r', 's', 't', 'u',
            # Fila 2
            'v', 'w', 'x', 'y', 'z'
        ]
        
        for i, letra in enumerate(letras):
            fila = i // 5
            columna = i % 5
            boton = tk.Button(
                frame_alfabeticos,
                text=letra.upper(),
                font=('Arial', 13, 'bold'),
                bg='#5e35b1',
                fg='white',
                relief=tk.RAISED,
                bd=2,
                padx=8,
                pady=10,
                command=lambda l=letra: self.agregar_letra(l)
            )
            boton.grid(row=fila, column=columna, padx=2, pady=2, sticky='nsew')
            
            # Efectos hover
            boton.bind('<Enter>', lambda e, b=boton: b.configure(bg='#7b1fa2'))
            boton.bind('<Leave>', lambda e, b=boton: b.configure(bg='#5e35b1'))
            
    def crear_botones_numericos(self, padre):
        """Crea los botones numéricos y operadores con mejor diseño"""
        frame_numericos = tk.Frame(padre, bg='#1a1a1a')
        frame_numericos.pack(fill=tk.BOTH, expand=True)
        
        # Configurar grid 4x5
        for i in range(5):
            frame_numericos.grid_columnconfigure(i, weight=1)
        for i in range(4):
            frame_numericos.grid_rowconfigure(i, weight=1)
        
        # Botones numéricos y operadores con colores mejorados
        botones_numericos = [
            # Fila 1
            ('1', '#424242', '#616161'), ('2', '#424242', '#616161'), ('3', '#424242', '#616161'), 
            ('/', '#ff9800', '#ffb74d'), ('C', '#d32f2f', '#f44336'),
            # Fila 2
            ('4', '#424242', '#616161'), ('5', '#424242', '#616161'), ('6', '#424242', '#616161'), 
            ('×', '#ff9800', '#ffb74d'), ('AC', '#d32f2f', '#f44336'),
            # Fila 3
            ('7', '#424242', '#616161'), ('8', '#424242', '#616161'), ('9', '#424242', '#616161'), 
            ('-', '#ff9800', '#ffb74d'), ('=', '#4caf50', '#66bb6a', 2),
            # Fila 4
            ('.', '#424242', '#616161'), ('+/-', '#424242', '#616161'), ('0', '#424242', '#616161'), 
            ('+', '#ff9800', '#ffb74d'), ('', '', 0)
        ]
        
        for i, boton_info in enumerate(botones_numericos):
            fila = i // 5
            columna = i % 5
            
            if len(boton_info) == 4:  # Botón con rowspan
                texto, color_normal, color_hover, rowspan = boton_info
                if texto:  # Solo crear botón si hay texto
                    boton = tk.Button(
                        frame_numericos,
                        text=texto,
                        font=('Arial', 16, 'bold'),
                        bg=color_normal,
                        fg='white',
                        relief=tk.RAISED,
                        bd=2,
                        padx=8,
                        pady=12,
                        command=lambda t=texto: self.procesar_boton_numerico(t)
                    )
                    boton.grid(row=fila, column=columna, rowspan=rowspan, padx=2, pady=2, sticky='nsew')
                    
                    # Efectos hover
                    boton.bind('<Enter>', lambda e, b=boton, c=color_hover: b.configure(bg=c))
                    boton.bind('<Leave>', lambda e, b=boton, c=color_normal: b.configure(bg=c))
            else:
                texto, color_normal, color_hover = boton_info
                boton = tk.Button(
                    frame_numericos,
                    text=texto,
                    font=('Arial', 16, 'bold'),
                    bg=color_normal,
                    fg='white',
                    relief=tk.RAISED,
                    bd=2,
                    padx=8,
                    pady=12,
                    command=lambda t=texto: self.procesar_boton_numerico(t)
                )
                boton.grid(row=fila, column=columna, padx=2, pady=2, sticky='nsew')
                
                # Efectos hover
                boton.bind('<Enter>', lambda e, b=boton, c=color_hover: b.configure(bg=c))
                boton.bind('<Leave>', lambda e, b=boton, c=color_normal: b.configure(bg=c))
                
    def crear_boton_cientifico(self, padre, texto, fila, columna, color_normal, color_hover):
        """Crea un botón científico individual con efectos hover"""
        boton = tk.Button(
            padre,
            text=texto,
            font=('Arial', 11, 'bold'),
            bg=color_normal,
            fg='white',
            relief=tk.RAISED,
            bd=2,
            padx=8,
            pady=10,
            command=lambda: self.procesar_boton_cientifico(texto)
        )
        boton.grid(row=fila, column=columna, padx=2, pady=2, sticky='nsew')
        
        # Efectos hover
        boton.bind('<Enter>', lambda e, b=boton, c=color_hover: b.configure(bg=c))
        boton.bind('<Leave>', lambda e, b=boton, c=color_normal: b.configure(bg=c))
        
    def procesar_boton_cientifico(self, texto):
        """Procesa los botones científicos"""
        if texto == 'log':
            self.calcular_logaritmo_base_10()
        elif texto == 'ln':
            self.calcular_logaritmo_natural()
        elif texto == 'sin':
            self.calcular_trigonometrica('sin')
        elif texto == 'cos':
            self.calcular_trigonometrica('cos')
        elif texto == 'tan':
            self.calcular_trigonometrica('tan')
        elif texto == '√':
            self.calcular_raiz_cuadrada()
        elif texto == 'x^y':
            self.agregar_operacion('^')
        elif texto == '1/x':
            self.calcular_inverso()
        elif texto == '10^x':
            self.calcular_potencia10()
        elif texto == '|x|':
            self.calcular_valor_absoluto()
        elif texto == 'e':
            self.mostrar_resultado(math.e)
        elif texto == 'π':
            self.mostrar_resultado(math.pi)
        elif texto == 'i':
            self.agregar_operacion('i')
        elif texto in ['(', ')']:
            self.agregar_operacion(texto)
        elif texto == '%':
            self.calcular_porcentaje()
        elif texto in ['≥', '>', '<', '≤']:
            self.agregar_operacion(texto)
        else:
            self.agregar_operacion(texto)
            
    def procesar_boton_numerico(self, texto):
        """Procesa los botones numéricos y operadores"""
        if texto.isdigit() or texto == '.':
            self.agregar_digito(texto)
        elif texto in ['+', '-', '×', '/']:
            self.establecer_operacion(texto)
        elif texto == '=':
            self.calcular_resultado()
        elif texto == 'C':
            self.limpiar()
        elif texto == 'AC':
            self.limpiar_todo()
        elif texto == '+/-':
            self.cambiar_signo()
            
    def agregar_letra(self, letra):
        """Agrega una letra a la expresión"""
        self.expresion_actual += letra
        self.numero_actual.set(self.expresion_actual)
        
    def agregar_operacion(self, operacion):
        """Agrega una operación a la expresión"""
        self.expresion_actual += operacion
        self.numero_actual.set(self.expresion_actual)
        
    def formatear_resultado(self, valor):
        """Devuelve una representación sin decimales si es entero, o decimal si corresponde."""
        try:
            numero = float(valor)
        except (TypeError, ValueError):
            return str(valor)

        # Evitar mostrar -0
        if numero == 0:
            return "0"

        # Enteros exactos sin parte decimal
        if float(numero).is_integer():
            return str(int(numero))

        # Limitar a 10 decimales y recortar ceros a la derecha
        texto = f"{numero:.10f}".rstrip('0').rstrip('.')
        return texto

    def mostrar_resultado(self, valor, marcar_nuevo=True):
        """Muestra el valor formateado en la pantalla y opcionalmente marca nuevo número."""
        self.numero_actual.set(self.formatear_resultado(valor))
        if marcar_nuevo:
            self.nuevo_numero = True

    def agregar_digito(self, digito):
        """Agrega un dígito al número actual"""
        if self.nuevo_numero:
            self.numero_actual.set(digito)
            self.nuevo_numero = False
        else:
            if digito == '.' and '.' in self.numero_actual.get():
                return
            if self.numero_actual.get() == '0' and digito != '.':
                self.numero_actual.set(digito)
            else:
                self.numero_actual.set(self.numero_actual.get() + digito)
                
    def establecer_operacion(self, operacion):
        """Establece la operación a realizar"""
        try:
            self.primer_numero = float(self.numero_actual.get())
            # Soportar potencia con '^' y multiplicación con '×'
            if operacion == '^':
                self.operacion_pendiente = '**'
            elif operacion == '×':
                self.operacion_pendiente = '*'
            else:
                self.operacion_pendiente = operacion
            self.nuevo_numero = True
        except ValueError:
            messagebox.showerror("Error", "Número inválido")
            
    def calcular_resultado(self):
        """Calcula el resultado de la operación"""
        if not self.operacion_pendiente:
            return
            
        try:
            segundo_numero = float(self.numero_actual.get())
            # Resolver según la operación pendiente
            if self.operacion_pendiente in ['+', '-', '*', '/']:
                op_map = {'+': '+', '-': '-', '*': '×', '/': '÷'}
                resultado = operaciones.realizar_operacion(
                    self.primer_numero,
                    segundo_numero,
                    op_map[self.operacion_pendiente]
                )
            elif self.operacion_pendiente == '**':
                resultado = operaciones.potencia(self.primer_numero, segundo_numero)
            else:
                raise ValueError('Operación no soportada')
            self.mostrar_resultado(resultado)
            self.operacion_pendiente = ""
            self.nuevo_numero = True
        except Exception as e:
            messagebox.showerror("Error", f"Error en el cálculo: {str(e)}")
            
    def limpiar(self):
        """Limpia la calculadora"""
        self.numero_actual.set("0")
        self.operacion_pendiente = ""
        self.primer_numero = 0
        self.nuevo_numero = True
        
    def limpiar_todo(self):
        """Limpia todo incluyendo la expresión"""
        self.limpiar()
        self.expresion_actual = ""
        
    def cambiar_signo(self):
        """Cambia el signo del número actual"""
        try:
            numero = float(self.numero_actual.get())
            self.mostrar_resultado(-numero, marcar_nuevo=False)
        except ValueError:
            messagebox.showerror("Error", "Número inválido")
            
    def calcular_porcentaje(self):
        """Calcula el porcentaje del número actual"""
        try:
            numero = float(self.numero_actual.get())
            resultado = numero / 100
            self.mostrar_resultado(resultado)
        except ValueError:
            messagebox.showerror("Error", "Número inválido")
            
    def calcular_raiz_cuadrada(self):
        """Calcula la raíz cuadrada del número actual"""
        try:
            numero = float(self.numero_actual.get())
            if numero < 0:
                messagebox.showerror("Error", "No se puede calcular la raíz cuadrada de un número negativo")
                return
            resultado = operaciones.raiz_cuadrada(numero)
            self.mostrar_resultado(resultado)
        except ValueError:
            messagebox.showerror("Error", "Número inválido")
            
    def calcular_inverso(self):
        """Calcula el inverso del número actual"""
        try:
            numero = float(self.numero_actual.get())
            if numero == 0:
                messagebox.showerror("Error", "No se puede dividir por cero")
                return
            resultado = operaciones.inverso(numero)
            self.mostrar_resultado(resultado)
        except ValueError:
            messagebox.showerror("Error", "Número inválido")
            
    def calcular_factorial(self):
        """Calcula el factorial del número actual"""
        try:
            numero = int(float(self.numero_actual.get()))
            if numero < 0:
                messagebox.showerror("Error", "No se puede calcular el factorial de un número negativo")
                return
            resultado = operaciones.factorial(numero)
            self.mostrar_resultado(resultado)
        except ValueError:
            messagebox.showerror("Error", "Número inválido")
            
    def calcular_logaritmo_natural(self):
        """Calcula el logaritmo natural del número actual"""
        try:
            numero = float(self.numero_actual.get())
            if numero <= 0:
                messagebox.showerror("Error", "No se puede calcular el logaritmo de un número menor o igual a cero")
                return
            resultado = operaciones.logaritmo_natural(numero)
            self.mostrar_resultado(resultado)
        except ValueError:
            messagebox.showerror("Error", "Número inválido")
            
    def calcular_logaritmo_base_10(self):
        """Calcula el logaritmo base 10 del número actual"""
        try:
            numero = float(self.numero_actual.get())
            if numero <= 0:
                messagebox.showerror("Error", "No se puede calcular el logaritmo de un número menor o igual a cero")
                return
            resultado = operaciones.logaritmo_base_10(numero)
            self.mostrar_resultado(resultado)
        except ValueError:
            messagebox.showerror("Error", "Número inválido")
            
    def calcular_valor_absoluto(self):
        """Calcula el valor absoluto del número actual"""
        try:
            numero = float(self.numero_actual.get())
            resultado = operaciones.valor_absoluto(numero)
            self.mostrar_resultado(resultado)
        except ValueError:
            messagebox.showerror("Error", "Número inválido")

    # === Funciones nuevas ===
    def alternar_modo_angulo(self):
        """Alterna entre RAD y DEG para funciones trigonométricas."""
        self.modo_angulo = 'DEG' if self.modo_angulo == 'RAD' else 'RAD'
        self.boton_modo.config(text=f'{self.modo_angulo} ▼')

        # Si hay un valor numérico en pantalla, no lo cambia, solo el modo

    def obtener_angulo_en_radianes(self, valor):
        """Convierte el valor de ángulo de acuerdo al modo actual a radianes."""
        rad = float(valor)
        if self.modo_angulo == 'DEG':
            rad = math.radians(rad)
        return rad

    def calcular_trigonometrica(self, funcion):
        """Calcula sin, cos o tan dependiendo del modo RAD/DEG."""
        try:
            valor = float(self.numero_actual.get())
            rad = self.obtener_angulo_en_radianes(valor)
            if funcion == 'sin':
                res = math.sin(rad)
            elif funcion == 'cos':
                res = math.cos(rad)
            else:
                res = math.tan(rad)
            self.mostrar_resultado(res)
        except ValueError:
            messagebox.showerror("Error", "Número inválido")

    def calcular_potencia10(self):
        """Calcula 10 elevado al número actual."""
        try:
            valor = float(self.numero_actual.get())
            self.mostrar_resultado(10 ** valor)
        except ValueError:
            messagebox.showerror("Error", "Número inválido")

    def retroceso(self):
        """Elimina el último carácter del display."""
        texto = self.numero_actual.get()
        if len(texto) > 1:
            self.numero_actual.set(texto[:-1])
        else:
            self.numero_actual.set('0')
            self.nuevo_numero = True

    def resolver_expresion(self):
        """Evalúa una expresión matemática simple ingresada en el display."""
        expresion = self.numero_actual.get().replace('×', '*').replace('÷', '/')
        expresion = expresion.replace('^', '**')
        try:
            # Seguridad: solo permitir dígitos, operadores básicos y punto
            import re
            if not re.fullmatch(r"[\d\s\.+\-*/()**]+", expresion):
                raise ValueError("Expresión no permitida")
            resultado = eval(expresion)
            self.mostrar_resultado(resultado)
        except Exception as e:
            messagebox.showerror("Error", f"Expresión inválida: {e}")

def main():
    """Función principal para ejecutar la calculadora"""
    ventana_raiz = tk.Tk()
    calculadora = Calculadora(ventana_raiz)
    ventana_raiz.mainloop()

if __name__ == "__main__":
    main()
