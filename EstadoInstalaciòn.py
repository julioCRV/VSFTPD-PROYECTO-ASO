import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os


class FTPApp:
    def __init__(self, root):
        self.root = root
        self.logo = "/home/publica/Escritorio/VSFTPD_PROYECTO/instalacion.png"
        # self.logo = "./instalacion.png"
        self.root.title("Aplicación FTP")
        self.root.geometry("600x400")
        self.root.configure(bg="#b497ed")  
        self.root.resizable(width=False, height=False) 
        self.fondo = tk.PhotoImage(file=self.logo)
        self.fondo1 = tk.Label(self.root, image=self.fondo).place(x=0, y=0, relwidth=1, relheight=1)

        self.centrar_ventana()

        # Botón para cambiar de ventana
        select_button1 = tk.Button(root, text="Ver Configuraciones", command=self.abrir_otra_ventana,background="#9681fa")
        select_button1.place(x=90,y=250)

         # Botón para cambiar de ventana
        select_button1 = tk.Button(root, text="Estado servidor FTP", command=self.abrir_ventana_estados,background="#9681fa")
        select_button1.place(x=90,y=200)

        # Botón para seleccionar un archivo con instalaciones FTP
        select_button = tk.Button(root, text="Instalar servidor FTP", command=self.mostrar_modal, background="#9681fa")
        select_button.place (x=90,y=100)

        # Botón para desinstalar vsftpd
        select_button = tk.Button(root, text="Desinstalar servidor FTP", command=self.confirmar_desinstalacion, background="#9681fa")
        select_button.place (x=90,y=150)

        # Botón para conectar al servidor FTP
        #connect_button = tk.Button(root, text="Conectar al Servidor FTP", command=self.connect_to_ftp)
        #connect_button.pack(pady=10)

        self.mostrar_mensaje()

# ----------------------------- ENRUTAMIENTO DE VENTANAS -----------------------------------------------------
    def abrir_ventana_estados(self):
        from EstadoVsftpd import FTPServerAppGUI
        self.root.withdraw()  # Oculta la ventana actual

        # Crea la ventana 2 y pasa la función para volver a la ventana principal
        ventana_estado = tk.Toplevel(self.root)
        FTPServerAppGUI(ventana_estado, self.volver_a_Estado_instalacion)

    def volver_a_Estado_instalacion(self):
        self.root.deiconify()  # Muestra la ventana principal nuevamente

    def abrir_otra_ventana(self):
        from Formulario import VSFTPDConfigEditor
        self.root.withdraw()  #Oculta la ventana actual

        # Crea y muestra la ventana que contiene el formulario de configuraciones
        ventana_formulario = tk.Toplevel(self.root)
        VSFTPDConfigEditor(ventana_formulario, self.volver_a_Estado_instalacion)
    


# --------------------- METODOS PARA MOSTRAR EL MENSAJE CUANDO SE INICIA EL PROGRAMA -------------------------
    def mostrar_mensaje(self):
        if self.is_vsftpd_installed() and self.is_system_user_ftp_installed():
            print("El servidor FTP ya se encuentra instalado")
            #messagebox.showinfo("Estado del Servidor","El servidor FTP ya se encuentra instalado")
        else:
            print("Instalando...")
             # Crear el mensaje del modal
            message = (
                "¡Atención!\n\n"
                "El servidor FTP (vsftpd) no se encuentra instalado en su sistema.\n"
                "¿Desea instalar vsftpd para habilitar las configuraciones?"
            )

            # Ocultar la ventana principal temporalmente
            root.withdraw()

            # Crear el modal de confirmación
            result = messagebox.askquestion("Instalación de vsftpd", message, icon="warning")

            # Procesar la respuesta del usuario
            if result == "yes":
                # Aquí puedes llamar a la función de instalación del servidor vsftpd
                print("tengo que instalar aca")
                self.instalacion_automatica_inicial()
            else:
                print("El usuario canceló la instalación.")

            # Hacer que la ventana principal sea visible nuevamente
            root.deiconify()

    def is_vsftpd_installed(self):
        try:
            self.vsftpd_instalado = True
            # Ejecuta el comando rpm para verificar la instalación de vsftpd
            subprocess.run(["sudo","rpm", "-q", "vsftpd"], check=True)
            return True  # Devuelve True si el comando se ejecuta correctamente (vsftpd está instalado)
        except subprocess.CalledProcessError:
            return False  # Devuelve False si hay un error (vsftpd no está instalado)

    def is_system_user_ftp_installed(self):
        try:
            subprocess.run(["sudo","rpm", "-q", "system-user-ftp"], check=True)
            return True
        except subprocess.CalledProcessError:
            return False



