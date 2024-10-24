#!/usr/bin/env python3

import os
import subprocess
import venv
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_project(name, path, domain, libraries):
    """
    Crée un nouveau projet avec la structure spécifiée.
    
    :param name: Nom du projet
    :param path: Chemin où créer le projet
    :param domain: Domaine du projet (ex: "Data Science", "Cybersecurity", "Full Stack")
    :param libraries: Liste des bibliothèques à installer
    """
    project_path = os.path.join(path, name)
    logging.info(f"Création du projet '{name}' dans {project_path}")

    try:
        # Crée le répertoire du projet
        os.makedirs(project_path, exist_ok=True)

        # Crée la structure du projet
        create_project_structure(project_path)

        # Crée l'environnement virtuel
        create_virtual_environment(project_path)

        # Crée requirements.txt et installe les bibliothèques
        create_requirements_and_install(project_path, libraries)

        # Crée main.py avec le template spécifique au domaine
        create_main_file(project_path, domain)

        # Crée README.md
        create_readme(project_path, name, domain)

        logging.info(f"Projet '{name}' créé avec succès")
    except Exception as e:
        logging.error(f"Erreur lors de la création du projet: {str(e)}")
        raise

def create_project_structure(project_path):
    """Crée les sous-répertoires du projet"""
    directories = ["data", "notebooks", "src", "tests"]
    for directory in directories:
        os.makedirs(os.path.join(project_path, directory), exist_ok=True)
    logging.info("Structure du projet créée")

def create_virtual_environment(project_path):
    """Crée un environnement virtuel pour le projet"""
    venv_path = os.path.join(project_path, ".venv")
    venv.create(venv_path, with_pip=True)
    logging.info(f"Environnement virtuel créé dans {venv_path}")

def create_requirements_and_install(project_path, libraries):
    """Crée le fichier requirements.txt et installe les bibliothèques"""
    requirements_path = os.path.join(project_path, "requirements.txt")
    with open(requirements_path, "w") as f:
        f.write("\n".join(libraries))
    
    pip_path = os.path.join(project_path, ".venv", "Scripts", "pip") if os.name == "nt" else os.path.join(project_path, ".venv", "bin", "pip")
    
    try:
        subprocess.run([pip_path, "install", "-r", requirements_path], check=True)
        logging.info("Bibliothèques installées avec succès")
    except subprocess.CalledProcessError as e:
        logging.error(f"Erreur lors de l'installation des bibliothèques: {str(e)}")
        raise

def create_main_file(project_path, domain):
    """Crée le fichier main.py avec le template spécifique au domaine"""
    main_path = os.path.join(project_path, "src", "main.py")
    with open(main_path, "w") as f:
        f.write(get_main_template(domain))
    logging.info(f"Fichier main.py créé pour le domaine {domain}")

def create_readme(project_path, name, domain):
    """Crée un fichier README.md basique"""
    readme_path = os.path.join(project_path, "README.md")
    with open(readme_path, "w") as f:
        f.write(f"# {name}\n\nCe projet est dans le domaine {domain}.\n\n## Description\n\nAjoutez ici une description de votre projet.\n\n## Installation\n\n```\npip install -r requirements.txt\n```\n\n## Utilisation\n\nExpliquez ici comment utiliser votre projet.\n")
    logging.info("Fichier README.md créé")

def get_main_template(domain):
    """Retourne le template approprié pour main.py selon le domaine"""
    templates = {
        "Data Science": """
# Data Science Project Main File

import pandas as pd
import numpy as np

def main():
    # Votre code de data science ici
    pass

if __name__ == "__main__":
    main()
""",
        "Cybersecurity": """
# Cybersecurity Project Main File

def main():
    # Votre code de cybersécurité ici
    pass

if __name__ == "__main__":
    main()
""",
        "Full Stack": """
# Full Stack Project Main File

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Bienvenue dans votre application Full Stack!"

if __name__ == "__main__":
    app.run(debug=True)
"""
    }
    return templates.get(domain, "# Point d'entrée principal de votre projet\n")

if __name__ == "__main__":
    # Test de la fonction create_project
    create_project("test_project", ".", "Data Science", ["numpy", "pandas", "matplotlib"])
