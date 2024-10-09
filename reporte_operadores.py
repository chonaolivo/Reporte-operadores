import tkinter as tk
from tkinter import Menu
from tkinter import messagebox
from tkinter import ttk
from tkinter.font import Font
import pyautogui
import subprocess
import os
import sys
import pyperclip

def configuracion():

    def actual(Estilos,tema):
        try:
            # Encuentra el índice del tema en la lista de estilos
            numeroOrden = Estilos.index(tema)
            return numeroOrden
        except ValueError:
            # Si el tema no está en la lista, devuelve None o puedes manejarlo según lo necesites
            return 0

    def GuardarConfig(LTamanio,res1,res2,tema,operadores):
        LTamanio=escalar.get()
        LTamanio=round(float(LTamanio))
        res1=ancho.get()
        res2=largo.get()
        tema=estilos.get()
        tema=str(tema)
        if tema=="\n":
            tema="default"
        #Extraer configuracion de config.txt
        print(tema)
        with open("config.txt", "w") as file:
            pasar = str(LTamanio).strip() + "\n" + str(res1).strip() + "\n" + str(res2).strip() + "\n" + "\n" +  str(tema).strip()
            file.write(pasar)
            print("guardado.")
        
        Aoperadores=[]
        try:
            with open("Operadores.txt", "r") as file:
                # Bucle para añadir todos los operadores
                for linea in file:
                    # Quitamos el salto de línea para evitar incompatibilidades
                    clean = linea.strip()  # Eliminar el carácter \n
                    Aoperadores.append(clean)  # Agregar la línea limpia a la lista de opciones
        except FileNotFoundError:
            print(f"El archivo Operadores.txt no fue encontrado.")

        aux=operadores.current()
        aux1=Aoperadores[aux]
        Aoperadores[aux]=operadores.get()
        aux= '\n'.join(Aoperadores)
         #abrimos el archivo "Operadores.txt"
        with open("Operadores.txt", "w") as file:
            #Escribimos el archivo con un salto de linea
            file.write(aux)
        messagebox.showinfo("Éxito", "Se guardó correctamente.")
        aux1 = str(aux1) + ".txt"
        aux = str(operadores.get()) + ".txt"
        print(aux1, aux)
        os.rename(aux1, aux)

        ReiniciarPrograma()

    def cambiarEstilo(tema):
        estilo = estilos.get()  # Obtenemos el estilo seleccionado
        # Cambiamos el estilo de los botones
        style = ttk.Style()
        style.theme_use(estilo)

    def cargarSelector():
        opciones = []  # Inicializar la lista de opciones dentro de la función
        try:
            with open("Operadores.txt", "r") as file:
                # Bucle para añadir todos los operadores
                for linea in file:
                    # Quitamos el salto de línea para evitar incompatibilidades
                    clean = linea.strip()  # Eliminar el carácter \n
                    opciones.append(clean)  # Agregar la línea limpia a la lista de opciones
        except FileNotFoundError:
            print(f"El archivo Operadores.txt no fue encontrado.")
        return opciones

    def cambiarTamanio(valor):
        LTamanio = escalar.get()
        lbl.config(text=LTamanio)
    
    #Extraer configuracion de config.txt
    with open("config.txt", "r") as file:
        lineas = file.readlines()  # Lee todas las líneas del archivo
    LTamanio, res1, res2, nombre, tema = lineas

    VentanaConfiguracion = tk.Toplevel(ventana)
    VentanaConfiguracion.title("Configuracion")
    VentanaConfiguracion.geometry("800x600")
    VentanaConfiguracion.iconbitmap('phoenix.ico')
    estilo= ttk.Style()
    estilo.theme_use(tema)
    marco = tk.Frame(VentanaConfiguracion)
    marco.pack(padx=10, pady=10)
    # Crear una fuente con el tamaño deseado
    letra=int(LTamanio.strip())
    fuente = Font(family="Arial", size=letra)
    # Configurar la nueva fuente como la fuente predeterminada para todos los widgets
    ventana.option_add("*Font", fuente)

    tk.Label(marco, text="Tamaño Letra:").grid(row=0, column=0, sticky="w", pady=(0, 10))
    # Escalar para ajustar el tamaño de la letra
    escalar = ttk.Scale(marco, from_=8, to=24, orient="horizontal", command=lambda valor: cambiarTamanio(valor))
    escalar.set(LTamanio)  # Establece el valor inicial del escalar
    escalar.grid(row=0, column=1, sticky="w", pady=(0, 10))
    lbl= tk.Label(marco,text=LTamanio)
    lbl.grid(row=0,column=2,sticky="w",pady=(0,10))

    # Res ventana
    tk.Label(marco, text="Resolucion:").grid(row=1, column=0, sticky="w", pady=(0, 10))
    largo = tk.Entry(marco, width=15)
    largo.grid(row=1, column=1, sticky="w", padx=5, pady=(0, 10))
    largo.insert(0, res1)
    ancho = tk.Entry(marco, width=15)
    ancho.grid(row=1, column=2, sticky="w", padx=5, pady=(0, 10))
    ancho.insert(0, res2)

    # Cambiar nombre
    tk.Label(marco, text="Cambiar Nombre del operador:").grid(row=2, column=0, sticky="w", pady=(0, 10))
    opciones = cargarSelector()
    operadores = ttk.Combobox(marco, values=opciones)
    operadores.grid(row=2, column=1, sticky="w", pady=(0, 10))
    operadores.current(0)

    #Cambiar estilo
    # Obtener todos los estilos disponibles
    Estilos = ttk.Style().theme_names()
    # Crear combo box para seleccionar el estilo
    estilos = ttk.Combobox(marco, values=Estilos)
    estilos.grid(row=3,column=1,sticky="w",pady=(0,10))
    # Botón para aplicar el cambio de estilo
    btnPrueba = tk.Button(marco, text="Probar Estilo", command=lambda:cambiarEstilo(tema))
    btnPrueba.grid(row=3,column=2,sticky="w",pady=(0,10))
    estilos.current(actual(Estilos,tema))
    btnGuardar = tk.Button(marco,text="Guardar",command=lambda: GuardarConfig(LTamanio,res1,res2,tema,operadores))
    btnGuardar.grid(row=4,column=0,sticky="w",pady=(0,10))
    
