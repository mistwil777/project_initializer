#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from .project_creator import create_project

class ProjectInitializerGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Project Initializer")
        self.window.geometry("600x500")
        
        # Définir l'icône de la fenêtre
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "..", "resources", "icon.png")
        if os.path.exists(icon_path):
            img = tk.PhotoImage(file=icon_path)
            self.window.tk.call('wm', 'iconphoto', self.window._w, img)
        
        self.project_name = tk.StringVar()
        self.project_path = tk.StringVar()
        self.selected_domain = tk.StringVar()
        self.libraries = {}
        
        self.create_widgets()

    def create_widgets(self):
        # Nom du projet
        tk.Label(self.window, text="Nom du projet:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(self.window, textvariable=self.project_name, width=40).grid(row=0, column=1, columnspan=2, padx=5, pady=5)

        # Chemin du projet
        tk.Label(self.window, text="Chemin du projet:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(self.window, textvariable=self.project_path, width=40).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.window, text="Parcourir", command=self.browse_path).grid(row=1, column=2, padx=5, pady=5)

        # Sélection du domaine
        tk.Label(self.window, text="Domaine:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        domains = ["Data Science", "Cybersecurity", "Full Stack"]
        domain_dropdown = ttk.Combobox(self.window, textvariable=self.selected_domain, values=domains, state="readonly")
        domain_dropdown.grid(row=2, column=1, padx=5, pady=5)
        domain_dropdown.bind("<<ComboboxSelected>>", self.update_libraries)

        # Bibliothèques
        tk.Label(self.window, text="Bibliothèques:").grid(row=3, column=0, sticky="nw", padx=5, pady=5)
        self.libraries_frame = tk.Frame(self.window)
        self.libraries_frame.grid(row=3, column=1, columnspan=2, sticky="nsew", padx=5, pady=5)

        # Bouton de création de projet
        tk.Button(self.window, text="Créer le projet", command=self.create_project).grid(row=4, column=1, pady=10)

    def browse_path(self):
        path = filedialog.askdirectory()
        self.project_path.set(path)

    def update_libraries(self, event):
        for widget in self.libraries_frame.winfo_children():
            widget.destroy()

        domain = self.selected_domain.get()
        libraries = self.get_libraries_for_domain(domain)

        canvas = tk.Canvas(self.libraries_frame)
        scrollbar = ttk.Scrollbar(self.libraries_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for i, lib in enumerate(libraries):
            var = tk.BooleanVar()
            cb = tk.Checkbutton(scrollable_frame, text=lib, variable=var)
            cb.grid(row=i, column=0, sticky="w")
            self.libraries[lib] = var

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def get_libraries_for_domain(self, domain):
        if domain == "Data Science":
            return [
                "numpy", "pandas", "matplotlib", "seaborn", "scikit-learn",
                "tensorflow", "keras", "pytorch", "scipy", "statsmodels",
                "plotly", "bokeh", "nltk", "gensim", "spacy",
                "xgboost", "lightgbm", "catboost"
            ]
        elif domain == "Cybersecurity":
            return ["scapy", "pycryptodome", "paramiko", "pyopenssl"]
        elif domain == "Full Stack":
            return ["django", "flask", "fastapi", "sqlalchemy"]
        return []

    def create_project(self):
        name = self.project_name.get()
        path = self.project_path.get()
        domain = self.selected_domain.get()
        selected_libraries = [lib for lib, var in self.libraries.items() if var.get()]

        if not name or not path or not domain:
            messagebox.showerror("Erreur", "Le nom du projet, le chemin et le domaine sont requis!")
            return

        progress_window = tk.Toplevel(self.window)
        progress_window.title("Création du projet")
        progress_window.geometry("300x100")

        label = tk.Label(progress_window, text="Création en cours...")
        label.pack(pady=20)

        progress_bar = ttk.Progressbar(progress_window, mode='indeterminate')
        progress_bar.pack(pady=10)
        progress_bar.start()

        def create_project_thread():
            try:
                create_project(name, path, domain, selected_libraries)
                self.window.after(0, lambda: self.show_success(progress_window))
            except Exception as e:
                self.window.after(0, lambda: self.show_error(str(e), progress_window))

        threading.Thread(target=create_project_thread, daemon=True).start()

    def show_success(self, progress_window):
        progress_window.destroy()
        messagebox.showinfo("Succès", f"Projet '{self.project_name.get()}' créé avec succès!")
        self.window.quit()
        self.window.destroy()

    def show_error(self, error_message, progress_window):
        progress_window.destroy()
        messagebox.showerror("Erreur", error_message)

    def run(self):
        self.window.mainloop()
