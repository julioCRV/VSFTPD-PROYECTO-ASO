import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import ttk

class VSFTPDConfigEditor:
    def __init__(self, root, funcion_volver):
        self.root = root
        self.funcion_volver = funcion_volver
        self.root.title("VSFTPD Config Editor")
        self.centrar_ventana()
        
        # Atributo de instancia para almacenar las líneas del archivo
        self.lines = [] 
        # Lista de numeros y datos fitrados sin comentarios de configuraciones de vsftpd
        self.Lista_Numeros_dato = []

        # Contiene la lista actual de datos del formulario ("write_enable")
        self.formulario_datos = []  
        # Contiene la lista actual de opciones del formulario ("YES" o "NO" o "editable")
        self.opciones = []
        # Contiene le numero de la lista de Tupla que tiene numero y datos Lista_Numeros_datos
        self.formulario_numero_lista = []

        # Contiene la lista de datos que no estan en el formulario se encuentran comentando #
        self.formulario_no_datos = []  
        # Contiene el numero de lista de dato que no se encuentra en el formulario por estar comentado #
        self.formulario_no_numero_lista = []
        
        # Datos reservados para los inputs de entrada
        self.texto_valores = []

        # Categorizacion
        self.general_settings = []
        self.local_settings = []
        self.anonymus_settings = []
        self.log_settings = []
        self.transfer_settings = []
        self.other_settings = []

        # Crear 6 secciones independientes con botones
        self.frame_seccion1 = tk.Frame(self.root, borderwidth=2, relief=tk.GROOVE)
        self.frame_seccion1.place(x=10, y=80, width=220, height=400)
        self.frame_seccion2 = tk.Frame(self.root, borderwidth=2, relief=tk.GROOVE)
        self.frame_seccion2.place(x=230, y=80, width=220, height=400)
        self.frame_seccion3 = tk.Frame(self.root, borderwidth=2, relief=tk.GROOVE)
        self.frame_seccion3.place(x=450, y=80, width=220, height=400)
        self.frame_seccion4 = tk.Frame(self.root, borderwidth=2, relief=tk.GROOVE)
        self.frame_seccion4.place(x=670, y=80, width=220, height=400)
        self.frame_seccion5 = tk.Frame(self.root, borderwidth=2, relief=tk.GROOVE)
        self.frame_seccion5.place(x=890, y=80, width=220, height=400)
        self.frame_seccion6 = tk.Frame(self.root, borderwidth=2, relief=tk.GROOVE)
        self.frame_seccion6.place(x=1110, y=80, width=220, height=400)

        self.frame_actual = self.frame_seccion1

        # Crear etiqueta de nombre
        self.label1 = tk.Label(self.root, text="General Settings", width=100, anchor="w")
        self.label1.place(x=10, y=60)
        self.label2 = tk.Label(self.root, text="Local FTP user Settings", width=100, anchor="w")
        self.label2.place(x=230, y=60)
        self.label3 = tk.Label(self.root, text="Anonymus FTP user Settings", width=100, anchor="w")
        self.label3.place(x=450, y=60)
        self.label4 = tk.Label(self.root, text="Log Settings", width=100, anchor="w")
        self.label4.place(x=670, y=60)
        self.label5 = tk.Label(self.root, text="Transfer Settings", width=100, anchor="w")
        self.label5.place(x=890, y=60)
        self.label6 = tk.Label(self.root, text="security features that are \n incompatible with some other settings", width=100, anchor="w")
        self.label6.place(x=1110, y=40)

        #Metodos que inicializan la ventana
        self.load_config()
        self.dividir_en_secciones()
        #self.general()
        self.load_formulario()

        #Botones que se encuentran ubicados en la ventana
        self.agregar_button = tk.Button(self.root, text="Agregar", command=self.agregar_datos_formulario,background="#43fef6")
        self.eliminar_button = tk.Button(self.root, text="Eliminar", command=self.eliminar_datos_formulario,background="#43fef6")
        self.button_configuracion = tk.Button(self.root, text="< volver", command=self.abrir_ventana_configuracion,background="#43fef6")
        self.button_actualizar = tk.Button(self.root, text="Actualizar", command=self.actualilzar_formulario,background="#43fef6")

        #Posicion de los botones
        self.agregar_button.place(x=400, y=10)
        self.eliminar_button.place(x=500, y=10)
        self.button_configuracion.place(x=10,y=10)
        self.button_actualizar.place(x=300, y=10)


