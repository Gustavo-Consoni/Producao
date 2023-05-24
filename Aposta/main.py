from functions import *

# ----- Informações de Login ----- #
while True:
    username = input('Usuário: ').strip()
    system('cls')
    password = input('Senha: ').strip()
    system('cls')
    print('\n------------------------------\n')
    print('As informações estão corretas?\n')
    print(f'Usuário: {username}')
    print(f'Senha: {password}')
    print('\n------------------------------\n')
    answer = input('Resposta: ').lower().strip()
    while answer not in ['s', 'n', 'sim', 'nao', 'não']:
        answer = input('Resposta: ').lower().strip()
    system('cls')
    if answer in ['s', 'sim']:
        break


# ----- Variáveis ----- #
bloco1 = bloco2 = bloco3 = index = afk = aposta = 0
gale = 3
limite = 6
selecionadas = ['bet365 Roulette', 'bet365 Dutch Roulette', 'Ruleta Latinoamérica bet365',
                'Roleta Brasileira bet365', 'Roulette', 'Hindi Roulette',
                'Greek Roulette', 'Turkish Roulette', 'Roleta Brasileira',
                'Prestige Roulette', 'Nederlandstalige Roulette', 'Deutsches Roulette',
                'UK Roulette', 'Bucharest Roulette', 'Roulette Italiana',
                'Arabic Roulette']


# ----- Navegador ----- #
options = ChromeOptions()
options.add_argument('--mute-audio')
browser = Chrome(options=options)
browser.maximize_window()
browser.get('https://livecasino.bet365.com/Play/bet365Roulette')
sleep(1)


# ----- Preenche o campo de USUARIO ----- #
username_field = wdw(browser, 10).until(ec.presence_of_element_located((By.ID, 'txtUsername')))
username_field.clear()
sleep(1)
username_field.send_keys(username)
sleep(1)


# ----- Preenche o campo de SENHA ----- #
password_field = wdw(browser, 10).until(ec.presence_of_element_located((By.ID, 'txtPassword')))
password_field.clear()
sleep(1)
password_field.send_keys(password)
sleep(1)


# ----- Clica no botão de FAZER LOGIN ----- #
wdw(browser, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, 'modal__button'))).click()
sleep(15)


# ----- Move até a tela de jogos ----- #
browser.execute_script('window.scrollBy(0, 50)')
sleep(1)


# ----- Realiza recursividade nos iframes ----- #
iframe = browser
verificar_iframes(iframe, 'sidebar-buttons__menu')
sleep(1)


# ----- Clica no Hall de Entrada ----- #
wdw(iframe, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, 'main-menu__item'))).click()
sleep(1)


# ----- Clica na aba de roletas ----- #
wdw(iframe, 10).until(ec.element_to_be_clickable((By.XPATH, 'html/body/div[1]/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/div/div[2]'))).click()
sleep(1)


