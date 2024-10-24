#!/usr/bin/env python3

import os
import sys
import platform

def create_desktop_shortcut():
    # Obtient le chemin du script principal
    main_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "main.py"))
    
    # Obtient le chemin du bureau
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    
    # Obtient le chemin de l'icône
    icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "resources", "icon.png"))
    
    if platform.system() == "Windows":
        import winshell
        from win32com.client import Dispatch
        
        shortcut_path = os.path.join(desktop, "Project Initializer.lnk")
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{main_script}"'
        shortcut.WorkingDirectory = os.path.dirname(main_script)
        shortcut.IconLocation = icon_path
        shortcut.save()
        
    elif platform.system() == "Linux":
        shortcut_path = os.path.join(desktop, "Project Initializer.desktop")
        
        with open(shortcut_path, "w") as shortcut:
            shortcut.write("[Desktop Entry]\n")
            shortcut.write("Version=1.0\n")
            shortcut.write("Type=Application\n")
            shortcut.write("Name=Project Initializer\n")
            shortcut.write(f"Exec={sys.executable} \"{main_script}\"\n")
            shortcut.write(f"Icon={icon_path}\n")
            shortcut.write("Terminal=false\n")
        
        os.chmod(shortcut_path, 0o755)
        
    elif platform.system() == "Darwin":  # macOS
        import plistlib
        
        app_name = "Project Initializer.app"
        app_path = os.path.join(desktop, app_name)
        os.makedirs(os.path.join(app_path, "Contents", "MacOS"), exist_ok=True)
        os.makedirs(os.path.join(app_path, "Contents", "Resources"), exist_ok=True)
        
        # Créer le fichier Info.plist
        info_plist = {
            'CFBundleExecutable': 'launcher.sh',
            'CFBundleIconFile': 'icon.png',
            'CFBundleName': 'Project Initializer',
        }
        with open(os.path.join(app_path, "Contents", "Info.plist"), "wb") as f:
            plistlib.dump(info_plist, f)
        
        # Créer le script launcher.sh
        with open(os.path.join(app_path, "Contents", "MacOS", "launcher.sh"), "w") as f:
            f.write("#!/bin/bash\n")
            f.write(f"{sys.executable} \"{main_script}\"\n")
        os.chmod(os.path.join(app_path, "Contents", "MacOS", "launcher.sh"), 0o755)
        
        # Copier l'icône
        import shutil
        shutil.copy(icon_path, os.path.join(app_path, "Contents", "Resources", "icon.png"))
    
    else:
        print("Unsupported operating system")
        return

    print(f"Shortcut created on the desktop: {shortcut_path}")

if __name__ == "__main__":
    create_desktop_shortcut()
