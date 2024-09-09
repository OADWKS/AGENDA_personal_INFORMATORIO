'''
[AGENDA_2024]

MEMO:
Se trata de una agenda de uso personal diseñada para organizar y gestionar tareas de la manera más eficiente posible, aunque es muy básica aún... Incluye funciones para guardar anotaciones en archivos .txt, lo que facilita 
el control detallado de las actividades registradas. Además, cuenta con un cronómetro para medir el tiempo dedicado a cada tarea, así como una calculadora que permite realizar cálculos sencillos cuando sea necesario. 
Un aspecto destacable es que la agenda está desarrollada en Tkinter, utilizando la librería personalizada "customtkinter", ésto se decidió para poder obtener una interfaz más atractiva.

'''
import tkinter as tk
import customtkinter as ctk
from datetime import datetime
import threading
import time
from tkcalendar import Calendar
from tkinter import filedialog, simpledialog ### import para lograr la interacción de la interfaz con el usuario a la hora de cargar las anotaciones {filedialog=abrir y guardar archivos}{simpledialog=para pedir los datos de las anotaciones}



## 01_CONFIGURACIÓN DE LA APARIENCIA Y TEMA DE LA INTERFAZ ##
ctk.set_appearance_mode("system") 
ctk.set_default_color_theme("blue")

'''
Se configuró la apariencia en función del sistema del usuario que lo ejecute teniendolo a éste como prioridad. En el caso que el usuario tenga el tema del sistema en oscuro, la interfaz de la agenda se verá
en tonos oscuros. Como color_theme se eligió dejar el color azul default de Ctkinter ya que era el que mejor contraste presentaba.

'''


# 02_VENTANA PRINCIPAL
root = ctk.CTk()
root.geometry("440x840")
root.title("AGENDA de ANDREA")



## 03_FUNCIONES ##
def actualizar_reloj():
    reloj_etiqueta.configure(text=datetime.now().strftime("%H:%M:%S"))
    root.after(1000, actualizar_reloj) 

## 03.1_FUNCIÓN_CRONÓMETRO ##    
## 03.2_VARIABLE GLOBAL ##
corriendo = False
tiempo_transcurrido = 0 ### nos había dado error y no podíamos iniciar el cronómetro desde 0, tuvimos que agregar una variable para poder gestionar el estado inicial, de otra manera no iniciaba.

def iniciar_cronometro():
    global corriendo
    if not corriendo:
        corriendo = True
        cronometro_thread = threading.Thread(target=ejecutar_cronometro, daemon=True)
        cronometro_thread.start()

def ejecutar_cronometro():
    global corriendo, tiempo_transcurrido
    tiempo_inicio = time.time()
    while corriendo:
        tiempo_transcurrido = int(time.time() - tiempo_inicio)
        etiqueta_cronometro.configure(text=f"Tiempo transcurrido: {tiempo_transcurrido} segundos")
        time.sleep(1)

def detener_cronometro():
    global corriendo
    corriendo = False

def reiniciar_cronometro():
    global tiempo_transcurrido
    tiempo_transcurrido = 0
    etiqueta_cronometro.configure(text="Tiempo transcurrido: 0 segundos")


## 03.3_FUNCIÓN_VENTANAS ##
def mostrar_frame(nombre_frame): ### decidimos optar por una interfaz que no muestre todas las funciones en una sola ventana si no que oculte, en función de la elección, una u otra.
    frame_lista_tareas.pack_forget()
    frame_anotaciones.pack_forget()
    frame_cronometro.pack_forget()
    frame_calculadora.pack_forget()
    
    if nombre_frame == "Lista de tareas":
        frame_lista_tareas.pack(pady=20, fill=tk.BOTH, expand=True)
    elif nombre_frame == "Anotaciones":
        frame_anotaciones.pack(pady=20, fill=tk.BOTH, expand=True)
    elif nombre_frame == "Cronómetro":
        frame_cronometro.pack(pady=20, fill=tk.BOTH, expand=True)
    elif nombre_frame == "Calculadora":
        frame_calculadora.pack(pady=20, fill=tk.BOTH, expand=True) ### por lo tanto para poder ir de ventana en ventana, con el menú desplegable, decidimos ocultar con condicional lo que no se iba a ver.
 