# ----- Loop para analisar as roletas ----- #
while True:

    # ----- Pega todas as roletas ----- #
    roletas = execute_finds(iframe, 'lobby-tables__item', By.CLASS_NAME)

    # ----- Filtra as roletas ----- #
    roletas = [roleta for roleta in roletas if execute_find(roleta, 'lobby-table__name-container', By.CLASS_NAME).text in selecionadas]

    # ----- Reseta o tempo do AFK ----- #
    if afk >= 30:

        try:

            # ----- Pega uma roleta aleatoriamente ----- #
            roleta = choice(roletas)

            # ----- Move até a roleta ----- #
            ActionChains(browser).scroll_to_element(roleta).perform()
            sleep(0.5)

            # ----- Clica na roleta ----- #
            wdw(browser, 10).until(ec.element_to_be_clickable(roleta)).click()
            sleep(0.5)

        except:

            continue

        # ----- Clica no Menu ----- #
        wdw(browser, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, 'sidebar-buttons__menu'))).click()
        sleep(0.5)

        # ----- Clica no Hall de Entrada ----- #
        wdw(browser, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, 'main-menu__item'))).click()
        sleep(0.5)

        # ----- Clica na aba de roletas ----- #
        wdw(browser, 10).until(ec.element_to_be_clickable((By.XPATH, 'html/body/div[1]/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/div/div[2]'))).click()
        sleep(0.5)

        # ----- Reseta o AFK ----- #
        afk = 0

    # ----- Seleciona cada roleta ----- #
    for roleta in roletas:

        # ----- Pega os numeros ----- #
        try:
            numeros = roleta.find_elements(By.CLASS_NAME, 'roulette-history-item__value-text--siwxW')
        except:
            continue

        # ----- Verifica quais blocos cairam ----- #
        while index != limite:
            if 1 <= int(numeros[index].text) <= 12:
                bloco1 += 1
            elif 13 <= int(numeros[index].text) <= 24:
                bloco2 += 1
            elif 25 <= int(numeros[index].text) <= 36:
                bloco3 += 1
            elif int(numeros[index].text) == 0:
                if limite < 10:
                    limite += 1
            index += 1

        # ----- Verifica se saiu 6 vezes o primeiro bloco ----- #
        if bloco1 == 6:

            # ----- Pega o ultimo numero que saiu ----- #
            comparador = numeros[0].text

            # ----- Move até a roleta ----- #
            execute_scroll(iframe, roleta)

            # ----- Clica na roleta ----- #
            execute_click(iframe, roleta)

            # ----- Seleciona a primeira ficha ----- #
            execute_click(iframe, 'arrow-slider__element', By.CLASS_NAME)

            try:

                # ----- Clica no segundo bloco ----- #
                ActionChains(iframe).move_to_element(wdw(iframe, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, 'roulette-table-cell_side-second-dozen')))).click().perform()

                # ----- Clica no terceiro bloco ----- #
                ActionChains(iframe).move_to_element(wdw(iframe, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, 'roulette-table-cell_side-third-dozen')))).click().perform()

            except:

                # ----- Clica no Menu ----- #
                wdw(iframe, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, 'sidebar-buttons__menu'))).click()
                sleep(0.5)

                # ----- Clica no Hall de Entrada ----- #
                wdw(iframe, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, 'main-menu__item'))).click()
                sleep(0.5)

                # ----- Clica na aba de roletas ----- #
                wdw(iframe, 10).until(ec.element_to_be_clickable((By.XPATH, 'html/body/div[1]/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/div/div[2]'))).click()
                sleep(0.5)

                break

            # ----- Loop pro marting gale ----- #
            while True:

                # ----- Pega o ultimo numero que saiu ----- #
                ultimo_numero = wdw(iframe, 10).until(ec.presence_of_element_located((By.CLASS_NAME, 'roulette-history-item__value-textsiwxWvFlm3ohr_UMS23f')))

                # ----- Verifica se saiu algum numero ----- #
                if comparador != ultimo_numero.text and ultimo_numero.text != '':

                    comparador = ultimo_numero.text

                    if gale >= 9:
                        gale = 3
                        aposta = 1
                        sleep(2)
                        break

                    if 1 <= int(comparador) <= 12 or int(comparador) == 0:

                        for contadora in range(gale):

                            # ----- Clica no segundo bloco ----- #
                            ActionChains(iframe).move_to_element(wdw(iframe, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, 'roulette-table-cell_side-second-dozen')))).click().perform()

                            # ----- Clica no terceiro bloco ----- #
                            ActionChains(iframe).move_to_element(wdw(iframe, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, 'roulette-table-cell_side-third-dozen')))).click().perform()

                        gale += 6

                    elif 13 <= int(comparador) <= 36:
                        gale = 3
                        aposta = 1
                        sleep(2)
                        break

        # ----- Verifica se saiu 6 vezes o segundo bloco ----- #
        elif bloco2 == 6:

            # ----- Pega o ultimo numero que saiu ----- #
            comparador = numeros[0].text

            # ----- Move até a roleta ----- #
            execute_scroll(iframe, roleta)

            # ----- Clica na roleta ----- #
            execute_click(iframe, roleta)

            # ----- Seleciona a primeira ficha ----- #
            execute_click(iframe, 'arrow-slider__element', By.CLASS_NAME)

            try:

                # ----- Clica no primeiro bloco ----- #
                ActionChains(iframe).move_to_element(wdw(iframe, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, 'roulette-table-cell_side-first-dozen')))).click().perform()

                # ----- Clica no terceiro bloco ----- #
                ActionChains(iframe).move_to_element(wdw(iframe, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, 'roulette-table-cell_side-third-dozen')))).click().perform()

            except:

                # ----- Clica no Menu ----- #
                wdw(iframe, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, 'sidebar-buttons__menu'))).click()
                sleep(0.5)

                # ----- Clica no Hall de Entrada ----- #
                wdw(iframe, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, 'main-menu__item'))).click()
                sleep(0.5)

                # ----- Clica na aba de roletas ----- #
                wdw(iframe, 10).until(ec.element_to_be_clickable((By.XPATH, 'html/body/div[1]/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/div/div[2]'))).click()
                sleep(0.5)

                break

            # ----- Loop pro marting gale ----- #
            while True:

                # ----- Pega o ultimo numero que saiu ----- #
                ultimo_numero = wdw(iframe, 10).until(ec.presence_of_element_located((By.CLASS_NAME, 'roulette-history-item__value-textsiwxWvFlm3ohr_UMS23f')))

                # ----- Verifica se saiu algum numero ----- #
                if comparador != ultimo_numero.text and ultimo_numero.text != '':

                    comparador = ultimo_numero.text

                    if gale >= 9:
                        gale = 3
                        aposta = 1
                        sleep(2)
                        break

                    if 13 <= int(comparador) <= 24 or int(comparador) == 0:

                        for contadora in range(gale):

                            # ----- Clica no primeiro bloco ----- #
                            ActionChains(iframe).move_to_element(wdw(iframe, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, 'roulette-table-cell_side-first-dozen')))).click().perform()

                            # ----- Clica no terceiro bloco ----- #
                            ActionChains(iframe).move_to_element(wdw(iframe, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, 'roulette-table-cell_side-third-dozen')))).click().perform()

                        gale += 6

                    elif 1 <= int(comparador) <= 12 or 25 <= int(comparador) <= 36:
                        gale = 3
                        aposta = 1
                        sleep(2)
                        break

        # ----- Verifica se saiu 6 vezes o terceiro bloco ----- #
        elif bloco3 == 6:

            # ----- Pega o ultimo numero que saiu ----- #
            comparador = numeros[0].text

            # ----- Move até a roleta ----- #
            execute_scroll(iframe, roleta)

            # ----- Clica na roleta ----- #
            execute_click(iframe, roleta)

            # ----- Seleciona a primeira ficha ----- #
            execute_click(iframe, 'arrow-slider__element', By.CLASS_NAME)

            try:

                # ----- Clica no primeiro bloco ----- #
                ActionChains(iframe).move_to_element(wdw(iframe, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, 'roulette-table-cell_side-first-dozen')))).click().perform()

                # ----- Clica no segundo bloco ----- #
                ActionChains(iframe).move_to_element(wdw(iframe, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, 'roulette-table-cell_side-second-dozen')))).click().perform()

            except:

                # ----- Clica no Menu ----- #
                wdw(iframe, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, 'sidebar-buttons__menu'))).click()
                sleep(0.5)

                # ----- Clica no Hall de Entrada ----- #
                wdw(iframe, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, 'main-menu__item'))).click()
                sleep(0.5)

                # ----- Clica na aba de roletas ----- #
                wdw(iframe, 10).until(ec.element_to_be_clickable((By.XPATH, 'html/body/div[1]/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/div/div[2]'))).click()
                sleep(0.5)

                break

            # ----- Loop pro marting gale ----- #
            while True:

                # ----- Pega o ultimo numero que saiu ----- #
                ultimo_numero = wdw(iframe, 10).until(ec.presence_of_element_located((By.CLASS_NAME, 'roulette-history-item__value-textsiwxWvFlm3ohr_UMS23f')))

                # ----- Verifica se saiu algum numero ----- #
                if comparador != ultimo_numero.text and ultimo_numero.text != '':

                    comparador = ultimo_numero.text

                    if gale >= 9:
                        gale = 3
                        aposta = 1
                        sleep(2)
                        break

                    if 25 <= int(comparador) <= 36 or int(comparador) == 0:

                        for contadora in range(gale):

                            # ----- Clica no primeiro bloco ----- #
                            ActionChains(iframe).move_to_element(wdw(iframe, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, 'roulette-table-cell_side-first-dozen')))).click().perform()

                            # ----- Clica no segundo bloco ----- #
                            ActionChains(iframe).move_to_element(wdw(iframe, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, 'roulette-table-cell_side-second-dozen')))).click().perform()

                        gale += 6

                    elif 1 <= int(comparador) <= 24:
                        gale = 3
                        aposta = 1
                        sleep(2)
                        break

        # ----- Reseta as variaveis ----- #
        bloco1 = bloco2 = bloco3 = index = 0
        limite = 6

        # ----- Realiza o anti-afk ----- #
        if aposta == 1:
            afk = 30
            aposta = 0
            break

    afk += 1
