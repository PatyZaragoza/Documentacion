import subprocess
import tkinter as tk
from tkinter import messagebox

def abrir_cliente_nomachine(host, port):
    """
    Abre el cliente gráfico de NoMachine para conectarse al servidor remoto.
    """
    try:
        print(f"Abriendo cliente NoMachine para conectar a {host}:{port}...")
        # Comando para abrir el cliente NoMachine con un host y puerto específico
        comando = ["/usr/NX/bin/nxplayer", f"nx://{host}:{port}"]
        
        # Ejecutar el comando
        subprocess.run(comando)
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el cliente NoMachine. Asegúrate de que esté instalado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")

def conectar():
    """
    Función que se ejecuta al presionar el botón de conectar.
    """
    host = ip_entry.get()
    port = port_entry.get()
    
    if not host:
        messagebox.showwarning("Advertencia", "Por favor, ingresa una IP válida.")
        return
    if not port.isdigit():
        messagebox.showwarning("Advertencia", "Por favor, ingresa un puerto válido.")
        return
    
    abrir_cliente_nomachine(host, port)

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Cliente NoMachine")
ventana.geometry("400x250")

# Etiqueta de instrucción
instruccion_label = tk.Label(ventana, text="Ingrese la IP del servidor remoto:")
instruccion_label.pack(pady=10)

# Campo de entrada para la IP
ip_entry = tk.Entry(ventana, width=30)
ip_entry.pack(pady=5)

# Etiqueta para el puerto
port_label = tk.Label(ventana, text="Ingrese el puerto del servidor remoto:")
port_label.pack(pady=10)

# Campo de entrada para el puerto
port_entry = tk.Entry(ventana, width=30)
port_entry.insert(0, "4000")  # Puerto predeterminado de NoMachine
port_entry.pack(pady=5)

# Botón para conectar
conectar_button = tk.Button(ventana, text="Conectar", command=conectar)
conectar_button.pack(pady=20)

# Iniciar la aplicación
ventana.mainloop()