#------------------------------------------------------------------------------------------
    def dividir_en_secciones(self):
        #print(self.Lista_Numeros_dato)
        titulo_config = ["# General Settings","# Local FTP user Settings", "# Anonymus FTP user Settings", "# Log Settings","# Transfer Settings", "### security features that are incompatible with some other settings. ###" ]
        pos_config = 0
        pos_lista = 0
        while pos_lista < len(self.Lista_Numeros_dato):
            num, linea = self.Lista_Numeros_dato[pos_lista]
            if  pos_config<len(titulo_config):
                if titulo_config[pos_config] in linea:
                    pos = self.Lista_Numeros_dato.index((num,linea)) + 1
                    for num2, linea2 in self.Lista_Numeros_dato[pos:]: 
                        if linea2.strip().startswith("# ") or linea2.strip().startswith("###"):
                            pos_lista = self.Lista_Numeros_dato.index((num2, linea2))
                            break
                        if pos_config==0:
                            self.general_settings.append((num2, linea2))
                        elif pos_config==1:
                            self.local_settings.append((num2, linea2))
                        elif pos_config==2:
                            self.anonymus_settings.append((num2, linea2))
                        elif pos_config==3:
                            self.log_settings.append((num2, linea2))
                        elif pos_config==4:
                            self.transfer_settings.append((num2, linea2))
                        elif pos_config==5:
                            self.other_settings.append((num2, linea2))
            else:
                pos_lista = pos_lista + 1        
            pos_config = pos_config + 1
             
            #print("general --> ",self.general_settings)
            #print("user --> ",self.local_settings)
            #print("anonymus --> ",self.anonymus_settings)
            #print("log --> ",self.log_settings)
            #print("transfer --> ",self.transfer_settings)
            #print("other --> ",self.other_settings)
    
    def actualilzar_formulario(self):
        self.inicializar()
        self.inicializar_botones()
        self.load_config()
        self.load_formulario()        

    def general(self):
        #self.load_formulario2(self.general_settings,self.frame_seccion1)
        #self.load_formulario2(self.local_settings,self.frame_seccion2)
        #self.load_formulario2(self.anonymus_settings,self.frame_seccion3)
        #self.load_formulario2(self.log_settings,self.frame_seccion4)
        self.load_formulario2(self.transfer_settings,self.frame_seccion5)
        #self.load_formulario2(self.other_settings,self.frame_seccion6)
