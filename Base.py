import tkinter as tk
from tkinter import ttk
import platform
import psutil
import socket
import os
import GPUtil

def get_system_info():
    uname = platform.uname()
    gpus = GPUtil.getGPUs()
    gpu_name = gpus[0].name if gpus else "Nenhuma GPU detectada"
    gpu_memory = f"{gpus[0].memoryTotal:.2f} MB" if gpus else "N/A"

    disk_usage = psutil.disk_usage('/')
    net_info = psutil.net_if_addrs()
    mac_address = net_info['Ethernet'][0].address if 'Ethernet' in net_info else "N/A"

    info = {
        "Sistema": uname.system,
        "Nome do Host": uname.node,
        "Versão": uname.version,
        "Release": uname.release,
        "Arquitetura": platform.machine(),
        "Processador": uname.processor,
        "Núcleos Físicos": psutil.cpu_count(logical=False),
        "Núcleos Lógicos": psutil.cpu_count(logical=True),
        "Frequência da CPU (MHz)": f"{psutil.cpu_freq().current:.2f}",
        "RAM Total (GB)": f"{psutil.virtual_memory().total / (1024**3):.2f}",
        "IP Local": socket.gethostbyname(socket.gethostname()),
        "Endereço MAC": mac_address,
        "Disco Total (GB)": f"{disk_usage.total / (1024**3):.2f}",
        "Disco Usado (GB)": f"{disk_usage.used / (1024**3):.2f}",
        "Disco Livre (GB)": f"{disk_usage.free / (1024**3):.2f}",
        "Placa de Vídeo": gpu_name,
        "Memória da GPU": gpu_memory,
        "Tempo de Atividade (Uptime)": f"{psutil.boot_time():.2f} segundos"
    }
    return info

def atualizar_infos():
    tree.delete(*tree.get_children())  # Limpa a tabela antes de inserir de novo
    infos = get_system_info()
    for chave, valor in infos.items():
        tree.insert("", "end", values=(chave, valor))

# --- Estilo retrô ---

root = tk.Tk()
root.title("Sistema 🖥️")
root.geometry("800x600")
root.resizable(False, False)
root.configure(bg="#C0C0C0")

style = ttk.Style()
style.theme_use("clam")

style.configure("Treeview",
                background="#FFFFFF",
                foreground="black",
                fieldbackground="#FFFFFF",
                rowheight=25,
                font=('Courier New', 10))

style.configure("Treeview.Heading",
                font=('Courier New', 10, 'bold'),
                foreground="black",
                background="#A0A0A0",
                relief="raised")

style.configure("TButton",
                background="#E0E0E0",
                foreground="black",
                font=('Courier New', 10, 'bold'),
                borderwidth=2,
                relief="raised")
style.map("TButton",
          background=[("active", "#D0D0D0")],
          relief=[("pressed", "sunken")])

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=0)

tree = ttk.Treeview(root, columns=("Tipo", "Valor"), show="headings", style="Treeview")
tree.heading("Tipo", text="Informação")
tree.heading("Valor", text="Valor")
tree.column("Tipo", width=200, anchor="center")
tree.column("Valor", width=580, anchor="center")
tree.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

botao = ttk.Button(root, text="Atualizar Informações", command=atualizar_infos)
botao.grid(row=1, column=0, pady=10)

# Carregar informações assim que iniciar
atualizar_infos()

root.mainloop()