def operativa():
    # Función para imprimir el valor actualizado
    def CambioLabel(valor_seleccionado):
            #Pregutamos si estamos en Relevamiento o no
        if varOpcion.get() == "Relevamiento":
            Label1["text"] = "Materiales"
        else:
            Label1["text"] = "Contexto"  
    
    #se crea y configura ventanaOperativa 
    ventanaOperativa = tk.Toplevel(ventana)
    ventanaOperativa.title("Operativa")
    ventanaOperativa.geometry("450x750")
    # Establecer el icono de la ventana
    ventanaOperativa.iconbitmap('phoenix.ico')

    #Se crea un Frame para contener los objetos que va a tener la ventana
    borde = tk.Frame(ventanaOperativa)
    borde.pack(pady=10)

    #Menu Selector para cambiar entre relevamiento y presupuesto
    opciones = ["Relevamiento", "Presupuesto"]  
    varOpcion = tk.StringVar(borde)
    #Seteamos el menu a la primera opcion
    varOpcion.set(opciones[0]) 
    # Menu Selector
    # Configurar el OptionMenu con la variable StringVar
    menu_selector = tk.OptionMenu(borde, varOpcion, *opciones,command=CambioLabel)
    menu_selector.grid(row=0, column=1, sticky="w", pady=(0,10))
    #Funcion pasar: crea una variable que almacena todo el texto de los entrys y los pega de forma ordenada en el entry Resultado
    def pasar():
        #Le damos formato a todo el codigo
        #preguntamos si estamos en Relevamiento o no
        if varOpcion.get() == "Relevamiento":
            texto = "*" + nombre.get() + "*" + "\n_Relevamiento:_\n\n" + items.get("1.0", tk.END)
        else:
            texto = "*" + nombre.get() + "*" + "\n\n_Presupuestar:_\n" + items.get("1.0", tk.END)
        if contacto.get():
            texto += "\n*Contacto:* " + contacto.get() + "\n"
        if telefono.get():
            texto += "*Telefono:* " + telefono.get() + "\n"
        if CorreoElectronico.get():
            texto += "*Correo Electronico:* " + CorreoElectronico.get() + "\n"
        if Direccion.get():
            texto += "*Direccion:* " + Direccion.get() + "\n"
        if Maps.get():
            texto += "(" + Maps.get() + ")"
        #Borramos el texto que pueda haber quedado
        resultado.delete("1.0", tk.END)
        #Pegamos la variable texto en el entry resultado
        resultado.insert(tk.END, texto)
        #copiamos en el porta papeles la variable texto
        pyperclip.copy(texto)

    #Label y entry Nombre
    tk.Label(borde, text="PH y Nombre:").grid(row=1, column=0, sticky="w", pady=(0,10))
    nombre = tk.Entry(borde, width=30)
    nombre.grid(row=1, column=1, sticky="w", pady=(0,10))
    #Label y entry Materiales
    Label1 = tk.Label(borde, text="Materiales:")
    Label1.grid(row=2, column=0, sticky="w", pady=(0,10))

    #####

    items = tk.Text(borde, height=10, width=28)
    items.grid(row=2, column=1, sticky="w", pady=(0,10))
    #Label y Entry Contacto
    tk.Label(borde, text="Contacto:").grid(row=3, column=0, sticky="w", pady=(0,10))
    contacto = tk.Entry(borde, width=30)
    contacto.grid(row=3, column=1, sticky="w", pady=(0,10))
    #Label y Entry Telefono
    tk.Label(borde, text="Telefono:").grid(row=4, column=0, sticky="w", pady=(0,10))
    telefono = tk.Entry(borde, width=30)
    telefono.grid(row=4, column=1, sticky="w", pady=(0,10))
    #Label y Entry Correo Electronico
    tk.Label(borde, text="Correo Electronico:").grid(row=5, column=0, sticky="w", pady=(0,10))
    CorreoElectronico = tk.Entry(borde, width=30)
    CorreoElectronico.grid(row=5, column=1, sticky="w", pady=(0,10))
    #Label y Entry Direccion
    tk.Label(borde, text="Direccion:").grid(row=6, column=0, sticky="w", pady=(0,10))
    Direccion = tk.Entry(borde, width=30)
    Direccion.grid(row=6, column=1, sticky="w", pady=(0,10))
    #Label y Entry Maps
    tk.Label(borde, text="Maps:").grid(row=7, column=0, sticky="w", pady=(0,10))
    Maps = tk.Entry(borde, width=30)
    Maps.grid(row=7, column=1, sticky="w", pady=(0,10))
    # Boton Aceptar: ejecuta la funcion pasar
    boton = tk.Button(borde, text="Aceptar", command=pasar)
    boton.grid(row=8, column=0, sticky="n", pady=(0,10))
  
    #Label y Entry Resultado
    tk.Label(borde, text="Resultado:").grid(row=9, column=0, sticky="w", pady=(0,10))
    resultado = tk.Text(borde, height=10, width=28)
    resultado.grid(row=9, column=1, sticky="w", pady=(0,10))

    ventana.mainloop