#------------------------------------------------------------------------------------------

    def inicializar(self):
        self.lines = [] 
        self.Lista_Numeros_dato = []
        self.formulario_datos = []  
        self.opciones = []
        self.formulario_numero_lista = []
        self.formulario_no_datos = []  
        self.formulario_no_numero_lista = []
        self.texto_valores = []
        self.general_settings = []
        self.local_settings = []
        self.anonymus_settings = []
        self.log_settings = []
        self.transfer_settings = []
        self.other_settings = []

         # Crear 6 secciones independientes con botones
        self.frame_seccion1 = tk.Frame(self.root, borderwidth=2, relief=tk.GROOVE)
        self.frame_seccion1.place(x=10, y=80, width=220, height=400)

        self.frame_seccion2 = tk.Frame(self.root, borderwidth=2, relief=tk.GROOVE)
        self.frame_seccion2.place(x=230, y=80, width=220, height=400)

        self.frame_seccion3 = tk.Frame(self.root, borderwidth=2, relief=tk.GROOVE)
        self.frame_seccion3.place(x=450, y=80, width=220, height=400)

        self.frame_seccion4 = tk.Frame(self.root, borderwidth=2, relief=tk.GROOVE)
        self.frame_seccion4.place(x=670, y=80, width=220, height=400)

        self.frame_seccion5 = tk.Frame(self.root, borderwidth=2, relief=tk.GROOVE)
        self.frame_seccion5.place(x=890, y=80, width=220, height=400)

        self.frame_seccion6 = tk.Frame(self.root, borderwidth=2, relief=tk.GROOVE)
        self.frame_seccion6.place(x=1110, y=80, width=220, height=400)

        self.frame_actual = self.frame_seccion1

        # Crear etiqueta de nombre
        self.label1 = tk.Label(self.root, text="General Settings", width=100, anchor="w")
        self.label1.place(x=10, y=60)
        self.label2 = tk.Label(self.root, text="Local FTP user Settings", width=100, anchor="w")
        self.label2.place(x=230, y=60)
        self.label3 = tk.Label(self.root, text="Anonymus FTP user Settings", width=100, anchor="w")
        self.label3.place(x=450, y=60)
        self.label4 = tk.Label(self.root, text="Log Settings", width=100, anchor="w")
        self.label4.place(x=670, y=60)
        self.label5 = tk.Label(self.root, text="Transfer Settings", width=100, anchor="w")
        self.label5.place(x=890, y=60)
        self.label6 = tk.Label(self.root, text="security features that are \n incompatible with some other settings", width=100, anchor="w")
        self.label6.place(x=1110, y=40)

    def inicializar_botones(self):
        #Botones que se encuentran ubicados en la ventana
        self.agregar_button = tk.Button(self.root, text="Agregar", command=self.agregar_datos_formulario,background="#43fef6")
        self.eliminar_button = tk.Button(self.root, text="Eliminar", command=self.eliminar_datos_formulario,background="#43fef6")
        self.button_configuracion = tk.Button(self.root, text="< volver", command=self.abrir_ventana_configuracion,background="#43fef6")

        #Posicion de los botones
        self.agregar_button.place(x=400, y=10)
        self.eliminar_button.place(x=500, y=10)
        self.button_configuracion.place(x=10,y=10)
            
    def es_linea_valida(self, linea):
        # Agrega aquí otras validaciones según sea necesario
        if "# General Settings" in linea:
            return True
        elif "# Local FTP user Settings" in linea:
            return True
        elif "# Anonymus FTP user Settings" in linea:
            return True
        elif "# Log Settings" in linea:
            return True
        elif "# Transfer Settings" in linea:
            return True
        elif "### security features that are incompatible with some other settings. ###" in linea:
            return True
        elif not linea.strip().startswith("# "):
            return True

#---------------------------- Exclusivamente para guardar y cargar VSFTPD.conf --------------------------------------------

    def load_config(self):
        try:
            with open("/etc/vsftpd.conf", "r") as file:
                self.lines = file.readlines()

                # 1er Filtro de "self.lines" de la lista todas las lineas o elementos que NO tengan "#" al comenzar
                lines2 = [(num, line.strip()) for num, line in enumerate(self.lines, start=1) if self.es_linea_valida(line)]
                #print(f"1er filtro: ---> {lines2}\n")


                # 2do Filtro de la lista "lines2" se selecciona las lineas o elementos que tengan un de 2 a 70 caracteres
                self.Lista_Numeros_dato= [(num, line) for num, line in lines2 if len(line.strip()) != 1 and len(line) <= 75]
                #print(f"2do filtro: ---> {self.Lista_Numeros_dato}\n")
                
                # 3er Filtro de la lista "self.Lista_Numeros_datos", se selecciona las lineas que no tengan un espacio
                # contiene todas las configuraciones con # o sin # comentados
                self.Lista_Numeros_dato= [(num, line) for num, line in self.Lista_Numeros_dato if line.strip() != ""]
                #print(f"3er filtro: ---> {self.Lista_Numeros_dato}\n")   
        except FileNotFoundError:
            messagebox.showerror("Error", "El archivo vsftpd.conf no existe.")
    
    def save_config(self):
        try:
            with open("/etc/vsftpd.conf", "w") as file:
                content = "".join(self.lines)
                file.write(content)
            #messagebox.showinfo("Guardado", "El archivo vsftpd.conf ha sido guardado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el archivo: {str(e)}") 

    def modificar_linea(self, numero_linea, nuevo_contenido):
        if 1 <= numero_linea <= len(self.lines):
            self.lines[numero_linea - 1] = nuevo_contenido + '\n'
            print(f"Línea {numero_linea} modificada.")
        else:
            print(f"Número de línea {numero_linea} fuera de rango.")

