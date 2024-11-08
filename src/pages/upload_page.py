import time

from src.pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from src.utils.logger import Logger
import os
import pyautogui

class UploadPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = Logger()
        self.driver = driver
        #self.directory_path = os.path.join(os.getcwd(), "output")
        self.directory_path = "C:\\Users\\Kris\\Downloads\\teste"
        self.file_names = []

        self.url = 'https://appp.gclick.com.br/documentos/upload'
        self.upload_icon = (By.XPATH, '//i/following-sibling::b[contains(text(), "Upload")]')


    def upload_files(self):
        try:
            self.wait_loading_disappear()
            self.webdriver.get(self.url)
            self.wait_loading_disappear()
            self.wait_presence_element(10, self.upload_icon).click()
            self.get_file_names()
            self.select_files()
            self.wait_loading_disappear()

        except NoSuchElementException as e:
            self.logger.error(f"Upload - Erro ao localizar um elemento: {str(e)}")
            raise

        except TimeoutException as e:
            self.logger.error(f"Upload - Tempo limite atingido ao esperar por um elemento: {str(e)}")
            raise

        except Exception as e:
            self.logger.error(f"Upload - Erro inesperado: {str(e)}")
            raise


    def get_file_names(self):
        try:
            if os.path.isdir(self.directory_path):
                for item in os.listdir(self.directory_path):
                    if os.path.isfile(os.path.join(self.directory_path, item)) and item.lower().endswith('.pdf'):
                        self.file_names.append(item)
            else:
                self.logger.error(f"O diretório {self.directory_path} não existe.")
                raise FileNotFoundError(f"O diretório {self.directory_path} não existe.")

        except Exception as e:
            self.logger.error(f"Erro ao obter nomes de arquivos: {e}")
            raise


    def select_files(self):
        try:
            formatted_files = ' '.join([f'"{file}"' for file in self.file_names])

            time.sleep(3)

            pyautogui.write(self.directory_path)
            pyautogui.press('enter')

            time.sleep(2)

            pyautogui.write(formatted_files)
            pyautogui.press('enter')

            print(formatted_files)


        except Exception as e:
            self.logger.error(f"Erro ao formatar nomes de arquivos para upload: {e}")
            raise

