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
    infos = get_system_info()
    for chave, valor in infos.items():
        tree.insert("", "end", values=(chave, valor))

# GUI usando Tkinter
root = tk.Tk()
root.title("Sistema 🖥️")
root.geometry("800x600")
root.resizable(False, False)
root.configure(bg="#1e1e1e")

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="#1e1e1e", foreground="white", fieldbackground="#1e1e1e", rowheight=25)
style.configure("Treeview.Heading", font=('Segoe UI', 10, 'bold'), foreground="white", background="#333")
style.configure("TButton", background="#333", foreground="white", font=('Segoe UI', 10, 'bold'))
style.map("TButton", background=[("active", "#444")])

# Grade da janela principal
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=0)

# Treeview para informações
tree = ttk.Treeview(root, columns=("Tipo", "Valor"), show="headings", style="Treeview")
tree.heading("Tipo", text="Informação")
tree.heading("Valor", text="Valor")
tree.column("Tipo", width=200, anchor="center")
tree.column("Valor", width=380, anchor="center")
tree.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

# Botão para atualizar
botao = ttk.Button(root, text="Atualizar Informações", command=lambda: [tree.delete(i) for i in tree.get_children()] or atualizar_infos())
botao.grid(row=1, column=0, columnspan=2, pady=10)

# Atualizar
atualizar_infos()
root.mainloop()