import tkinter as tk
from tkinter import messagebox, ttk

expression = ""
history = []

# Fungsi tombol
def click(item):
    global expression
    expression += str(item)
    input_text.set(expression)

def equal():
    global expression, history
    try:
        result = str(eval(expression))
        history.append(f"{expression} = {result}")
        if len(history) > 50:
            history[:] = history[-50:]
        update_history()
        input_text.set(result)
        expression = result
    except:
        input_text.set("Error")
        expression = ""

def clear():
    global expression
    expression = ""
    input_text.set("")

# Update riwayat di listbox utama
def update_history():
    history_listbox.delete(0, tk.END)
    for item in history:
        history_listbox.insert(tk.END, item)
    history_listbox.yview_moveto(1)

# Klik riwayat di main window
def click_history(event):
    global expression
    selection = history_listbox.curselection()
    if selection:
        selected_text = history_listbox.get(selection[0])
        expression = selected_text.split('=')[0].strip()
        input_text.set(expression)

# Menu Riwayat Interaktif
def show_history_window():
    win = tk.Toplevel(root)
    win.title("Riwayat Lengkap")
    win.geometry("350x400")
    win.configure(bg="#1e1e1e")

    frame = tk.Frame(win, bg="#1e1e1e")
    frame.pack(fill='both', expand=True, padx=10, pady=10)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side='right', fill='y')

    listbox = tk.Listbox(frame, bg="#333333", fg="white", font=('Arial', 14),
                         selectbackground="#4caf50", yscrollcommand=scrollbar.set)
    listbox.pack(fill='both', expand=True)
    scrollbar.config(command=listbox.yview)

    # Isi riwayat
    for item in history:
        listbox.insert(tk.END, item)

    # Klik riwayat untuk isi layar utama
    def click_history_window(event):
        global expression
        selection = listbox.curselection()
        if selection:
            selected_text = listbox.get(selection[0])
            expression = selected_text.split('=')[0].strip()
            input_text.set(expression)
            win.destroy()  # tutup jendela riwayat

    listbox.bind("<<ListboxSelect>>", click_history_window)

    # Hapus riwayat
    def clear_history():
        global history
        if messagebox.askyesno("Konfirmasi", "Hapus semua riwayat?"):
            history.clear()
            listbox.delete(0, tk.END)
            update_history()

    clear_btn = tk.Button(win, text="Hapus Riwayat", bg="#f44336", fg="white", font=('Arial', 14), command=clear_history)
    clear_btn.pack(pady=10)

# Hover dan klik tombol efek smartphone
def smooth_hover(btn, target_color, steps=10, delay=15):
    start_color = btn['bg']
    start_rgb = root.winfo_rgb(start_color)
    target_rgb = root.winfo_rgb(target_color)
    diff = [(t - s)/steps for s, t in zip(start_rgb, target_rgb)]
    def step(i=0):
        if i > steps: return
        new_color = "#%04x%04x%04x" % tuple(int(start + d*i) for start, d in zip(start_rgb, diff))
        btn.config(bg=new_color)
        root.after(delay, lambda: step(i+1))
    step()

def button_press_effect(btn):
    original_color = btn['bg']
    btn.config(bg="#222222")
    root.after(100, lambda: btn.config(bg=original_color))

def bind_hover_click(btn, normal, hover, action):
    btn.bind("<Enter>", lambda e: smooth_hover(btn, hover))
    btn.bind("<Leave>", lambda e: smooth_hover(btn, normal))
    btn.config(command=lambda b=btn: [button_press_effect(b), action()])

# Window utama
root = tk.Tk()
root.title("Kalkulator Smartphone Modern")
root.geometry("400x700")
root.configure(bg="#1e1e1e")

# Menu bar
menubar = tk.Menu(root)
history_menu = tk.Menu(menubar, tearoff=0)
history_menu.add_command(label="Lihat Riwayat", command=show_history_window)
menubar.add_cascade(label="Riwayat", menu=history_menu)
root.config(menu=menubar)

# Input layar
input_text = tk.StringVar()
history_text = tk.StringVar()

input_frame = tk.Frame(root, bg="#1e1e1e")
input_frame.pack(pady=10)

input_field = tk.Entry(input_frame, textvariable=input_text, font=('Arial', 28, 'bold'),
                       bd=0, bg="#333333", fg="white", justify='right', width=15)
input_field.grid(row=0, column=0, ipadx=10, ipady=15)

# Frame tombol
btns_frame = tk.Frame(root, bg="#1e1e1e")
btns_frame.pack()

buttons = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['0', '.', '=', '+']
]

default_color = "#555555"
hover_color = "#888888"
equal_color = "#4caf50"
clear_color = "#f44336"

def create_btn(text, bg, action):
    btn = tk.Button(btns_frame, text=text, fg="white", bg=bg, font=('Arial', 20, 'bold'),
                    width=5, height=2)
    bind_hover_click(btn, bg, hover_color, action)
    return btn

# Buat tombol
for i in range(4):
    for j in range(4):
        btn_text = buttons[i][j]
        if btn_text == "=":
            btn = create_btn(btn_text, equal_color, equal)
        else:
            btn = create_btn(btn_text, default_color, lambda t=btn_text: click(t))
        btn.grid(row=i, column=j, padx=5, pady=5)

# Tombol Clear
clear_btn = tk.Button(root, text='C', fg="white", bg=clear_color, font=('Arial', 20, 'bold'), width=22, height=2)
bind_hover_click(clear_btn, clear_color, hover_color, clear)
clear_btn.pack(pady=10)

# Riwayat singkat di main window
history_label = tk.Label(root, text="Riwayat Singkat:", bg="#1e1e1e", fg="white", font=('Arial', 16, 'bold'))
history_label.pack(anchor='w', padx=20)

history_listbox = tk.Listbox(root, listvariable=history_text, bg="#333333", fg="white",
                             font=('Arial', 14), height=8, selectbackground="#4caf50")
history_listbox.pack(fill='both', padx=20, pady=5)
history_listbox.bind("<<ListboxSelect>>", click_history)

root.mainloop()