## 03.4_FUNCIÓN_LISTA DE TAREAS ##
def mostrar_mensaje(mensaje):
    mensaje_label.configure(text=mensaje)  ### creamos ésta función para que en caso de que se opriman los botones "agregar tarea" o "eliminar tarea" sin haber escrito o seleccionado nada, no diera error sino que imprimiría en pantalla la faltante.

def agregar_tarea():
    titulo_tarea = entrada_tarea.get().strip()
    if titulo_tarea:
        lista_tareas.insert(tk.END, titulo_tarea)
        entrada_tarea.delete(0, tk.END)
        mostrar_mensaje("")  ### para agregar la tarea
    else:
        mostrar_mensaje("El título de la tarea no puede estar vacío.")  

def eliminar_tarea():
    if lista_tareas.curselection():
        lista_tareas.delete(lista_tareas.curselection()[0])
        mostrar_mensaje("")  ### para ver la tarea eliminada
    else:
        mostrar_mensaje("Selecciona una tarea para eliminar.")


## 03.5_FUNCIÓN_CALCULADORA ##
def calcular_expresion(expresion):
    try:
        resultado = eval(expresion) ### utilizamos la función eval para poder ejecutar los cálculos dadnole una expresión dictada en la interfaz. (según fuentes de py, eval puede ser peligrosa porque admite entrada de códigos malisiosos pero era la forma en la que no daba error)
        entrada_calculadora.delete(0, tk.END)
        entrada_calculadora.insert(tk.END, str(resultado)) 
    except Exception as error: ### aplicamos la variable error en caso de hacer alguna operación imposible de ejecutar, el error ya está preprogramado en caso de que exista.
        entrada_calculadora.delete(0, tk.END)
        entrada_calculadora.insert(tk.END, "Error") 

def click_boton(valor_boton):
    texto_actual = entrada_calculadora.get() 
    nuevo_texto = texto_actual + str(valor_boton) ### aplicamos un string para poder ejecutar como cadena los valores dispuestos en la interfaz, de ésta manera podemos concatenar el texto actual con el nuevo texto que vayamos a poner.
    entrada_calculadora.delete(0, tk.END)
    entrada_calculadora.insert(tk.END, nuevo_texto) ### para poder ejecutar de manera continua la calculadora, aplicamos un nuevo texto que se mostrará con el valor actualizado de la nueva operación.

def limpiar_entrada():
    entrada_calculadora.delete(0, tk.END) 


## 03.6_FUNCIÓN_ANOTACIONES ##
def guardar_notas():
    archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")]) ### utilizamos el método filedialog para iniciar el diálogo con el usuario, definimos solamente archivos .txt para evitar errores.
    if archivo:
        try:
            with open(archivo, 'w') as archivo: ### utilizamos archivo para determinar la ruta de guardado, si ya existe se reescribirá el nuevo archivo que se guardará. Con el "with" aseguramos que se cierre el archivo sin tener errores.
                archivo.write(caja_texto_anotaciones.get("1.0", tk.END)) ### aquí lo mismo que antes, determinamos el inicio y final del texto dentro de las anotaciones.
        except Exception as e:
            print(f"Error al guardar las notas: {e}")

def cargar_notas():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'r') as file:
                contenido = file.read()
                caja_texto_anotaciones.delete("1.0", tk.END) ### utilizamos ésto para borrar las anotaciones ubicando un princiio "1.0" y un final.
                caja_texto_anotaciones.insert(tk.END, contenido) ### y éste para poder reemplazarlo por otro insertando el nuevo texto, sin tener un error en caso de sopreponer un archivo .txt nuevo a uno que se estaba utilizando.
        except FileNotFoundError:
            print("No se encontró el archivo de notas.") 
        except Exception as e:
            print(f"Error al cargar las notas: {e}")

def cambiar_fuente(tamaño):
    caja_texto_anotaciones.configure(font=("Arial", int(tamaño))) ### agregamos ésta función para poder agrandar de forma manual la altura de la fuente, pudiendo con los parámetros cambiar el tipo de fuente o tamaño.

