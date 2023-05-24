from pandas import read_excel, read_csv, notna
from os import path, system, getcwd, remove
from PyPDF2 import PdfReader
from re import search, compile
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from random import uniform


def filtrar_leiloes():

    # Variaveis
    global contatos_filtrados

    # ---------- Filtra o leilão connect ---------- #
    try:
        base = read_excel('arquivos/connect.xlsx', header=2)
        for contador in range(base.shape[0]):
            nome = base['NOME'][contador].replace('\n', ' ').upper()
            celular = base['CELULAR'][contador].translate(str.maketrans('', '', substituir))
            if len(celular) == 10:
                celular = celular[:2] + '9' + celular[2:]
            if len(celular) == 11 and notna(celular):
                contatos_filtrados.append([nome, celular])
        print('Filtragem do leilão connect concluido!')
    except:
        pass

    # ---------- Filtra o leilão programa ---------- #
    try:
        base = read_excel('arquivos/programa.xlsx')
        for contador in range(base.shape[0]):
            try:
                if int(base['CPF / CNPJ'][contador].translate(str.maketrans('', '', substituir))):
                    nome = base['CLIENTE'][contador].upper()
            except:
                for contadora in range(base.shape[1]):
                    dado = base.iloc[contador][contadora]
                    if notna(dado) and 'celular' in dado.lower():
                        celular = dado.split()[2].translate(str.maketrans('', '', substituir))
                        if len(celular) == 10:
                            celular = celular[:2] + '9' + celular[2:]
                        if len(celular) == 11:
                            contatos_filtrados.append([nome, celular])
        print('Filtragem do leilão programa concluido!')
    except:
        pass

    # ---------- Filtra o leilão central ---------- #
    try:
        base = read_excel('arquivos/central.xlsx', header=9)
        email = True
        for contador in range(base.shape[0]):
            if email:
                nome = base.iloc[contador][0]
                email = False
            for contadora in range(base.shape[1]):
                dado = base.iloc[contador][contadora]
                if notna(dado) and 'cel' in dado.lower():
                    celular = dado.split()[2].translate(str.maketrans('', '', substituir))
                    if len(celular) == 10:
                        celular = celular[:2] + '9' + celular[2:]
                    if len(celular) == 11:
                        contatos_filtrados.append([nome, celular])
                try:
                    if 'email' in dado.lower():
                        email = True
                except:
                    pass
        print('Filtragem do leilão central concluido!')
    except:
        pass

    # ---------- Filtra o leilão nicolau ---------- #
    try:
        pdf = PdfReader('arquivos/nicolau.pdf')
        numeros = []
        contatos = []
        for contador in range(len(pdf.pages)):
            pagina = pdf.pages[contador]
            conteudo = pagina.extract_text().splitlines()
            for contadora in range(len(conteudo)):
                if search(compile(r'\d{6,7}-\d{4}'), conteudo[contadora].replace(' ', '').replace('(', '').replace(')', '')):
                    if 'CELULAR' in conteudo[contadora] or 'COMERCIAL' in conteudo[contadora] or 'CELULAR' in conteudo[contadora + 1] or 'COMERCIAL' in conteudo[contadora + 1]:
                        numeros.append(search(compile(r'\d{6,7}-\d{4}'), conteudo[contadora].replace(' ', '').replace('(', '').replace(')', '')))
                elif search('DADOS P/', conteudo[contadora]):
                    if search(compile(r':(.+)'), conteudo[contadora - 1]):
                        nome = search(compile(r':(.+)'), conteudo[contadora - 1])
                    elif search(compile(r':(.+)'), conteudo[contadora - 2]):
                        nome = search(compile(r':(.+)'), conteudo[contadora - 2] + conteudo[contadora - 1])
            for numero in numeros:
                contatos.append([nome.group(1), numero.group(0).replace('-', '')])
            numeros.clear()
        contatos = [[contato[0], contato[1][:2] + '9' + contato[1][2:]] if len(contato[1]) == 10 else contato for contato in contatos]
        telefones_vistos = set()
        for contato in contatos:
            telefone = contato[1]
            if telefone not in telefones_vistos and telefone[3] not in ['2', '3', '4', '5']:
                telefones_vistos.add(telefone)
                contatos_filtrados.append(contato)
        print('Filtragem do leilão nicolau concluido!')
    except:
        pass

    print(f'Quantiade de contatos filtrados: {len(contatos_filtrados)}')

    print('\n------------------------------\n')


