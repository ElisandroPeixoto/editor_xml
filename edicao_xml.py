import xml.etree.ElementTree as Et


class EditorXML:
    def __init__(self, arquivo):
        # Carrega o arquivo XML
        self.arquivo = arquivo
        self.tree = Et.parse(arquivo)
        self.root = self.tree.getroot()

    def editar_ip(self, ip):
        # Encontrar a tag com o endereco IP
        device = self.root.find('Device')
        connection = device.find('Connection')
        setting_pages = connection.find('SettingPages')
        setting_page = setting_pages.findall('SettingPage')
        setting_page_0 = setting_page[0]
        row = setting_page_0.findall('Row')
        row_2 = row[2]
        setting = row_2.findall('Setting')
        setting_1 = setting[1]

        # Editando o endereco IP
        setting_1.find('Value').text = ip

        # Salva a modificacao
        self.tree.write(self.arquivo)

    def ativar_wordbit(self, wordbit):
        # Encontrar a tag que contem as wordbits
        device = self.root.find('Device')
        connection = device.find('Connection')
        setting_pages = connection.find('SettingPages')
        setting_page = setting_pages.findall('SettingPage')

        # Procura pela "SettingPage" que contem o "Meter"
        for p in setting_page:
            nome = p.find('Name').text
            if nome == 'Meter':
                row = p.findall('Row')  # Procura pela Row

                for r in row:
                    setting_row = r.findall('Setting')

                    for s in setting_row:
                        valor = s.find('Value').text
                        if valor == wordbit:
                            # Ativa a wordbit na coluna "Enable"
                            setting_row[0].find('Value').text = 'True'

                            # Salva a modificacao
                            self.tree.write(self.arquivo)

    def substituir_texto(self, texto_original, texto_novo):
        """Substitui o texto default para o texto do novo drive"""
        for element in self.root.iter():
            if element.text is not None and texto_original in element.text:
                element.text = element.text.replace(texto_original, texto_novo)

        # Salva a modificacao
        self.tree.write(self.arquivo)

    def criar_relig_satisf(self, lista_equips):
        """Cria o programa RELIG_SATISF"""

        # Acessa a tag que contem o programa
        pou = self.root.find('POU')
        content = pou.find('Content')
        implementation = content.find('Implementation')

        texto_final = []  # Armazena as linhas de texto de cada IED
        for ieds in lista_equips:  # Itera sobre a lista de IEDs para escrever as linhas de codigo de cada um
            texto_final.append(
                f"""{ieds}_RELIGAMENTO := FUNC_RELIG({ieds}_CMD_SEL.FM_INST_SH1.stVal,{ieds}_CMD_SEL.FM_INST_SH2.stVal,{ieds}_CMD_SEL.FM_INST_SH3.stVal,{ieds}_CMD_SEL.FM_INST_SH4.stVal);\r{ieds}_DNP.AI_00048.instMag := {ieds}_RELIGAMENTO;
                """)

        implementation.text = "\r".join(texto_final)  # Junta as linhas de codigo de cada IED em um unico texto
        self.tree.write(self.arquivo)  # Escreve no arquivo

    def criar_gvl(self, lista_equips):
        gvl = self.root.find('GVL')
        content = gvl.find('Content')

        variaveis_com_monitor = []
        variaveis_religamento = []

        for ieds in lista_equips:
            variaveis_com_monitor.append(
                f"""    {ieds}_COM_MONITOR : INT;""")

            variaveis_religamento.append(
                f"""    {ieds}_RELIGAMENTO: INT;""")

        # Estruturas do Codigo
        header = ["VAR_GLOBAL"]
        comentario_1 = ["\r// MONITORAMENTO DE COMANDOS"]
        comentario_2 = ["\r// MONITORAMENTO DO CICLO DE RELIGAMENTO"]
        footer = ["END_VAR"]

        lista_final = header + comentario_1 + variaveis_com_monitor + comentario_2 + variaveis_religamento + footer

        content.text = "\r".join(lista_final)
        self.tree.write('VARIAVEIS_GLOBAIS.xml')