def agregarOperador():
    #Funcion Agregar: agrega una opcion nueva al menuBar operadores y al txt que almacena los nombres de los operadores
    def agregar():
        #Obtenemos el nombre ingresado por el usuario
        texto = entry.get()
        if texto:
            try:
                #abrimos el archivo "Operadores.txt"
                with open("Operadores.txt", "a") as file:
                    #Escribimos el archivo con un salto de linea
                    file.write(texto + "\n")
                # Actualizamos el menu
                MenuOperador.add_command(label=texto, command=accionOperador(texto, 1))
                messagebox.showinfo("Éxito", "Línea agregada exitosamente.")
                #Cerramos la ventana emergente
                VentanaNuevoOperador.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error al agregar la línea: {e}")
        else:
            messagebox.showerror("Error", "Por favor, ingresa un texto.")

    #creacion y configuracion de la VentanaNuevoOperador
    VentanaNuevoOperador = tk.Toplevel(ventana)
    VentanaNuevoOperador.title("Agregar Línea")
    VentanaNuevoOperador.geometry("300x100")
    
    #creamos un frame para almacenar los Widgets
    marco = tk.Frame(VentanaNuevoOperador)
    marco.pack(pady=10)
    
    #Label
    tk.Label(marco, text="Ingresa la nueva línea:").pack(side=tk.LEFT)

    #Entry para ingresar el nombre del nuevo operador
    entry = tk.Entry(marco, width=30)
    entry.pack(side=tk.LEFT)

    #Boton para sentenciar la acción
    boton_agregar = tk.Button(VentanaNuevoOperador, text="Agregar", command=agregar)
    boton_agregar.pack()