# ----------------------------- METODOS ASOCIADOS AL "BOTON DE INSTALACION" ---------------------------------- 
    def mostrar_modal(self):
        ventana = tk.Tk()
        ventana.title("Tipo de Instalación")
        self.centrar_ventana_modal(ventana, 220, 130)

        etiqueta = tk.Label(ventana, text="Selecciona el tipo de instalación:")
        etiqueta.pack(pady=10)

        btn_instalacion_manual = tk.Button(ventana, text="Instalación Manual", command=lambda:self.instalacion_manual(ventana))
        btn_instalacion_manual.pack(pady=5)

        btn_instalacion_automatica = tk.Button(ventana, text="Instalación Automática", command=lambda:self.instalacion_automatica(ventana))
        btn_instalacion_automatica.pack(pady=5)

    def seleccionar_tipo_instalacion(self, tipo):
        messagebox.showinfo("Selección de Tipo de Instalación", f"Has seleccionado {tipo}.")

# --------- Instalacion manual
    def instalacion_manual(self, ventana):
        ventana.destroy()
        # Abre un cuadro de diálogo para seleccionar un archivo
        file_path = filedialog.askopenfilename()
        print("Archivo seleccionado:", file_path)
        try:
                # Mostrar un mensaje de confirmación
            respuesta = messagebox.askyesno("Confirmación", f"¿Desea instalar este archivo? \n {file_path}")

            if respuesta:
                # Si el usuario hace clic en 'Sí', iniciar la instalación
                self.mostrar_ventana_instalacion(file_path)
                print("vsftpd instalado correctamente.")
            else:
                # Si el usuario hace clic en 'No', realizar otra acción o salir
                print("Instalación cancelada.")
            
        except subprocess.CalledProcessError as e:
            print(f"Error al instalar vsftpd: {e}")

    def mostrar_ventana_instalacion(self, file_path):
        if self.is_vsftpd_installed() and self.is_system_user_ftp_installed():
            print("soy felizzzzzzzz")
            messagebox.showinfo("Estado del Servidor","El servidor FTP ya se encuentra instalado")
        else:
        # Crear una nueva ventana
            ventana_nueva = tk.Toplevel(self.root)
            ventana_nueva.title("Instalación del Servidor FTP")
            self.centrar_ventana_modal(ventana_nueva, 350, 80)

            # Agregar contenido a la nueva ventana
            etiqueta = tk.Label(ventana_nueva, text="El servidor FTP se está instalando. Por favor, espera...")
            etiqueta.pack(pady=20)

            # Simula el tiempo de instalación (3 segundos en este caso)
            ventana_nueva.after(3000, lambda:self.mostrar_mensaje_instalacion_completada1(ventana_nueva, file_path))

    def mostrar_mensaje_instalacion_completada1(self, venta_nueva, file_path):
        venta_nueva.destroy()
         # Llamar a self.install_vsftpd después de mostrar el mensaje de instalación completada
        subprocess.run(["sudo","rpm", "-ivh", file_path], check=True)
        messagebox.showinfo("Instalación Completada", "El servidor FTP se ha instalado correctamente.")