'''

En el caso de las funciones el lenguaje de Ctkinter es muy similar al de Tkinter, sacando algunas excepciones como .configure en vez de .config. Por lo que la mayoría del código se mantiene similar a como si lo 
hubieramos hecho con la librería de Tkinter. Encontramos mucho más cómodo la interfaz propuesta por Ctkinter por eso decidimos hacer en su totalidad con dicha librería.

'''


## 04_INTERFAZ_VENTANAS ##

## 04.1_MENÚ DESPLEGABLE ##
menu = ctk.CTkOptionMenu(root, values=["Lista de tareas", "Anotaciones", "Cronómetro", "Calculadora"], command=mostrar_frame)
menu.pack(pady=10, anchor='ne', fill=tk.X)
menu.configure(width=root.winfo_width())

## 04.2_RELOJ GLOBAL ##
reloj_etiqueta = ctk.CTkLabel(root, text="", font=("Times New Roman", 100))
reloj_etiqueta.pack(pady=10)
actualizar_reloj()

## 04.3_VENTANA_LISTA DE TAREAS ##
frame_lista_tareas = ctk.CTkFrame(root)
frame_lista_tareas.pack(pady=20, padx=20)

etiqueta_lista_tareas = ctk.CTkLabel(frame_lista_tareas, text="Lista de tareas", font=("Arial", 18))
etiqueta_lista_tareas.pack(pady=10)

frame_lista_tareasbox = ctk.CTkFrame(frame_lista_tareas)
frame_lista_tareasbox.pack(pady=10, fill=tk.BOTH, expand=True)

scroll_lista_tareas = ctk.CTkScrollbar(frame_lista_tareasbox, orientation="vertical")
scroll_lista_tareas.pack(side=tk.RIGHT, fill=tk.Y)

lista_tareas = tk.Listbox(
    frame_lista_tareasbox,
    yscrollcommand=scroll_lista_tareas.set,
    selectmode=tk.SINGLE)

lista_tareas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scroll_lista_tareas.configure(command=lista_tareas.yview)

entrada_tarea = ctk.CTkEntry(frame_lista_tareas, placeholder_text="Título de la tarea")
entrada_tarea.pack(pady=10)

boton_agregar_tarea = ctk.CTkButton(frame_lista_tareas, text="Agregar Tarea", command=agregar_tarea)
boton_agregar_tarea.pack(pady=10)

boton_eliminar_tarea = ctk.CTkButton(frame_lista_tareas, text="Eliminar Tarea", command=eliminar_tarea)
boton_eliminar_tarea.pack(pady=10)

mensaje_label = ctk.CTkLabel(frame_lista_tareas, text="", text_color="red")  ### se decidió que el mensaje en caso de que no se ejecute nada sea en color rojo para mejor contraste
mensaje_label.pack(pady=10)

## 04.4_VENTANA_ANOTACIONES ##
frame_anotaciones = ctk.CTkFrame(root)
etiqueta_anotaciones = ctk.CTkLabel(frame_anotaciones, text="Anotaciones", font=("Arial", 18))
etiqueta_anotaciones.pack(pady=10)


#### 04.4.1_CONTENEDOR_AREA DE BOTONES Y TEXTO ####
frame_anotaciones_content = ctk.CTkFrame(frame_anotaciones)
frame_anotaciones_content.pack(pady=10, fill=tk.BOTH, expand=True)

caja_texto_anotaciones = ctk.CTkTextbox(frame_anotaciones_content, width=600, height=300, wrap=tk.WORD)
caja_texto_anotaciones.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scroll_anotaciones = ctk.CTkScrollbar(frame_anotaciones_content, orientation="vertical", command=caja_texto_anotaciones.yview)
scroll_anotaciones.pack(side=tk.RIGHT, fill=tk.Y)
caja_texto_anotaciones.configure(yscrollcommand=scroll_anotaciones.set)

boton_menor_fuente = ctk.CTkButton(frame_anotaciones, text="A -", command=lambda: cambiar_fuente("10"))
boton_menor_fuente.pack(side=tk.LEFT, padx=5, pady=5)