def filtrar_banco_de_dados():

    # Variaveis
    global contatos_filtrados

    try:
        base = read_excel('arquivos/banco.xlsx')
        for contador in range(base.shape[0]):
            nome = str(base.iloc[contador][0]).replace('\n', ' ').upper()
            celular = str(base.iloc[contador][1]).translate(str.maketrans('', '', substituir))
            contatos_filtrados.append([nome, celular])
        print('Filtragem do banco de dados concluido!')
        print('\n------------------------------\n')
    except:
        pass


# ---------- Configura o navegador ---------- #
def inicializar_navegador():

    # Variaveis
    global navegador

    # Configura o navegador
    options = ChromeOptions()
    options.add_experimental_option('prefs', {'download.default_directory': fr'{getcwd()}\arquivos'})
    options.add_argument(fr'--user-data-dir={path.expanduser("~")}\AppData\Local\Google\Chrome\User Data\Profile 1')
    options.add_argument('--mute-audio')
    navegador = Chrome(options=options)
    navegador.maximize_window()


def cadastrar_contatos():

    # Variaveis
    global contatos_cadastrados
    global contatos_novos
    global contatos_filtrados
    global navegador

    # Entra nos contatos do Gmail
    navegador.get('https://contacts.google.com')
    sleep(uniform(1, 2))

    # Espera a pessoa realizar o login
    while True:
        try:
            if navegador.find_element(By.CLASS_NAME, 'VfPpkd-BIzmGd.VfPpkd-BIzmGd-OWXEXe-X9G3K.bgpk6e.gl6QPb'):
                break
        except:
            pass

    # Deleta o arquivo csv com os contatos cadastrados no google caso exista
    if path.exists(fr'{getcwd()}\arquivos\contacts.csv'):
        remove(fr'{getcwd()}\arquivos\contacts.csv')

    # Clica em exportar para abrir o modal
    bloco = WebDriverWait(navegador, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'MmLA2b.ca2xib')))
    botoes = WebDriverWait(bloco, 10).until(expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, 'VfPpkd-Bz112c-LgbsSe.yHy1rc.eT1oJ.mN1ivc.ebDMpf')))
    for botao in botoes:
        if 'upload' in botao.text:
            botao.click()
    sleep(uniform(1, 2))

    # Clica em exportar no modal
    modal = WebDriverWait(navegador, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'llhEMd.iWO5td')))
    WebDriverWait(modal, 10).until(expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, 'VfPpkd-LgbsSe.ksBjEc.lKxP2d.LQeN7')))[1].click()
    sleep(uniform(1, 2))

    try:
        # Abre o arquivo
        base = read_csv('arquivos/contacts.csv')
        # Pega os telefones cadastrados
        contatos_cadastrados = base['Phone 1 - Value'].values
        # Trata os telefones
        contatos_cadastrados = [contato.translate(str.maketrans('', '', substituir)) for contato in contatos_cadastrados]
        # Filtra os telefones novos
        contatos_novos = [contato for contato in contatos_filtrados if contato[1] not in contatos_cadastrados]
    except:
        contatos_novos = contatos_filtrados

    # Verifica se existem contatos novos
    if len(contatos_novos) > 0:

        # Loop para realizar o cadastro de todos os compradores
        for contato in contatos_novos:

            # Clica em criar contato
            WebDriverWait(navegador, 10).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, 'U26fgb.iZrPLc'))).click()
            sleep(uniform(1, 2))

            # Clica em criar um contato
            modal = WebDriverWait(navegador, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'JPdR6b.e5Emjc.qjTEB')))
            WebDriverWait(modal, 10).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, 'z80M1'))).click()
            sleep(uniform(1, 2))

            # Pega a parte do cadastro
            pagina = WebDriverWait(navegador, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'MCcOAc.IqBfM.ecJEib.EWZcud.k8Lt0.cjGgHb.d8Etdd.LcUz9d')))
            cwiz = WebDriverWait(pagina, 10).until(expected_conditions.presence_of_all_elements_located((By.TAG_NAME, 'c-wiz')))

            # Preenche o input do nome
            WebDriverWait(cwiz[-2], 10).until(expected_conditions.presence_of_element_located((By.XPATH, 'div/div[1]/div[2]/div/div/div[1]/div/div/div[2]/div[2]/div[1]/div/label/input'))).send_keys(contato[0])
            sleep(uniform(1, 2))

            # Preenche o input do telefone
            WebDriverWait(cwiz[-2], 10).until(expected_conditions.presence_of_element_located((By.XPATH, 'div/div[1]/div[2]/div/div/div[6]/div/div/div[2]/div[1]/div[2]/label/input'))).send_keys(contato[1])
            sleep(uniform(1, 2))

            # Clica em salvar
            WebDriverWait(cwiz[-2], 10).until(expected_conditions.element_to_be_clickable((By.XPATH, 'div/div[1]/div[1]/div/div[1]/div[2]/div[2]/div[2]'))).click()
            sleep(uniform(4, 6))

        # Espera 1 minuto para que todos os novos contatos sejam sincronizados com o WhatsApp
        sleep(60)

    # Informa o usuario caso não exista contatos novos para salvar
    else:
        print('Não existem contatos novos para cadastrar!')


