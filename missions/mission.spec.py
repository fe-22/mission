# Arquivo mission.spec

import os

def on_start():
    # Obtém o caminho absoluto do diretório 'dist'
    dist_path = os.path.abspath('dist')

    # Imprime o caminho absoluto do diretório 'dist'
    print("O caminho absoluto do diretório 'dist' é:", dist_path)