# --------- Instalacion automatica
    def instalacion_automatica_inicial(self):
        if self.is_vsftpd_installed() and self.is_system_user_ftp_installed():
            print("soy felizzzzzzzz")
            messagebox.showinfo("Estado del Servidor","El servidor FTP ya se encuentra instalado")
        else:
        # Crear una nueva ventana
            ventana_nueva = tk.Toplevel(self.root)
            ventana_nueva.title("Instalación del Servidor FTP")
            self.centrar_ventana_modal(ventana_nueva, 350, 80)

            # Agregar contenido a la nueva ventana
            etiqueta = tk.Label(ventana_nueva, text="El servidor FTP se está instalando. Por favor, espera...")
            etiqueta.pack(pady=20)

            # Simula el tiempo de instalación (3 segundos en este caso)
            ventana_nueva.after(3000, lambda:self.mostrar_mensaje_instalacion_completada2(ventana_nueva))

    def instalacion_automatica(self, ventana):
        ventana.destroy()
        if self.is_vsftpd_installed() and self.is_system_user_ftp_installed():
            print("soy felizzzzzzzz")
            messagebox.showinfo("Estado del Servidor","El servidor FTP ya se encuentra instalado")
        else:
        # Crear una nueva ventana
            ventana_nueva = tk.Toplevel(self.root)
            ventana_nueva.title("Instalación del Servidor FTP")
            self.centrar_ventana_modal(ventana_nueva, 350, 80)

            # Agregar contenido a la nueva ventana
            etiqueta = tk.Label(ventana_nueva, text="El servidor FTP se está instalando. Por favor, espera...")
            etiqueta.pack(pady=20)

            # Simula el tiempo de instalación (3 segundos en este caso)
            ventana_nueva.after(3000, lambda:self.mostrar_mensaje_instalacion_completada2(ventana_nueva))

    def mostrar_mensaje_instalacion_completada2(self, venta_nueva):
        venta_nueva.destroy()
         # Llamar a self.install_vsftpd después de mostrar el mensaje de instalación completada
        self.install_vsftpd()
        messagebox.showinfo("Instalación Completada", "El servidor FTP se ha instalado correctamente.")

    def install_vsftpd(self):
        try:
            ruta_al_archivo_rpm_vsftpd = "/home/publica/Escritorio/VSFTPD_PROYECTO/Instaladores/vsftpd-3.0.3-lp152.7.6.x86_64.rpm"
            ruta_al_archivo_rpm_user = "/home/publica/Escritorio/VSFTPD_PROYECTO/Instaladores/system-user-ftp-20170617-lp152.5.114.noarch.rpm"
            subprocess.run(["sudo","rpm", "-ivh", ruta_al_archivo_rpm_vsftpd], check=True)
            subprocess.run(["sudo","rpm", "-ivh", ruta_al_archivo_rpm_user], check=True)
            print("vsftpd instalado correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al instalar vsftpd: {e}")

       
            
# ----------------------------- METODOS ASOCIADOS AL "BOTON DE DESINSTALACION" -------------------------------- 
    def confirmar_desinstalacion(self):
        # Crea la ventana principal
        ventana = tk.Tk()
        ventana.title("Confirmar Desinstalación")
        self.centrar_ventana_modal(ventana, 330, 120)

        # Configura el mensaje
        mensaje = "¿Estás seguro de que deseas desinstalar el servidor FTP?"
        etiqueta = tk.Label(ventana, text=mensaje, padx=10, pady=10)
        etiqueta.pack()

        # Configura los botones
        btn_cancelar = tk.Button(ventana, text="Cancelar", command=ventana.destroy)
        btn_cancelar.pack(side="left", padx=45)

        btn_desinstalar = tk.Button(ventana, text="Desinstalar", command=lambda:self.uninstall_server(ventana))
        btn_desinstalar.pack(side="right", padx=45)
        
    def uninstall_server(self, ventana):
        ventana.destroy()
        try:
            #ruta_al_archivo_rpm_vsftpd = "/home/publica/Escritorio/VSFTPD_PROYECTO/Instaladores/vsftpd-3.0.3-lp152.7.6.x86_64.rpm"
            #ruta_al_archivo_rpm_user = "/home/publica/Escritorio/VSFTPD_PROYECTO/Instaladores/system-user-ftp-20170617-lp152.5.114.noarch.rpm"
            subprocess.run(["sudo","rpm", "-e", "vsftpd"], check=True)
            #subprocess.run(["rpm", "-ivh", ruta_al_archivo_rpm_user], check=True)
            messagebox.showinfo("Desinstalación Completa", "El servidor FTP se ha desinstalado correctamente.")
            #print("vsftpd instalado correctamente.")
        except subprocess.CalledProcessError as e:
            messagebox.showinfo("Desinstalación fallida", f"¡El servidor FTP ya se encuentra desinstalado! \n \n mas detalles del error: \n{e}")
            #print(f"Error al instalar vsftpd: {e}")

# ----------------------------- POSICIONAMIENTO DE VENTANAS ----------------------------------
    def centrar_ventana(self):
        # Obtener las dimensiones de la pantalla
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()

        # Obtener las dimensiones de la ventana
        ancho_ventana = 600
        alto_ventana = 400

        # Calcular la posición para centrar la ventana
        x_pos = (ancho_pantalla - ancho_ventana) // 2
        y_pos = (alto_pantalla - alto_ventana) // 2

        # Establecer la posición de la ventana
        self.root.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}")
    
    def centrar_ventana_modal(self, ventana, ancho, alto):
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

if __name__ == "__main__":
    root = tk.Tk()
    app = FTPApp(root)
    root.mainloop()
