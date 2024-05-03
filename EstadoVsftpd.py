import subprocess
import tkinter as tk
from tkinter import messagebox
import os

class FTPServerAppGUI:
    def __init__(self, root, funcion_volver):
        self.server_running = False
        self.root = root
        self.funcion_volver = funcion_volver

        self.logo = "/home/publica/Escritorio/VSFTPD_PROYECTO/estado_servidor.png"
        #self.logo = "./estado_servidor.png"
        self.root.title("VSFTPD ")
        self.fondo = tk.PhotoImage(file=self.logo)
        self.fondo1 = tk.Label(self.root, image=self.fondo).place(x=0, y=0, relwidth=1, relheight=1)

        self.centrar_ventana()

        # Etiquetas
        self.label_status = tk.Label(root, text="Estado del servidor FTP",bg="#a5e7cc",font=("Arial", 16,"bold"))
        self.label_status.place(x=75,y=65)

        # Botones
        self.button_check_installation = tk.Button(root, text="Verificar Instalación", command=self.check_installation,background="#43fef6")
        self.button_check_status = tk.Button(root, text="Verificar Estado", command=self.check_server_status,background="#43fef6")
        self.button_start_server = tk.Button(root, text="Iniciar Servidor", command=self.start_server,background="#43fef6")
        self.button_stop_server = tk.Button(root, text="Parar Servidor", command=self.stop_server,background="#43fef6")
        self.button_restart_server = tk.Button(root, text="Reiniciar Servidor", command=self.restart_server,background="#43fef6")
        self.button_configuracion = tk.Button(root, text="< volver", command=self.abrir_ventana_configuracion,background="#43fef6")

        # Colocar widgets en la ventana
        self.button_check_installation.place(x=50,y=180)
        self.button_check_status.place   (x=285, y=250)
        self.button_start_server.place   (x=170, y=300)
        self.button_stop_server.place    (x=290, y=300)
        self.button_restart_server.place (x=410, y=300)

        self.button_configuracion.place(x=10,y=10)


        self.canvas = tk.Canvas(root, width=50, height=50)
        self.canvas.place(x=310, y=150)

        self.label = tk.Label(root, text="Estado", font=("Helvetica", 16))
        self.label.place(x=280, y=210)
        
        self.check_service_status()
        
    def install_vsftpd(self):
        try:
            ruta_al_archivo_rpm_vsftpd = "/home/publica/Escritorio/VSFTPD_PROYECTO/Instaladores/vsftpd-3.0.3-lp152.7.6.x86_64.rpm"
            ruta_al_archivo_rpm_user = "/home/publica/Escritorio/VSFTPD_PROYECTO/Instaladores/system-user-ftp-20170617-lp152.5.114.noarch.rpm"
            subprocess.run(["sudo","rpm", "-ivh", ruta_al_archivo_rpm_vsftpd], check=True)
            subprocess.run(["sudo","rpm", "-ivh", ruta_al_archivo_rpm_user], check=True)
            print("vsftpd instalado correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al instalar vsftpd: {e}")

    def mostrar_mensaje(self):
        if self.is_vsftpd_installed() and self.is_system_user_ftp_installed():
            print("soy felizzzzzzzz")
        else:
            print("Instalando...")
             # Crear el mensaje del modal
            message = (
                "¡Atención!\n\n"
                "El servidor FTP (vsftpd) no se encuentra instalado en su sistema.\n"
                "¿Desea instalar vsftpd para habilitar transferencias seguras de archivos?"
            )

            # Ocultar la ventana principal temporalmente
            self.root.withdraw()

            # Crear el modal de confirmación
            result = messagebox.askquestion("Instalación de vsftpd", message, icon="warning")

            # Procesar la respuesta del usuario
            if result == "yes":
                # Aquí puedes llamar a la función de instalación del servidor vsftpd
                print("tengo que instalar aca")
                self.install_vsftpd()
            else:
                print("El usuario canceló la instalación.")

            # Hacer que la ventana principal sea visible nuevamente
            self.root.deiconify()

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
    
    def abrir_ventana_configuracion(self):
        self.root.withdraw()  # Oculta la ventana actual
        self.funcion_volver()  # Llama a la función para volver a la ventana principal

# -----------------------------FUNCIONALIDADES-----------------------------------------

    def check_installation(self):
        try:
            os.environ['SHELL'] = '/bin/bash' 
            command = 'sudo rpm -qa | grep vsftpd'
            result = subprocess.run(command,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            output = result.stdout

            # Mostrar el resultado en una ventana emergente
            #messagebox.showinfo("Resultado de la verificación de instalación de vsFTPd", output)

            if result.returncode == 0:
                messagebox.showinfo("Estado de instalación",f"{output}\nEstá instalado en el sistema.")
            else:
                messagebox.showinfo("Estado", "vsFTPd no está instalado en el sistema.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", str(e))

    def check_server_status(self):
        self.check_service_status()
        try:
            result = subprocess.run(['sudo','service', 'vsftpd', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            output = result.stdout

            # Mostrar el resultado en una ventana emergente
            #messagebox.showinfo("Resultado de la verificación del estado del servidor FTP", output)

            if result.returncode == 0:
                messagebox.showinfo("Estado", "El servidor FTP está en ejecución.")
            else:
                messagebox.showinfo("Estado", "El servidor FTP no está en ejecución.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", str(e))

    def start_server(self):
        try:
            # Ejecutar el comando con sudo si es necesario
            result = subprocess.run(['sudo','service', 'vsftpd', 'start'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

            # Mostrar el resultado en una ventana emergente
            if result.returncode == 0:
                messagebox.showinfo("Estado", "El servidor FTP se inició correctamente.")
                self.server_running = True
            else:
                error_message = f"Error al iniciar el servidor FTP. Detalles: {result.stderr.strip()}"
                messagebox.showerror("Error", error_message)
                self.server_running = False
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", str(e))
        self.check_service_status()

    def stop_server(self):
        try:
            result = subprocess.run(['sudo','service', 'vsftpd', 'stop'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

            # Mostrar el resultado en una ventana emergente
            if result.returncode == 0:
                messagebox.showinfo("Estado", "El servidor FTP se detuvo correctamente.")
                self.server_running = False
            else:
                messagebox.showerror("Error", "Error al detener el servidor FTP.")
                self.server_running = True  # o deja la variable sin cambios según tu lógica específica
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", str(e))
        self.check_service_status()

    def restart_server(self):
        try:
            result = subprocess.run(['sudo','service', 'vsftpd', 'restart'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

            # Mostrar el resultado en una ventana emergente
            if result.returncode == 0:
                messagebox.showinfo("Estado", "El servidor FTP se reinicio correctamente.")
                self.server_running = False
            else:
                messagebox.showerror("Error", "Error al reinicar el servidor FTP.")
                self.server_running = True  # o deja la variable sin cambios según tu lógica específica
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", str(e))
        self.check_service_status()

    def check_service_status(self):
        try:
            command = 'sudo service vsftpd status'
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

            if result.returncode == 0 and "active (running)" in result.stdout:
                self.update_status("corriendo", "green")
            elif result.returncode == 3 and "inactive (dead)" in result.stdout:
                self.update_status("detenido", "red")
            else:
                self.update_status("no instalado", "gray")

        except subprocess.CalledProcessError as e:
            self.update_status("error", "gray")

    def update_status(self, status, color):
        self.label.config(text=f"[ {status} ]", fg=color)

        # Borrar cualquier objeto en el canvas
        self.canvas.delete("all")

        # Dibujar un círculo (ovalo) de color correspondiente
        x, y, r = 25, 25, 20
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color)