def ReiniciarPrograma():
    # ReiniciarPrograma: destruimos la ventana para luego volverla a abrir, con la finalidad de actualizar el front
    ventana.destroy()
    # Ejecutamos nuevamente el archivo
    subprocess.call([sys.executable, 'reporte_operador3.py'])

def eliminarOperador():
    #EliminarOperador: quita el operador del menuBar Operadores y borra la linea del archivo Operadores.txt
    try:
        # Lee todas las líneas del archivo
        with open("Operadores.txt", "r") as file:
            lineas = file.readlines()

        # Elimina el nombre del operador seleccionado
        lineas = [linea for linea in lineas if linea.strip() != ventana.title().strip()]

        # Escribe las líneas restantes de vuelta en el archivo
        with open("Operadores.txt", "w") as file:
            for linea in lineas:
                file.write(linea)
        
        #Invocamos la funcion ReiniciarPrograma
        ReiniciarPrograma()

    except FileNotFoundError:
        print(f"El archivo Operadores.txt no fue encontrado.")

def agregarOperadores():
    #agregarOperadores: Creamos el menuBar Operadores 
    try:
        with open("Operadores.txt", "r") as file:
            #Bucle para añadir todos los operadores
            for linea in file:
                #Quitamos el salto de linea para evitar incompatibilidades
                clean = linea.strip()  # Eliminar el carácter \n
                #Añadimos el operador al MenuBar
                MenuOperador.add_command(label=clean, command=accionOperador(clean, 1))
    except FileNotFoundError:
        print(f"El archivo Operadores.txt no fue encontrado.")

def nombreOperador(event=None):
    #Funcion exclusiva para poder usar el atajo con Bind
    GuardarTexto(ventana.title())

def accionOperador(nombre_operador,codigo):
    #accionOperador: Funcion Exclusiva para compatibilizar las formas de guardar el texto en el codigo
    def inner():
        if codigo==1:
            cargar_texto(nombre_operador)    
        elif codigo==2:
            nombreOperador()
    return inner

def EnviarWhatsapp():
    #EnviarWhatsapp: cumple la funcion de realizar una secuencia de teclado que concluye en enviar el texto al primer chat de Whatsapp
    
    # Copiar el texto al portapapeles
    TextoPlanilla = EntryPrincipal.get("1.0", "end-1c")
    ventana.clipboard_clear()
    ventana.clipboard_append(TextoPlanilla)
    
    # Abrir WhatsApp y enviar el mensaje
    pyautogui.press('winleft')
    pyautogui.write('WhatsApp')
    pyautogui.press('enter')
    pyautogui.sleep(1)
    pyautogui.press('esc')
    pyautogui.sleep(1)
    pyautogui.press('tab')
    pyautogui.sleep(1)
    pyautogui.press('enter')
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.sleep(1)
    pyautogui.press('enter')
    pyautogui.sleep(1)
    pyautogui.press('esc')

def SeleccionarTodo(event=None):
    #Funcion Exclusiva para seleccionar todo el texto del EntryPrincipal
    EntryPrincipal.tag_add("sel", "1.0", "end")

def CortarTexto(event=None):
    #Funcion Exclusiva para realizar la accion de cortar la seleccion del texto con el atajo cntrl+v
    EntryPrincipal.event_generate("<<Cut>>")

