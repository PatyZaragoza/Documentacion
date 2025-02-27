#se debe de tomar en cuenta el tipo de Sistema operativo 
# ingeniería en sistemas computacionales 
# Autor : Patricia Zaragoza Palma 

import socket
import numpy as np
import cv2
import struct

def run_server():
    # Configuración del servidor para recibir la pantalla del cliente
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5000))
    server_socket.listen(1)
    print("Esperando conexión del cliente...")
    client_socket, _ = server_socket.accept()
    print("Cliente conectado.")

    # Configuración para retransmitir a la tercera computadora (receptor)
    transmit_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transmit_socket.bind(('0.0.0.0', 5001))  # Puerto para retransmisión
    transmit_socket.listen(1)
    print("Esperando conexión del receptor...")
    receiver_socket, _ = transmit_socket.accept()
    print("Receptor conectado. Retransmitiendo la pantalla...")

    data = b""
    payload_size = struct.calcsize(">L")

    try:
        while True:
            # Recibir el tamaño de la imagen del cliente
            while len(data) < payload_size:
                data += client_socket.recv(4096)
            
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]

            # Recibir la imagen del cliente
            while len(data) < msg_size:
                data += client_socket.recv(4096)
            
            frame_data = data[:msg_size]
            data = data[msg_size:]

            # Retransmitir el tamaño de la imagen al receptor
            receiver_socket.sendall(struct.pack(">L", msg_size))
            # Retransmitir los datos de la imagen al receptor
            receiver_socket.sendall(frame_data)

            # Decodificar y mostrar la imagen en el servidor (opcional)
            img = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)
            img_resized = cv2.resize(img, (800, 450))  # Ajustar el tamaño de la ventana de visualización
            cv2.imshow("Pantalla Remota en el Servidor", img_resized)

            if cv2.waitKey(1) == 27:  # Presiona ESC para salir
                break

    except KeyboardInterrupt:
        print("Retransmisión detenida.")

    finally:
        client_socket.close()
        receiver_socket.close()
        server_socket.close()
        transmit_socket.close()
        cv2.destroyAllWindows()
        print("Conexión cerrada.")

if __name__ == "__main__":
    run_server()
