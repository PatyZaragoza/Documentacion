# Patricia Zaragoza Palma
import os
import sys
import subprocess
import socket
import pyautogui
import io
import tkinter as tk
from tkinter import messagebox
from Xlib import display, X

# Redirigir errores para que no se muestren en la consola
sys.stderr = open(os.devnull, 'w')

def install_dependencies():
    """
    Verifica e instala las dependencias necesarias para capturar pantallas.
    """
    try:
        # Verificar si gnome-screenshot está instalado
        result = subprocess.run(["which", "gnome-screenshot"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if not result.stdout:
            print("Instalando gnome-screenshot...")
            subprocess.run(["sudo", "apt", "install", "-y", "gnome-screenshot"], check=True)

        # Verificar e instalar Pillow
        try:
            import PIL
            from PIL import Image
        except ImportError:
            print("Instalando Pillow...")
            subprocess.run([os.sys.executable, "-m", "pip", "install", "Pillow>=9.2.0"], check=True)

        # Verificar e instalar Xlib
        try:
            from Xlib import display, X
        except ImportError:
            print("Instalando Python-Xlib...")
            subprocess.run([os.sys.executable, "-m", "pip", "install", "python-xlib"], check=True)

        print("Todas las dependencias están instaladas.")
    except Exception as e:
        # Suprimir errores y continuar con la ejecución
        pass

def get_active_window():
    """
    Obtiene el título de la ventana activa.
    """
    try:
        root = display.Display().screen().root
        window_id = root.get_full_property(display.Display().intern_atom('_NET_ACTIVE_WINDOW'), X.AnyPropertyType).value[0]
        window = display.Display().create_resource_object('window', window_id)
        window_name = window.get_full_property(display.Display().intern_atom('_NET_WM_NAME'), X.AnyPropertyType)
        if window_name:
            return window_name.value
    except Exception:
        # Silenciar errores al obtener la ventana activa
        return None

def get_local_ip():
    """
    Obtiene la IP local de la interfaz de red activa (IPv4).
    """
    try:
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_socket.connect(("8.8.8.8", 80))  # Conecta temporalmente a un servidor conocido
        local_ip = temp_socket.getsockname()[0]
        temp_socket.close()
        return local_ip
    except Exception:
        return "127.0.0.1"  # Como último recurso, devuelve localhost

def start_screen_monitoring_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = get_local_ip()
    try:
        server_socket.bind((host, port))
    except OSError:
        pass  # Silenciar el error y no mostrarlo
        return

    server_socket.listen(5)
    print(f"Esperando conexiones en {host}:{port}...")

    ip_label.config(text=f"IP: {host}")
    port_label.config(text=f"Puerto: {port}")

    try:
        last_active_window = None
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Conexión establecida con {addr}")

            try:
                while True:
                    # Supervisar cambios en la ventana activa
                    active_window = get_active_window()
                    if active_window != last_active_window:
                        print(f"Cambio detectado: {active_window}")
                        last_active_window = active_window

                        # Capturar y enviar la captura de pantalla
                        screenshot = pyautogui.screenshot()

                        # Convertir la imagen a RGB si tiene canal alfa
                        screenshot = screenshot.convert("RGB")

                        byte_array = io.BytesIO()
                        screenshot.save(byte_array, format='JPEG')
                        image_data = byte_array.getvalue()

                        # Enviar el tamaño de la imagen y los datos
                        client_socket.sendall(len(image_data).to_bytes(4, byteorder='big'))
                        client_socket.sendall(image_data)
            except Exception:
                pass  # Silenciar cualquier error durante la conexión
            finally:
                print(f"Cerrando conexión con {addr}")
                client_socket.close()
    finally:
        server_socket.close()

# Crear la ventana principal
root = tk.Tk()
root.title("Servidor de Monitoreo de Pantalla")

ip_label = tk.Label(root, text="Esperando IP...")
ip_label.pack(pady=10)

port_label = tk.Label(root, text="Esperando puerto...")
port_label.pack(pady=10)

port = 12345

# Instalar dependencias antes de iniciar el servidor
try:
    install_dependencies()
except Exception:
    root.destroy()
    exit(1)

# Iniciar el servidor en un hilo separado
import threading
server_thread = threading.Thread(target=start_screen_monitoring_server, args=(port,), daemon=True)
server_thread.start()

root.geometry("600x400")
root.mainloop()
