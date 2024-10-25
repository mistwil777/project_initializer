#!/usr/bin/env python3

import os
import subprocess

def create_desktop_shortcut():
    # Obtient le chemin du script principal
    main_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "main.py"))
    
    # Convertit le chemin Linux en chemin Windows
    main_script_windows = subprocess.getoutput(f"wslpath -w '{main_script}'")
    
    # Obtient le chemin du bureau Windows
    desktop = subprocess.getoutput("cmd.exe /c echo %USERPROFILE%\\Desktop").strip()
    
    # Définit le chemin du raccourci
    shortcut_path = os.path.join(desktop, "Project Initializer.lnk")
    
    # Définit le chemin de l'icône
    icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "resources", "icon.png"))
    icon_path_windows = subprocess.getoutput(f"wslpath -w '{icon_path}'")
    
    # Crée le raccourci Windows en utilisant un script VBS
    vbs_content = f"""
    Set WshShell = CreateObject("WScript.Shell")
    Set Shortcut = WshShell.CreateShortcut("{shortcut_path}")
    Shortcut.TargetPath = "wsl.exe"
    Shortcut.Arguments = "python '{main_script_windows}'"
    Shortcut.WorkingDirectory = "{os.path.dirname(main_script_windows)}"
    Shortcut.IconLocation = "{icon_path_windows}"
    Shortcut.Save
    """
    
    # Écrit le script VBS dans un fichier temporaire
    with open("temp_shortcut.vbs", "w") as vbs_file:
        vbs_file.write(vbs_content)
    
    # Exécute le script VBS
    subprocess.run(["cmd.exe", "/c", "cscript", "//Nologo", "temp_shortcut.vbs"], check=True)
    
    # Supprime le fichier VBS temporaire
    os.remove("temp_shortcut.vbs")
    
    print(f"Raccourci créé sur le bureau Windows : {shortcut_path}")

if __name__ == "__main__":
    create_desktop_shortcut()
