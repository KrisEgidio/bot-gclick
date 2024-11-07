import time

from src.pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from src.utils.logger import Logger
from bs4 import BeautifulSoup
import pandas as pd

class Clients(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = Logger()
        self.driver = driver
        self.dataframe_clients = pd.DataFrame()

        self.url = 'https://appp.gclick.com.br/relatorios/clientes'
        self.insert_filters = (By.XPATH, '//button//span[contains(text(), "Inserir Filtros")]')
        self.input_search = (By.XPATH, '//input[@placeholder="Pesquisar"]')
        self.checkbox_groups = (By.XPATH, '//label[contains(text(), "Grupos")]')
        self.select_groups = (By.XPATH, '//app-input-autocomplete[@endpoint="grupos"]//input')
        self.option_mei = (By.XPATH, '//mat-option//span//span//b[contains(text(), "MEI")]')
        self.apply_filters = (By.XPATH, '//button//span[contains(text(), "Aplicar Filtros")]')
        self.select_status = (By.XPATH, '//div//span[contains(text(), "Status do cliente")]/following-sibling::mat-form-field')
        self.option_active = (By.XPATH, '//mat-option//span[contains(text(), "Ativo")]')
        self.total_itens = (By.XPATH, '//div[@class="mat-mdc-paginator-range-label"]')
        self.select_itens = (By.XPATH, '//div[contains(text(), "Itens por página")]/following-sibling::mat-form-field')
        self.option_1000 = (By.XPATH, '//mat-option//span[contains(text(), "1000")]')
        self.next_page = (By.XPATH, '//button[@aria-label="Próxima página"]')
        self.loading = (By.XPATH, '//img[@alt="Carregando"]')
        self.body = (By.TAG_NAME, 'body')
        self.table = (By.TAG_NAME, 'table')

    def get_clients(self):
        try:
            self.webdriver.get(self.url)

            self.wait_loading_disappear()
            self.wait_presence_element(10, self.table)

            self.wait_presence_element(20, self.insert_filters).click()
            self.wait_presence_element(10, self.input_search).send_keys('Grupos')
            self.wait_presence_element(20, self.checkbox_groups).click()

            # Clicar fora
            self.find_element(self.body).click()

            self.wait_presence_element(20, self.select_groups).click()
            self.wait_presence_element(10, self.select_groups).send_keys('MEI')
            self.wait_presence_element(20, self.option_mei).click()

            # Clicar fora
            self.find_element(self.body).click()

            self.wait_presence_element(20, self.select_status).click()
            self.wait_presence_element(20, self.option_active).click()


            self.wait_presence_element(20, self.apply_filters).click()

            self.wait_loading_disappear()
            self.wait_presence_element(10, self.table)

            max_attempts = 5
            total_itens = 0

            for attempt in range(max_attempts):
                try:
                    # Espera de 2 segundos antes de cada tentativa
                    time.sleep(2)

                    # Tenta obter o elemento e processar o texto
                    total_itens = self.wait_visible_element(20, self.total_itens).text
                    total_itens = total_itens.split('de')[1].strip()
                    total_itens = int(total_itens)

                    # Se tudo der certo, sai do loop
                    break
                except Exception as e:
                    print(f"Tentativa {attempt + 1} falhou: {e}")
                    if attempt == max_attempts - 1:
                        self.logger.error(f"Número máximo de tentativas atingido. Verifique o erro: {str(e)}")
                        raise  # Lança a exceção se for a última tentativa

            if total_itens == 0:
                return self.dataframe_clients

            self.wait_visible_element(20, self.select_itens).click()
            option_element = self.wait_presence_element(20, self.option_1000)
            self.webdriver.execute_script('arguments[0].click();', option_element)

            self.wait_loading_disappear()

            self.extract_clients_from_table()

            return self.dataframe_clients

        except NoSuchElementException as e:
            self.logger.error(f"Clientes - Erro ao localizar um elemento: {str(e)}")
            raise

        except TimeoutException as e:
            self.logger.error(f"Clientes - Tempo limite atingido ao esperar por um elemento: {str(e)}")
            raise

        except Exception as e:
            self.logger.error(f"Clientes - Erro inesperado: {str(e)}")
            raise

    def wait_loading_disappear(self):
        try:
            self.wait_invisibility_of_element(60, self.loading)
        except Exception as e:
            pass

    def extract_clients_from_table(self):
        try:
            all_rows = []
            self.wait_presence_element(10, self.table)

            while True:
                data = []
                headers, data = self.extract_data()
                all_rows.extend(data)

                try:
                    self.wait_clickable_element(2, self.next_page)
                except:
                    break

            self.dataframe_clients = pd.DataFrame(all_rows, columns=headers)

        except Exception as e:
            self.logger.error(f"Extrair dados - Erro inesperado: {str(e)}")
            raise

    def extract_data(self):
        try:
            soup = BeautifulSoup(self.webdriver.page_source, 'html.parser')
            tables = soup.find_all('table')
            headers = ['cnpj', 'name']

            table = tables[0] if tables else None

            rows = table.findAll('tr')[1:]

            data = []

            for row in rows:
                columns = row.findAll('td')
                row_data = []

                cnpj = columns[2].text.strip()
                name = columns[3].text.strip()

                row_data.append(cnpj)
                row_data.append(name)

                data.append(row_data)

            return headers, data
        except Exception as e:
            self.logger.error(f"Extrair dados - Erro inesperado: {str(e)}")
            raise


