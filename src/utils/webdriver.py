import os
import undetected_chromedriver as uc


def get_driver(headless=False):
    chrome_options = uc.ChromeOptions()
    download_directory = os.path.join(os.getcwd(), "output")

    # Modo headless para rodar sem UI, o que aumenta a velocidade
    if headless:
        chrome_options.add_argument("--headless")

    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--user-agent=Default")

    chrome_prefs = {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "intl.accept_languages": "pt-BR",  # Definir idioma do navegador
        "download.default_directory": download_directory,
        "plugins.always_open_pdf_externally": False,
    }

    chrome_options.add_experimental_option("prefs", chrome_prefs)
    driver = uc.Chrome(options=chrome_options)

    # Maximizar a janela se não estiver rodando em modo headless
    if not headless:
        driver.maximize_window()

    return driver
