import shutil


def mover_arquivos(diretorio, lista_arquivos):
    for arquivo in range(0, len(lista_arquivos)):
        shutil.move(lista_arquivos[arquivo], diretorio)
