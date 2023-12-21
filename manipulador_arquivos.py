import shutil
import os
import pandas as pd


def copiar_arquivos(planilha_base, arquivo_copia, sufixo_copia):
    # Abre a planilha com os nomes dos equipamentos
    planilha_nomes = pd.read_excel(planilha_base)

    # Extrai os nomes para uma lista
    lista_nomes = [nomes for nomes in planilha_nomes['nome']]

    for a in range(0, len(lista_nomes)):
        # Cria o caminho para a cópia na mesma pasta
        caminho_destino = os.path.join(os.path.dirname(arquivo_copia), f'{lista_nomes[a]}{sufixo_copia}')

        # Copia o arquivo
        shutil.copy2(arquivo_copia, caminho_destino)


def mover_arquivos(diretorio, lista_arquivos):
    for arquivo in range(0, len(lista_arquivos)):
        shutil.move(lista_arquivos[arquivo], diretorio)