#---------------------------------------- Creacion del formulario --------------------------------------------
    def load_formulario(self):  
        #tupla[0] contine los numeros y tupla[1] los datos
        #print(self.Lista_Numeros_dato)
        for tupla in self.Lista_Numeros_dato:
        #for tupla in lista_clasificada:
            nuevo_elemento = tupla[1]  #Dato de configuracion
            nuevo_elemento2 = tupla[0] #El numero en la lista
            
            #                 posicion el la lista    dato configuracion
            # filtrar de Lista tupla ("19","write_enable=yes") solo el dato que nos interesa
            if not nuevo_elemento.startswith("#"):
                self.formulario_datos.append(nuevo_elemento)
                self.formulario_numero_lista.append(nuevo_elemento2)
                #print(f"estoy aqui: {self.formulario_numero_lista} y {self.formulario_datos}")
            elif nuevo_elemento.startswith("# ") or nuevo_elemento.startswith("###"):
                self.formulario_datos.append(nuevo_elemento)
                self.formulario_numero_lista.append(nuevo_elemento2)
                self.formulario_no_datos.append(nuevo_elemento)
                self.formulario_no_numero_lista.append(nuevo_elemento2)
            else:
                self.formulario_no_datos.append(nuevo_elemento)
                self.formulario_no_numero_lista.append(nuevo_elemento2)
        # Crear tk.StringVar para ser enlazada a los widget de comboBox
        self.opciones = [tk.StringVar(value="Sí") for _ in range(len(self.formulario_datos))]
        self.texto_valores = [tk.StringVar(value="") for _ in range(len(self.formulario_numero_lista))]
         # Lista para almacenar las variables de los checkboxes
        self.checkbox_vars = [tk.BooleanVar(value=False) for _ in range(len(self.formulario_no_numero_lista))]
        #print(self.opciones)
        #print([f"{line}" for num, line in ListaConNum])
        self.crear_tabla()     

    def devolver_frame(self, linea):
        # Agrega aquí otras validaciones según sea necesario
        if "# General Settings" in linea:
            self.frame_actual=self.frame_seccion1
            return self.frame_seccion1
        elif "# Local FTP user Settings" in linea:
            self.frame_actual=self.frame_seccion2
            return self.frame_seccion2
        elif "# Anonymus FTP user Settings" in linea:
            self.frame_actual=self.frame_seccion3
            return self.frame_seccion3
        elif "# Log Settings" in linea:
            self.frame_actual=self.frame_seccion4
            return self.frame_seccion4
        elif "# Transfer Settings" in linea:
            self.frame_actual=self.frame_seccion5
            return self.frame_seccion5
        elif "### security features that are incompatible with some other settings. ###" in linea:
            self.frame_actual=self.frame_seccion6
            return self.frame_seccion6
        else:
            return self.frame_actual

    def crear_tabla(self):
        # Crear filas de la tabla
        
        for i, nombre in enumerate(self.formulario_datos):
            
            #print(nombre)
            fila_frame = tk.Frame(self.devolver_frame(nombre))
            fila_frame.pack(side="top", pady=2)
            
            ####################################################################################
            if "=" in nombre:
                partes = nombre.split("=")

                # Obtener las dos partes
                nombre = partes[0]
                estado_yn = partes[1]
                self.formulario_datos[i]=nombre
                ####################################################################################

                # Crear etiqueta de nombre
                tk.Label(fila_frame, text=nombre, width=15, anchor="w").pack(side="left")
                
                ####################################################################################
                if estado_yn == "YES":
                    estado2_yn = "NO"
                else:
                    estado2_yn = "YES"
                ####################################################################################

                if estado_yn == "YES" or estado_yn =="NO":
                    # Crear botón deslizante (combobox) y vincular la función de actualización
                    combo_box = ttk.Combobox(fila_frame, values=[estado_yn,estado2_yn], textvariable=self.opciones[i], state="readonly", width=5)
                    combo_box.current(0)  # Establecer la opción predeterminada
                    combo_box.pack(side="left", padx=(0, 55))
                    
                    # Vincular la función de actualización al cambio de valor en el Combobox
                    combo_box.bind("<<ComboboxSelected>>", lambda event, index=i: self.actualizar_lista(index))
                else:
                    
                    # Crear cuadro de texto (readonly)
                    cuadro_texto = tk.Entry(fila_frame, textvariable=self.texto_valores[i], width=15, state="readonly")
                    self.texto_valores[i].set(estado_yn)
                    cuadro_texto.pack(side="left")

                    # Asociar evento de clic al cuadro de texto
                    cuadro_texto.bind("<Button-1>", lambda event, index=i: self.abrir_ventana_edicion(index))
            else:

                continue

    def abrir_ventana_edicion(self, index):
        # Función para abrir la ventana de edición
        ventana_edicion = tk.Toplevel(self.root)
        ventana_edicion.title("Editar datos")
        self.centrar_ventana2(ventana_edicion, 300, 100)        

        # Cuadro de texto para la edición
        self.cuadro_texto = tk.Entry(ventana_edicion, textvariable=self.texto_valores[index], width=25)
        # Posicionar el cursor al final
        self.cuadro_texto.icursor(tk.END)
        self.cuadro_texto.pack(pady=15)
        
        # Botón de guardar
        boton_guardar = tk.Button(ventana_edicion, text="Guardar", command=lambda: self.guardar_cambios(index, ventana_edicion))
        boton_guardar.pack(pady=10)

        # Enfocar el cuadro de texto automáticamente
        self.cuadro_texto.focus_set()  

    def guardar_cambios(self, index, ventana_edicion):
        # Función para guardar los cambios y cerrar la ventana de edición
        self.texto_valores[index].set(self.cuadro_texto.get())
        dato_modificado = self.formulario_datos[index] + "=" + self.texto_valores[index].get()

        self.modificar_linea(self.formulario_numero_lista[index], dato_modificado)
        self.save_config()
        self.load_config()
        ventana_edicion.destroy()
 
    def actualizar_lista(self, index):
        # Función para actualizar la lista cuando cambia el valor en un Combobox
        self.imprimir_tabla()
        #print(f"Se cambió la opción para {self.formulario_datos[index]} a {self.opciones[index].get()}")
        dato_modificado = self.formulario_datos[index] + "=" + self.opciones[index].get()

        self.modificar_linea(self.formulario_numero_lista[index], dato_modificado)
        self.save_config()
        self.load_config()

