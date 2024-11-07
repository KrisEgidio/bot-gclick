from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc


def get_driver(headless=False):
    chrome_options = uc.ChromeOptions()

    # Modo headless para rodar sem UI, o que aumenta a velocidade
    if headless:
        chrome_options.add_argument("--headless")

    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--user-agent=UAstring")

    chrome_prefs = {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "intl.accept_languages": "pt-BR"  # Definir idioma do navegador
    }

    chrome_options.add_experimental_option("prefs", chrome_prefs)
    driver = uc.Chrome(options=chrome_options)

    # Maximizar a janela se não estiver rodando em modo headless
    if not headless:
        driver.maximize_window()

    return driver
