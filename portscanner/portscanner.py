import tkinter as tk
from tkinter import ttk, messagebox
import socket
import threading
import time

open_ports = []
is_scanning = False
lock = threading.Lock()

def scan_port(ip, port, tree):
    global open_ports
    if not is_scanning:
        return
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip, port))
        if result == 0:
            with lock:
                open_ports.append(port)
                tree.insert('', 'end', values=(port, "OPEN"), tags=("open",))
        else:
            tree.insert('', 'end', values=(port, "Closed"), tags=("closed",))
        sock.close()
    except:
        pass

def show_popup(open_ports_count, time_taken):
    popup = tk.Toplevel(root)
    popup.configure(bg="black")
    popup.geometry("500x300")
    popup.title(" Scan Report")

    tk.Label(popup, text="🔷 SCAN COMPLETE 🔷", fg="#00ffff", bg="black",
             font=("Consolas", 20, "bold")).pack(pady=20)

    tk.Label(popup, text=f"✅ {open_ports_count} Open Ports Detected",
             fg="#00ccff", bg="black", font=("Consolas", 14)).pack(pady=10)

    tk.Label(popup, text=f"⏱️ Time Taken: {time_taken:.2f} seconds",
             fg="#00ccff", bg="black", font=("Consolas", 14)).pack(pady=10)

    tk.Button(popup, text="🔒 Close", command=popup.destroy,
              bg="#001f33", fg="#00ffff", font=("Consolas", 12),
              activebackground="#003344", relief="flat", padx=20, pady=5).pack(pady=30)

    popup.transient(root)
    popup.grab_set()
    root.wait_window(popup)

def start_scan(target_entry, start_port_entry, end_port_entry, tree, status_label):
    global open_ports, is_scanning
    open_ports = []
    is_scanning = True
    tree.delete(*tree.get_children())
    start_time = time.time()

    target = target_entry.get().strip()
    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        messagebox.showerror("Invalid host", "❌ Hostname/IP is invalid.")
        return

    try:
        start_port = int(start_port_entry.get())
        end_port = int(end_port_entry.get())
        if start_port < 1 or end_port > 65535 or start_port > end_port:
            raise ValueError
    except:
        messagebox.showerror("Invalid Ports", "❌ Please enter valid port numbers (1–65535).")
        return

    status_label.config(text=f"Scanning {target} ({ip})...")

    def run():
        threads = []
        for port in range(start_port, end_port + 1):
            if not is_scanning:
                break
            t = threading.Thread(target=scan_port, args=(ip, port, tree))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        time_taken = time.time() - start_time
        show_popup(len(open_ports), time_taken)
        status_label.config(text=f"✅ Scan Complete. {len(open_ports)} open ports. ⏱️ {time_taken:.2f}s")

    threading.Thread(target=run).start()

def stop_scan(status_label):
    global is_scanning
    is_scanning = False
    status_label.config(text="⏹️ Scan Stopped by User")

root = tk.Tk()
root.title("Port Scanner")
root.geometry("750x600")
root.configure(bg="black")

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview",
                background="black",
                fieldbackground="black",
                foreground="#00ffff",
                rowheight=25,
                font=("Consolas", 10))
style.map('Treeview', background=[('selected', '#003344')],
                         foreground=[('selected', '#00ffff')])
style.configure("Treeview.Heading",
                background="#001f33",
                foreground="#00ccff",
                font=('Consolas', 11, 'bold'))

tk.Label(root, text=" PORT SCANNER", bg="black", fg="#00ffff",
         font=("Consolas", 16, "bold")).pack(pady=10)

input_frame = tk.Frame(root, bg="black")
input_frame.pack(pady=5)

tk.Label(input_frame, text="Target:", bg="black", fg="#00ccff", font=("Consolas", 10)).grid(row=0, column=0, padx=5)
target_entry = tk.Entry(input_frame, font=("Consolas", 10), width=25)
target_entry.grid(row=0, column=1, padx=5)

tk.Label(input_frame, text="Start Port:", bg="black", fg="#00ccff", font=("Consolas", 10)).grid(row=0, column=2, padx=5)
start_port_entry = tk.Entry(input_frame, font=("Consolas", 10), width=10)
start_port_entry.grid(row=0, column=3, padx=5)

tk.Label(input_frame, text="End Port:", bg="black", fg="#00ccff", font=("Consolas", 10)).grid(row=0, column=4, padx=5)
end_port_entry = tk.Entry(input_frame, font=("Consolas", 10), width=10)
end_port_entry.grid(row=0, column=5, padx=5)

btn_frame = tk.Frame(root, bg="black")
btn_frame.pack(pady=10)

start_btn = ttk.Button(btn_frame, text="▶️ Start Scan", command=lambda: start_scan(target_entry, start_port_entry, end_port_entry, tree, status_label))
start_btn.grid(row=0, column=0, padx=10)

stop_btn = ttk.Button(btn_frame, text="⏹️ Stop Scan", command=lambda: stop_scan(status_label))
stop_btn.grid(row=0, column=1, padx=10)

tree = ttk.Treeview(root, columns=("Port", "Status"), show="headings")
tree.heading("Port", text="Port")
tree.heading("Status", text="Status")
tree.column("Port", width=100)
tree.column("Status", width=150)
tree.tag_configure("open", background="#002b36")
tree.tag_configure("closed", background="#1c1c1c")
tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

status_label = tk.Label(root, text="Awaiting input...", bg="black", fg="#00ffff", font=("Consolas", 10))
status_label.pack(pady=10)

root.mainloop()
