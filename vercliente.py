# Patricia Zaragoza Palma 
# ingeniería en sistemas computacionales 
import socket
import numpy as np
import cv2
import mss
import struct
import time

def run_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('172.168.3.92', 5000))  # Asegúrate de que esta IP sea la correcta para el servidor

        with mss.mss() as sct:
            while True:
                try:
                    # Captura la pantalla y envía la imagen comprimida
                    screenshot = sct.grab(sct.monitors[0])
                    img = np.array(screenshot)
                    _, img_encoded = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 80])
                    data = img_encoded.tobytes()

                    # Envía el tamaño de la imagen seguido de los datos de la imagen
                    client_socket.sendall(struct.pack(">L", len(data)))
                    client_socket.sendall(data)

                    time.sleep(0.03)  # Controla el framerate

                except BrokenPipeError:
                    print("Conexión perdida. Intentando reconectar...")
                    break  # Salir del bucle si la conexión se interrumpe

    except ConnectionRefusedError:
        print("No se pudo conectar al servidor. Verifica que el servidor esté activo.")
    
    finally:
        client_socket.close()
        print("Conexión cerrada.")

if __name__ == "__main__":
    run_client()