def enviar_mensagem():

    # Variaveis
    global contatos_filtrados
    global navegador

    # Entra no WhatsApp Web
    navegador.get('https://web.whatsapp.com')
    sleep(uniform(1, 2))

    # Espera a pessoa ler o QRCODE caso não esteja logado
    while True:
        try:
            navegador.find_element(By.CLASS_NAME, 'landing-title._2K09Y')
        except:
            break

    # Loop para enviar a mensagem para todos os compradores
    contador = 0
    while contador <= len(contatos_filtrados):

        # Pula o contato caso tenha o mesmo nome do anterior
        if contatos_filtrados[contador - 1][0] == contatos_filtrados[contador][0]:
            contador += 1
            continue

        # Verifica se o contato existe
        try:

            # Clica na aba contatos
            cabecalho = WebDriverWait(navegador, 20).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'g0rxnol2.ercejckq.cm280p3y.p357zi0d.gndfcl4n.kcgo1i74.ln8gz9je.e8h85j61.emrlamx0.aiput80m.lyvj5e2u.l9g3jx6n.f6ipylw5')))
            botao_contatos = WebDriverWait(cabecalho, 10).until(expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, '_3OtEr')))[-2]
            WebDriverWait(cabecalho, 10).until(expected_conditions.element_to_be_clickable(botao_contatos)).click()
            sleep(uniform(1, 2))

            # Busca o contato
            WebDriverWait(navegador, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'selectable-text.copyable-text.iq0m558w'))).send_keys(contatos_filtrados[contador][0])
            sleep(uniform(1, 2))

            # Pega o bloco dos contatos
            bloco = WebDriverWait(navegador, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'g0rxnol2.g0rxnol2.thghmljt.p357zi0d.rjo8vgbg.ggj6brxn.f8m0rgwh.gfz4du6o.ag5g9lrv.bs7a17vp')))
            botoes = bloco.find_elements(By.CLASS_NAME, '_199zF._3j691')

            # Loop para a quantidade de contatos com o mesmo nome
            for contadora in range(len(botoes)):

                # Pega o bloco dos contatos
                bloco = WebDriverWait(navegador, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'g0rxnol2.g0rxnol2.thghmljt.p357zi0d.rjo8vgbg.ggj6brxn.f8m0rgwh.gfz4du6o.ag5g9lrv.bs7a17vp')))
                botoes = bloco.find_elements(By.CLASS_NAME, '_199zF._3j691')
                botoes[contadora].click()
                sleep(uniform(1, 2))

                # Caso exista um texto
                if texto:

                    # Escreve o texto
                    for mensagem in texto.splitlines():
                        ActionChains(navegador).send_keys(mensagem).key_down(Keys.CONTROL).key_down(Keys.ENTER).key_up(Keys.CONTROL).key_up(Keys.ENTER).perform()
                    sleep(uniform(1, 2))

                    # Envia a mensagem
                    WebDriverWait(navegador, 10).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, '_2xy_p._3XKXx'))).click()
                    sleep(uniform(1, 2))

                # Caso exista um arquivo
                if arquivo:

                    # Clica no clipe
                    WebDriverWait(navegador, 10).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, '_1OT67'))).click()
                    sleep(uniform(1, 2))

                    # Coloca o arquivo no input
                    documento = WebDriverWait(navegador, 10).until(expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, 'Iaqxu.FCS6Q._1LsXI')))[0]
                    WebDriverWait(documento, 10).until(expected_conditions.presence_of_element_located((By.XPATH, 'button/input'))).send_keys(fr'{getcwd()}\arquivos\{arquivo}')
                    sleep(uniform(1, 2))

                    # Envia o arquivo
                    WebDriverWait(navegador, 10).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, '_3wFFT'))).click()
                    sleep(uniform(1, 2))

                # Quebra o loop caso seja o ultimo contato com o mesmo nome
                if contadora == len(botoes) - 1:
                    contador += len(botoes)
                    break

                # Clica na aba contatos
                cabecalho = WebDriverWait(navegador, 20).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'g0rxnol2.ercejckq.cm280p3y.p357zi0d.gndfcl4n.kcgo1i74.ln8gz9je.e8h85j61.emrlamx0.aiput80m.lyvj5e2u.l9g3jx6n.f6ipylw5')))
                botao_contatos = WebDriverWait(cabecalho, 10).until(expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, '_3OtEr')))[-2]
                WebDriverWait(cabecalho, 10).until(expected_conditions.element_to_be_clickable(botao_contatos)).click()
                sleep(uniform(1, 2))

                # Busca o contato
                WebDriverWait(navegador, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'selectable-text.copyable-text.iq0m558w'))).send_keys(contatos_filtrados[contador][0])
                sleep(uniform(1, 2))

        # Pula o contato
        except:

            # Clica na flecha para voltar
            WebDriverWait(navegador, 10).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, 'kk3akd72.dmous0d2.fewfhwl7.ajgl1lbb.ltyqj8pj'))).click()
            contador += 1
            sleep(uniform(1, 2))
            pass


