# Patricia Zaragoza Palma
# Ingenieria en Sistemas Computacionales
import socket
import pyautogui
import io
import tkinter as tk
import threading
import time  # Importar para usar sleep
from PIL import Image

def start_screen_monitoring_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Usar la dirección IP especificada
    host = "172.168.2.38"
    server_socket.bind((host, port))
    server_socket.listen(5)  # Permitir hasta 5 conexiones en espera
    print(f"Esperando conexiones en {host}:{port}...")

    # Actualizar la interfaz gráfica con la IP y el puerto
    ip_label.config(text=f"IP: {host}")
    port_label.config(text=f"Puerto: {port}")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Conexión establecida con {addr}")

            try:
                while True:
                    # Captura de pantalla
                    screenshot = pyautogui.screenshot()
                    
                    # Convertir la imagen a RGB (eliminar canal alfa)
                    screenshot = screenshot.convert("RGB")
                    
                    # Convertir a bytes
                    byte_array = io.BytesIO()
                    screenshot.save(byte_array, format='JPEG')
                    image_data = byte_array.getvalue()

                    # Enviar tamaño de la imagen
                    client_socket.sendall(len(image_data).to_bytes(4, byteorder='big'))
                    # Enviar la imagen
                    client_socket.sendall(image_data)

                    # Esperar 5 segundos antes de la siguiente captura
                    time.sleep(0.05)
            except Exception as e:
                print(f"Error con {addr}: {e}")
            finally:
                print(f"Cerrando conexión con {addr}")
                client_socket.close()
    finally:
        server_socket.close()

# Crear la ventana principal
root = tk.Tk()
root.title("Servidor de Monitoreo de Pantalla")

# Crear etiquetas para mostrar la IP y el puerto
ip_label = tk.Label(root, text="Esperando IP...")
ip_label.pack(pady=10)

port_label = tk.Label(root, text="Esperando puerto...")
port_label.pack(pady=10)

# Configura el puerto
port = 5001

# Iniciar el servidor en un hilo separado
server_thread = threading.Thread(target=start_screen_monitoring_server, args=(port,), daemon=True)
server_thread.start()

# Ajustar el tamaño de la ventana
root.geometry("600x400")

# Iniciar el bucle principal de la interfaz
root.mainloop()
