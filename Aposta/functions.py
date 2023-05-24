from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from undetected_chromedriver import Chrome, ChromeOptions
from time import sleep
from random import choice
from os import system


def execute_click(driver, element, type=''):
    while True:
        try:
            if type:
                driver.find_element(type, element).click()
            else:
                element.click()
            break
        except:
            print(f'Erro ao clicar no elemento: {element}')


def execute_find(driver, element, type):
    while True:
        try:
            return driver.find_element(type, element)
        except:
            print(f'Erro ao encontrar o elemento: {element}')


def execute_finds(driver, element, type):
    while True:
        try:
            return driver.find_elements(type, element)
        except:
            print(f'Erro ao encontrar os elementos: {element}')


def execute_scroll(driver, element):
    while True:
        try:
            ActionChains(driver).scroll_to_element(element).perform()
            break
        except:
            print(f'Erro ao scrollar pro elemento: {element}')


def execute_move(driver, element):
    while True:
        try:
            ActionChains(driver).move_to_element(element).perform()
            break
        except:
            print(f'Erro ao mover pro elemento: {element}')


def procurar_elemento(driver, element):

    try:
        wdw(driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, element)))
        return True
    except:
        return False


def verificar_iframes(driver, element):

    if procurar_elemento(driver, element):
        wdw(driver, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, element))).click()
        return True

    iframes = wdw(driver, 10).until(ec.presence_of_all_elements_located((By.TAG_NAME, 'iframe')))
    for iframe in iframes:
        wdw(driver, 10).until(ec.frame_to_be_available_and_switch_to_it(iframe))
        if verificar_iframes(driver, element):
            return True
        driver.switch_to.parent_frame()

    return False