#----------------------- Funcionalidad de agregar y borrar datos del formulario -------------------------------

    def agregar_datos_formulario(self):
        # Función para abrir la ventana de edición
        ventana_agregar = tk.Toplevel(self.root)
  
        ventana_agregar.title("Agregar nuevos datos a la tabla")
        self.centrar_ventana2(ventana_agregar, 600, 700)  
        # Crear canvas con scrollbar vertical
        canvas = tk.Canvas(ventana_agregar)
        scrollbar = tk.Scrollbar(ventana_agregar, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame interior para los checkboxes
        frame_interior = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame_interior, anchor="nw")

        # Crear checkboxes y asociar a variables
        for i, dato in enumerate(self.formulario_no_datos):
            if(self.es_una_configuracion(dato)):
                # Frame para alinear datos y checkbox horizontalmente
                frame = tk.Frame(frame_interior)
                frame.pack(anchor="w", pady=0)

                # Etiqueta para mostrar el dato
                label = tk.Label(frame, text=dato)
                label.pack(side="right")
            else:
                # Elimina el # de todos lo datos #write_enable --> write_enable
                dato = dato.lstrip('#')
                # Frame para alinear datos y checkbox horizontalmente
                frame = tk.Frame(frame_interior)
                frame.pack(anchor="w", pady=0)

                # Etiqueta para mostrar el dato
                label = tk.Label(frame, text=dato)
                label.pack(side="right")

                # Crear checkbox y asociar a variable
                checkbox = tk.Checkbutton(frame, variable=self.checkbox_vars[i])
                checkbox.pack(side="right")
            
        frame = tk.Frame(frame_interior)
        frame.pack(anchor="w", side="right")

         # Botón para imprimir el estado de los checkboxes
        btn_agregar_datos = tk.Button(frame, text="Agregar datos", command=lambda :self.mostrar_modal_confirmacion_agregar(ventana_agregar))
        btn_agregar_datos.pack(pady=1)

        # Configurar el canvas para el scrollbar
        frame_interior.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all")) 

    def mostrar_modal_confirmacion_agregar(self, ventana_agregar):
        # Crear una nueva ventana (cuadro de diálogo) utilizando Toplevel
        ventana_confirmacion = tk.Toplevel(self.root)
        ventana_confirmacion.title("Confirmación")
        
        # Agregar etiqueta y botones al cuadro de diálogo
        label = tk.Label(ventana_confirmacion, text="¿Estás seguro de añadir los datos?")
        label.pack(pady=10)

        # Botón "Guardar"
        btn_guardar = tk.Button(ventana_confirmacion, text="Guardar", command=lambda: self.agregar_formulario(ventana_confirmacion))
        btn_guardar.pack(side="left", padx=10)

        # Botón "Cancelar"
        btn_cancelar = tk.Button(ventana_confirmacion, text="Cancelar", command=ventana_confirmacion.destroy)
        btn_cancelar.pack(side="left", padx=10)
          
        # Centrar la ventana de confirmación sobre la ventana principal
        self.centrar_ventana3(ventana_confirmacion)
        ventana_agregar.destroy()
        
    def agregar_formulario(self, ventana_confirmacion):
        # Imprimir el estado de los checkboxes
        # Función para guardar los cambios y cerrar la ventana de edición
        for index, dato in enumerate(self.formulario_no_datos):
            if self.checkbox_vars[index].get():
                dato = dato.lstrip('#')
                self.modificar_linea(self.formulario_no_numero_lista[index], dato)
                print(f"{self.formulario_no_numero_lista[index]}: {dato}")
        self.save_config()
        self.borrar_contenido()
        self.inicializar()
        self.load_config()
        self.load_formulario()
        self.inicializar_botones()
        #self.agregar_datos_formulario()   
        ventana_confirmacion.destroy()

    def eliminar_datos_formulario(self):
        # Función para abrir la ventana de edición
        ventana_agregar = tk.Toplevel(self.root)
  
        ventana_agregar.title("Agregar nuevos datos a la tabla")

        # Crear canvas con scrollbar vertical
        canvas = tk.Canvas(ventana_agregar)
        scrollbar = tk.Scrollbar(ventana_agregar, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame interior para los checkboxes
        frame_interior = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame_interior, anchor="nw")
        
        self.centrar_ventana2(ventana_agregar, 600, 700)  

        #self.load_formulario()
        # Crear checkboxes y asociar a variables
        for i, dato in enumerate(self.formulario_datos):
            if(self.es_una_configuracion(dato)):
                # Frame para alinear datos y checkbox horizontalmente
                frame = tk.Frame(frame_interior)
                frame.pack(anchor="w", pady=0)

                # Etiqueta para mostrar el dato
                label = tk.Label(frame, text=dato)
                label.pack(side="right")
            else:
                dato = self.formulario_datos[i] + "=" + self.opciones[i].get()
                # Frame para alinear datos y checkbox horizontalmente
                frame = tk.Frame(frame_interior)
                frame.pack(anchor="w", pady=0)

                # Etiqueta para mostrar el dato
                label = tk.Label(frame, text=dato)
                label.pack(side="right")

                # Crear checkbox y asociar a variable
                checkbox = tk.Checkbutton(frame, variable=self.checkbox_vars[i])
                checkbox.pack(side="right")
            
        frame = tk.Frame(frame_interior)
        frame.pack(anchor="w", side="right")

         # Botón para imprimir el estado de los checkboxes
        btn_eliminar_dato = tk.Button(frame, text="Eliminar datos", command=lambda: self.mostrar_modal_confirmacion_eliminar(ventana_agregar))
        btn_eliminar_dato.pack(pady=10)

        # Configurar el canvas para el scrollbar
        frame_interior.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all")) 

    def mostrar_modal_confirmacion_eliminar(self, ventana_agregar):
        # Crear una nueva ventana (cuadro de diálogo) utilizando Toplevel
        ventana_confirmacion = tk.Toplevel(self.root)
        ventana_confirmacion.title("Confirmación eliminar")
        
        # Agregar etiqueta y botones al cuadro de diálogo
        label = tk.Label(ventana_confirmacion, text="¿Estás seguro de eliminar los datos?")
        label.pack(pady=10)

        # Botón "Guardar"
        btn_guardar = tk.Button(ventana_confirmacion, text="Guardar", command=lambda: self.eliminar_formulario(ventana_confirmacion))
        btn_guardar.pack(side="left", padx=10)

        # Botón "Cancelar"
        btn_cancelar = tk.Button(ventana_confirmacion, text="Cancelar", command=ventana_confirmacion.destroy)
        btn_cancelar.pack(side="left", padx=10)

        # Centrar la ventana de confirmación sobre la ventana principal
        self.centrar_ventana3(ventana_confirmacion)
        ventana_agregar.destroy()

    def eliminar_formulario(self, ventana_confirmacion):
        # Imprimir el estado de los checkboxes
        # Función para guardar los cambios y cerrar la ventana de edición
        for index, dato in enumerate(self.formulario_datos):
            if self.checkbox_vars[index].get():
                dato = "#" + self.formulario_datos[index] + "=" + self.opciones[index].get()
                self.modificar_linea(self.formulario_numero_lista[index], dato)
                #print(f"{self.formulario_no_numero_lista[index]}: {dato}")
        self.save_config()
        self.borrar_contenido()
        self.inicializar()
        self.load_config()
        self.load_formulario()
        self.inicializar_botones()
        #self.eliminar_datos_formulario()  
        ventana_confirmacion.destroy()

    def es_una_configuracion(self, linea):
        # Agrega aquí otras validaciones según sea necesario
        if "# General Settings" in linea:
            return True
        elif "# Local FTP user Settings" in linea:
            return True
        elif "# Anonymus FTP user Settings" in linea:
            return True
        elif "# Log Settings" in linea:
            return True
        elif "# Transfer Settings" in linea:
            return True
        elif "### security features that are incompatible with some other settings. ###" in linea:
            return True
        else:
            return False
