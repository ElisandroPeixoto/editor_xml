from edicao_xml import EditorXML
import pandas as pd
from manipulador_arquivos import copiar_arquivos, mover_arquivos

# Planilha Base
arquivo_planilha_base = 'lista_arquivos.xlsx'
planilha_arquivos = pd.read_excel(arquivo_planilha_base)

# Listas Base
# Arquivos Protocolo SEL
nomes_arquivos = [nome_arquivo for nome_arquivo in planilha_arquivos['arquivos']]

# Programa Comandos
nomes_programas = [nome_programa for nome_programa in planilha_arquivos['programas']]

# Nomes para RELIG_SATISF e GVL
nomes_equipamentos = [nome_equip for nome_equip in planilha_arquivos['nome']]

# Wordbits a serem ativadas nos drives Protocolo SEL
wordbits_padrao = ['SH0', 'SH1', 'SH2', 'SH3', 'SH4', 'RB01', 'RB02', 'RB03', 'RB04', 'RB05', 'RB06', 'RB07', 'RB08',
                   'RB09', 'RB10', 'RB11', 'RB12', 'OC', 'CC', 'SV10T', 'LT01', 'LT02', 'LT03', 'LT07', 'LT11']

wordbits_311c = ['SH0', 'SH1', 'SH2', 'SH3', 'SH4', 'RB1', 'RB2', 'RB3', 'RB4', 'RB5', 'RB6', 'OC', 'CC', 'SV10T',
                 'LT1', 'LT2', 'LT3']

wordbits_751a = ['SH0', 'SH1', 'SH2', 'SH3', 'SH4', 'RB01', 'RB02', 'RB03', 'RB04', 'RB05', 'RB06', 'RB11', 'RB12',
                 'SV10T', 'LT06', 'LT08', 'LT11']

wordbits_351a = ['SH0', 'SH1', 'SH2', 'SH3', 'SH4', 'RB1', 'RB2', 'RB3', 'RB4', 'RB5', 'RB6', 'RB9', 'RB10', 'LT1',
                 'LT2', 'LT3', 'LT7', 'SV10T', 'OC', 'CC']

# -------------------------------------------------------------------------------------

lista_modelo_ieds = []

# Copia os arquivos
for a in range(0, len(planilha_arquivos['nome'])):

    modelo_ied = planilha_arquivos['ied'][a]
    drive_SEL = f'{modelo_ied}_CMD_SEL.xml'
    programa_comandos = f'{modelo_ied}_COMANDOS.xml'

    copiar_arquivos(planilha_arquivos['nome'][a], drive_SEL, '_CMD_SEL.xml')
    copiar_arquivos(planilha_arquivos['nome'][a], programa_comandos, '_COMANDOS.xml')

    lista_modelo_ieds.append(modelo_ied)  # Armazena o modelo dos IEDs para ser usado na renomeacao dos arquivos

# Feedback da copia dos arquivos
print('Copia dos arquivos Protocolo SEL: Finalizado')
print('Copia dos Programas de Monitoramento dos Comandos: Finalizado')
print("Aguardando geração dos arquivos XML...")

# -------------------------------------------------------------------------------------

# Itera sobre os arquivos que resultarão nos drives Protocolo SEL
for a in range(0, len(nomes_arquivos)):

    # Ajuste dos arquivos "_CMD_SEL.xml"
    ajuste = EditorXML(nomes_arquivos[a])  # Instancia o editor do drive Protocolo SEL
    ajuste.editar_ip(planilha_arquivos['ip'][a])  # Altera o IP conforme a planilha
    ajuste.substituir_texto(lista_modelo_ieds[a], planilha_arquivos['nome'][a])  # Altera o nome do arquivo

    # Selecao da lista de wordbits conforme modelo do IED
    if planilha_arquivos['ied'][a] == 'IED311C':
        lista_wordbits = wordbits_311c
    elif planilha_arquivos['ied'][a] == 'IED351A':
        lista_wordbits = wordbits_351a
    elif planilha_arquivos['ied'][a] == 'IED751A':
        lista_wordbits = wordbits_751a
    else:
        lista_wordbits = wordbits_padrao

    # Ativacao das Wordbits
    for w in lista_wordbits:
        ajuste.ativar_wordbit(w)

    # Ajuste dos arquivos "_COMANDOS.xml"
    programa_comandos = EditorXML(nomes_programas[a])
    programa_comandos.substituir_texto(lista_modelo_ieds[a], planilha_arquivos['nome'][a])

    print(f'Ajustado: {planilha_arquivos["nome"][a]}')


# -------------------------------------------------------------------------------------

# Geracao do Programa RELIG_SATISF
prg_relig = EditorXML('RELIG_SATISF.xml')  # Instancia o gerador do programa RELIG_SATISF
prg_relig.criar_relig_satisf(nomes_equipamentos)

# Geracao da GVL
prg_gvl = EditorXML('VARIAVEIS_GLOBAIS.xml')  # Instancia o gerador da GVL
prg_gvl.criar_gvl(nomes_equipamentos)

# Move os arquivos para suas respectivas pastas
mover_arquivos('./Protocolo SEL', nomes_arquivos)
mover_arquivos('./Programs', nomes_programas)
