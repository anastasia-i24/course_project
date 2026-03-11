import tkinter as tk
from tkinter import ttk, messagebox
import os
import generate_par

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор бизнес-процесса")
        self.root.geometry("500x300")
        self.entries = [] 
        ttk.Label(root, text="Name", font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=10, pady=10)
        ttk.Label(root, text="Group", font=('Arial', 10, 'bold')).grid(row=0, column=1, padx=10, pady=10)
        self.frame = ttk.Frame(root)
        self.frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
        self.add_row()
        btn_frame = ttk.Frame(root)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=5)
        ttk.Button(btn_frame, text="+ Добавить", command=self.add_row).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Запустить", command=self.generate).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Очистить", command=self.clear).pack(side=tk.LEFT, padx=5)
        self.status = tk.StringVar()
        self.status.set("Введите данные и нажмите Запустить")
        ttk.Label(root, textvariable=self.status, relief=tk.SUNKEN).grid(row=3, column=0, columnspan=2, sticky='ew', padx=10, pady=10)
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(1, weight=1)
    
    
    def add_row(self):
        row = len(self.entries)
        e1 = ttk.Entry(self.frame, width=30)
        e2 = ttk.Entry(self.frame, width=30)
        e1.grid(row=row, column=0, padx=5, pady=2, sticky='ew')
        e2.grid(row=row, column=1, padx=5, pady=2, sticky='ew')
        self.entries.append((e1, e2))
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
    

    def clear(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.entries = []
        self.add_row()
    

    def generate(self):
        lanes = []
        for e1, e2 in self.entries:
            name = e1.get().strip()
            group = e2.get().strip()
            if name and group:
                lanes.append({'name': name, 'group': group})
        if not lanes:
            messagebox.showwarning("Внимание", "Не введены данные")
            return
        self.status.set("Генерация...")
        self.root.update()
        success, msg = generate_par(lanes)
        self.status.set(msg)
        if success:
            messagebox.showinfo("Успех", 
                f"Файл создан: {os.path.abspath('result.par')}")
        else:
            messagebox.showerror("Ошибка", msg)