#-------------------------------------- Solo para acomodar ventanas --------------------------------------------

    def centrar_ventana(self): 
        # Obtener las dimensiones de la pantalla
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()

        # Obtener las dimensiones de la ventana
        ancho_ventana = 1350
        alto_ventana = 500

        # Calcular la posición para centrar la ventana
        x_pos = (ancho_pantalla - ancho_ventana) // 2
        y_pos = (alto_pantalla - alto_ventana) // 2

        # Establecer la posición de la ventana
        self.root.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}") 

    def centrar_ventana2(self, ventana, ancho, alto):
        # Obtener las dimensiones de la pantalla
        ancho_pantalla = ventana.winfo_screenwidth()
        alto_pantalla = ventana.winfo_screenheight()

        # Obtener las dimensiones de la ventana
        ancho_ventana = ancho
        alto_ventana = alto

        # Calcular la posición para centrar la ventana
        x_pos = (ancho_pantalla - ancho_ventana) // 2
        y_pos = (alto_pantalla - alto_ventana) // 2

        # Establecer la posición de la ventana
        ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}")

    def centrar_ventana3(self, ventana):
        ventana.update_idletasks()
        ancho_ventana = ventana.winfo_width()
        alto_ventana = ventana.winfo_height()
        x_pantalla = (ventana.winfo_screenwidth() // 2) - (ancho_ventana // 2)
        y_pantalla = (ventana.winfo_screenheight() // 2) - (alto_ventana // 2)
        ventana.geometry('{}x{}+{}+{}'.format(ancho_ventana, alto_ventana, x_pantalla, y_pantalla))

    def abrir_ventana_configuracion(self):
        self.root.withdraw()  # Oculta la ventana actual
        self.funcion_volver()  # Llama a la función para volver a la ventana principal

    def imprimir_tabla(self):
        # Imprimir los datos seleccionados en la tabla
        for i, nombre in enumerate(self.formulario_datos):
            opcion = self.opciones[i].get()
            print(f"{nombre}: {opcion}")
    
    def borrar_contenido(self):
        # Recorre todos los widgets en la ventana y destrúyelos
        for widget in self.root.winfo_children():
            widget.destroy()