def AcomodarTamanio(event=None):
    #Funcion Exclusiva para redimensionar la ventana y sus Widgets
    # Obtener el tamaño de la ventana
    width = ventana.winfo_width()
    height = ventana.winfo_height()
    
    # Ajustar el tamaño del Text
    EntryPrincipal.config(width=width-20, height=height//25)

def GuardarTexto(nombre_operador, event=None):
    # Guardar el texto en un archivo de texto correspondiente al nombre del operador
    nombre_operador=ventana.title()
    try:
        with open(f"{nombre_operador}.txt", "w") as file:
            file.write(EntryPrincipal.get("1.0", "end-1c"))
    except Exception as e:
        # Manejar cualquier excepción que ocurra durante la escritura en el archivo
        print(f"Error al guardar el texto: {e}")

def cargar_texto(nombre_operador):
    #Funcion exclusiva para cargar el texto de los archivos txt al entry
    try:
        #Le colocamos el nombre del operador a la ventana
        ventana.title(nombre_operador)
        with open(f"{nombre_operador}.txt", "r") as file:
            #Igualamos la variable al texto del archivo
            TextoGuardado = file.read()
            #Borramos el texto que tiene actualmente el entry
            EntryPrincipal.delete("1.0", tk.END)
            #Agregamos el texto del archivo txt
            EntryPrincipal.insert(tk.END, TextoGuardado)
    except FileNotFoundError:
        pass

#cargar configuracion
#Extraer configuracion de config.txt
with open("config.txt", "r") as file:
    lineas = file.readlines()  # Lee todas las líneas del archivo
LTamanio, res1, res2, nombre, tema = lineas
res=str(lineas[1].strip()) + "x" + str(lineas[2].strip())
tamanio=int(lineas[0].strip())
tema=lineas[4].strip()
print(tamanio,res,tema)
# Crear la ventana
ventana = tk.Tk()
ventana.title("NOVEDADES OPERADORES")
ventana.geometry(res)
# Establecer el icono de la ventana
ventana.iconbitmap('phoenix.ico')
# Configurar el evento de cambio de tamaño de la ventana
ventana.bind('<Configure>', AcomodarTamanio)
# Crear una fuente con el tamaño deseado
fuente = Font(family="Arial", size=tamanio)
# Configurar la nueva fuente como la fuente predeterminada para todos los widgets
ventana.option_add("*Font", fuente)
# Cambiamos el estilo de los botones
style = ttk.Style()
style.theme_use(tema)


# Declaro Menu
MenuSuperior = Menu(ventana)
ventana.config(menu=MenuSuperior)

# Archivo
MenuArchivo = Menu(MenuSuperior, tearoff=0)
MenuSuperior.add_cascade(label="Archivo", menu=MenuArchivo)
MenuArchivo.add_command(label="Operativa",command=operativa)
MenuArchivo.add_command(label="Guardar",command=accionOperador("",2))
MenuArchivo.add_command(label="Salir", command=ventana.quit)

# Opciones Operador
MenuOperador = Menu(MenuSuperior, tearoff=0)
MenuSuperior.add_cascade(label="Opciones", menu=MenuOperador)
MenuOperador.add_command(label="Enviar Novedades",command=EnviarWhatsapp)
MenuOperador.add_command(label="Agregar Operador",command=agregarOperador)
MenuOperador.add_command(label="Eliminar Operador",command=eliminarOperador)
MenuOperador.add_command(label="Configuracion",command=configuracion)

#Seleccionar Operador
MenuOperador = Menu(MenuSuperior, tearoff=0)
MenuSuperior.add_cascade(label="Operadores", menu=MenuOperador)
agregarOperadores()

#Creamos el Entry principal
EntryPrincipal = tk.Text(ventana, height=10, width=50)
EntryPrincipal.pack(fill=tk.BOTH, expand=True)

# Configurar atajos de teclado
EntryPrincipal.bind("<Control-a>", SeleccionarTodo)  # Seleccionar todo el texto
EntryPrincipal.bind("<Control-x>", CortarTexto)   # Cortar texto
EntryPrincipal.bind("<space>", nombreOperador) #guardar

# Configurar el evento de cierre de la ventana para guardar el texto
def CerrarVentana():
    ventana.destroy()

ventana.protocol("WM_DELETE_WINDOW", CerrarVentana)

# Ejecutar la ventana
ventana.mainloop()
