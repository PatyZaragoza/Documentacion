import paramiko
import tkinter as tk
from tkinter import messagebox

def ejecutar_comando_ssh(host, usuario, contraseña, comando):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=host, username=usuario, password=contraseña)
        stdin, stdout, stderr = ssh_client.exec_command(comando)
        stdin.write(contraseña + '\n')
        stdin.flush()
        salida = stdout.read().decode("utf-8")
        error = stderr.read().decode("utf-8")
        ssh_client.close()
        return salida, error
    except Exception as e:
        return None, str(e)

def ejecutar_comando_bloquear():
    host = host_entry.get()
    usuario = usuario_entry.get()
    contraseña = contraseña_entry.get()
    comando_bloquear_teclado = f"echo '{contraseña}' | sudo -S killall -STOP gnome-shell"

    salida_bloquear_teclado, error_bloquear_teclado = ejecutar_comando_ssh(host, usuario, contraseña, comando_bloquear_teclado)
    if error_bloquear_teclado:
        messagebox.showinfo("Éxito", "Bloqueo de teclado y ratón exitoso.")
    else:
        messagebox.showinfo("Éxito", "Bloqueo de teclado y ratón exitoso.")

def ejecutar_comando_desbloquear():
    host = host_entry.get()
    usuario = usuario_entry.get()
    contraseña = contraseña_entry.get()
    comando_desbloquear_teclado = f"echo '{contraseña}' | sudo -S killall -CONT gnome-shell"

    salida_desbloquear_teclado, error_desbloquear_teclado = ejecutar_comando_ssh(host, usuario, contraseña, comando_desbloquear_teclado)
    if error_desbloquear_teclado:
        messagebox.showinfo("Éxito", "Desbloqueo de teclado y ratón exitoso.")
    else:
        messagebox.showinfo("Éxito", "Desbloqueo de teclado y ratón exitoso.")

def habilitar_botones(event=None):
    if host_entry.get() and usuario_entry.get() and contraseña_entry.get():
        btn_bloquear.config(state=tk.NORMAL)
        btn_desbloquear.config(state=tk.NORMAL)
    else:
        btn_bloquear.config(state=tk.DISABLED)
        btn_desbloquear.config(state=tk.DISABLED)

root = tk.Tk()
root.title("BLoqueo")
root.geometry("380x380")
root.resizable(False, False)

# Obtener dimensiones de la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calcular la posición para centrar la ventana
x = (screen_width // 2) - (380 // 2)
y = (screen_height // 2) - (380 // 2)

root.geometry(f"380x380+{x}+{y}")

tk.Label(root, text="Bloqueo del teclado y cursor de la computadora cliente").pack(pady=10)

tk.Label(root, text="Ip de la computadora:").pack(anchor="w", padx=20)
host_entry = tk.Entry(root)
host_entry.pack(fill="x", padx=20)
host_entry.bind("<KeyRelease>", habilitar_botones)

tk.Label(root, text="Nombre del usuario de la computadora:").pack(anchor="w", padx=20)
usuario_entry = tk.Entry(root)
usuario_entry.pack(fill="x", padx=20)
usuario_entry.bind("<KeyRelease>", habilitar_botones)

tk.Label(root, text="Contraseña de la maquina:").pack(anchor="w", padx=20)
contraseña_entry = tk.Entry(root, show="*")
contraseña_entry.pack(fill="x", padx=20)
contraseña_entry.bind("<KeyRelease>", habilitar_botones)

btn_bloquear = tk.Button(root, text="Bloquear", command=ejecutar_comando_bloquear, state=tk.DISABLED)
btn_bloquear.pack(pady=10)

btn_desbloquear = tk.Button(root, text="Desbloquear", command=ejecutar_comando_desbloquear, state=tk.DISABLED)
btn_desbloquear.pack(pady=10)

root.mainloop()