# ---------- Variaveis globais ---------- #
navegador = None
contatos_filtrados = []
contatos_cadastrados = []
contatos_novos = []
texto = arquivo = fonte = fazer = resposta_texto = resposta_arquivo = ''
substituir = '()/.-+\n '


# ---------- Pergunta a fonte dos dados ---------- #
print('Por onde será a coleta de dados?\n')
print('(1) - Leilões')
print('(2) - Banco de Dados\n')
while fonte not in ['1', '2']:
    fonte = input('Resposta: ').strip()
system('cls')


# ---------- Pergunta o que fará com os dados ---------- #
print('O que você quer fazer com os dados?\n')
print('(1) - Cadastrar')
print('(2) - Enviar Mensagem')
print('(3) - Cadastrar e Enviar Mensagem\n')
while fazer not in ['1', '2', '3']:
    fazer = input('Resposta: ').strip()
system('cls')


# ---------- Verifica se vai precisar de mensagem ---------- #
if fazer in ['2', '3']:

    # ---------- Pega o texto ---------- #
    while True:
        while resposta_texto not in ['s', 'n', 'sim', 'nao', 'não']:
            resposta_texto = input('Enviar texto: ').lower().strip()
            system('cls')
        if resposta_texto in ['s', 'sim']:
            while True:
                texto = input('Qual é o texto:\n').replace('  ', '\n').strip()
                print('\n------------------------------\n')
                print('O texto está correto?')
                print(f'{texto}')
                print('\n------------------------------\n')
                resposta_texto = input('Resposta: ').lower().strip()
                while resposta_texto not in ['s', 'n', 'sim', 'nao', 'não']:
                    resposta_texto = input('Resposta: ').lower().strip()
                if resposta_texto in ['s', 'sim']:
                    system('cls')
                    break
                system('cls')
        break

    # ---------- Pega o arquivo ---------- #
    while True:
        while resposta_arquivo not in ['s', 'n', 'sim', 'nao', 'não']:
            resposta_arquivo = input('Enviar arquivo: ').lower().strip()
            system('cls')
        if resposta_arquivo in ['s', 'sim']:
            while True:
                arquivo = input('Nome do arquivo:\n').strip()
                print('\n------------------------------\n')
                print('O nome do arquivo está correto?')
                print(f'{arquivo}')
                print('\n------------------------------\n')
                resposta_arquivo = input('Resposta: ').lower().strip()
                while resposta_arquivo not in ['s', 'n', 'sim', 'nao', 'não']:
                    resposta_arquivo = input('Resposta: ').lower().strip()
                if resposta_arquivo in ['s', 'sim']:
                    system('cls')
                    break
                system('cls')
        break


# Sinaliza que o programa começou a executar
print('------------------------------\n')
print('Executando...')
print('\n------------------------------\n')


# Quando vai apenas cadastrar os contatos
if fonte == '1' and fazer == '1':
    filtrar_leiloes()
    inicializar_navegador()
    cadastrar_contatos()

elif fonte == '2' and fazer == '1':
    filtrar_banco_de_dados()
    inicializar_navegador()
    cadastrar_contatos()

# Quando vai apenas enviar a mensagem
elif fonte == '1' and fazer == '2' and texto or arquivo:
    filtrar_leiloes()
    inicializar_navegador()
    enviar_mensagem()

elif fonte == '2' and fazer == '2' and texto or arquivo:
    filtrar_banco_de_dados()
    inicializar_navegador()
    enviar_mensagem()

# Quando vai cadastrar e enviar mensagem ao mesmo tempo
elif fonte == '1' and fazer == '3' and texto or arquivo:
    filtrar_leiloes()
    inicializar_navegador()
    cadastrar_contatos()
    enviar_mensagem()

elif fonte == '2' and fazer == '3' and texto or arquivo:
    filtrar_banco_de_dados()
    inicializar_navegador()
    cadastrar_contatos()
    enviar_mensagem()

else:
    print('Nenhum contato para cadastrar ou não existe texto/arquivo para enviar!')