boton_mayor_fuente = ctk.CTkButton(frame_anotaciones, text="A +", command=lambda: cambiar_fuente("20"))
boton_mayor_fuente.pack(side=tk.LEFT, padx=5, pady=5)

boton_guardar = ctk.CTkButton(frame_anotaciones, text="Guardar Notas", command=guardar_notas)
boton_guardar.pack(side=tk.LEFT, padx=5, pady=5)

boton_cargar = ctk.CTkButton(frame_anotaciones, text="Cargar Notas", command=cargar_notas)
boton_cargar.pack(side=tk.LEFT, padx=5, pady=5)


## 04.4_VENTANA_CRONÓMETRO ##
frame_cronometro = ctk.CTkFrame(root)
etiqueta_cronometro = ctk.CTkLabel(frame_cronometro, text="Tiempo transcurrido: 0 segundos", font=("Arial", 18))
etiqueta_cronometro.pack(pady=10)

boton_iniciar_cronometro = ctk.CTkButton(frame_cronometro, text="Iniciar Cronómetro", command=iniciar_cronometro)
boton_iniciar_cronometro.pack(pady=5)

boton_detener_cronometro = ctk.CTkButton(frame_cronometro, text="Detener Cronómetro", command=detener_cronometro)
boton_detener_cronometro.pack(pady=5)

boton_reiniciar_cronometro = ctk.CTkButton(frame_cronometro, text="Reiniciar Cronómetro", command=reiniciar_cronometro)
boton_reiniciar_cronometro.pack(pady=5)

## 04.5_VENTANA_CALCULADORA ##
frame_calculadora = ctk.CTkFrame(root)
etiqueta_calculadora = ctk.CTkLabel(frame_calculadora, text="Calculadora", font=("Arial", 18))
etiqueta_calculadora.grid(row=0, column=0, columnspan=4, pady=10)

entrada_calculadora = ctk.CTkEntry(frame_calculadora, width=300, justify='right')
entrada_calculadora.grid(row=1, column=0, columnspan=4, pady=10)

#### 04.5.1_DISEÑO_BOTONES
botones = [
    ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3),
    ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3),
    ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
    ('0', 5, 0), ('.', 5, 1), ('+', 5, 2), ('=', 5, 3),
    ('C', 6, 0),] ### el diseño de botones lo hicimos de manera en que nos quede {lista=tupla=("elemento","fila","columna")}, de ésta manera era más sencillo sin tener que hacer un botón por cada número o símbolo.

for (texto, fila, columna) in botones:
    if texto == '=':
        boton = ctk.CTkButton(frame_calculadora, text=texto, command=lambda: calcular_expresion(entrada_calculadora.get())) ### utilizamos lambda como palabra clave para poder ejecutar la función que hará el cálculo una vez que se apriete la tecla "=".
    elif texto == 'C':
        boton = ctk.CTkButton(frame_calculadora, text=texto, command=limpiar_entrada) ### utilizamos éste botón para poder borrar los elementos mostrados en pantalla.
    else:
        boton = ctk.CTkButton(frame_calculadora, text=texto, command=lambda txt=texto: click_boton(txt)) ### utilizamos lambda para generar la función del contexto específico, no definimos por nombre de función.
    boton.grid(row=fila, column=columna, padx=5, pady=5, sticky="nsew")

#### 04.5.2_DISEÑO_RESPONSIVE
for i in range(7): ### agarramos dentro del rango 0 a 6, del frame de la calculadora.
    frame_calculadora.grid_rowconfigure(i, weight=1)  ### utilizamos para modificar uniformemente todas las filas con un valor ascendente o descendente proporcional, de ésta manera podemos mantener uniformemente las distancias y proporciones.
for j in range(4): ### agarramos dentro del rango 0 a 3, del frame de la calculadora.
    frame_calculadora.grid_columnconfigure(j, weight=1)  ### utilizamos para modificar uniformemente todas las filas con un valor ascendente o descendente proporcional, de ésta manera podemos mantener uniformemente las distancias y proporciones.


## 04.6_VENTANA_POR DEFECTO_LISTA DE TAREAS ##
mostrar_frame("Lista de tareas")

root.mainloop()

