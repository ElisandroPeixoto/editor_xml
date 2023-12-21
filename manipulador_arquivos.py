import shutil
import os
import pandas as pd


def copiar_arquivos(nome_arquivo, arquivo_copia, sufixo_copia):
    # Cria o caminho para a cópia na mesma pasta
    caminho_destino = os.path.join(os.path.dirname(arquivo_copia), f'{nome_arquivo}{sufixo_copia}')

    # Copia o arquivo
    shutil.copy2(arquivo_copia, caminho_destino)


def mover_arquivos(diretorio, lista_arquivos):
    for arquivo in range(0, len(lista_arquivos)):
        shutil.move(lista_arquivos[arquivo], diretorio)
