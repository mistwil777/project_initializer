#!/usr/bin/env python3

import os
import sys

# Ajoute le répertoire parent au chemin Python pour pouvoir importer les modules du projet
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.gui import ProjectInitializerGUI

if __name__ == "__main__":
    app = ProjectInitializerGUI()
    app.run()
