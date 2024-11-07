from src.pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from src.utils.logger import Logger

class LoginPage(BasePage):
    
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = Logger()
        self.driver = driver
        self.url = "https://appp.gclick.com.br/"
        self.username_locator = (By.XPATH, '//input[@formcontrolname="username"]')
        self.password_locator = (By.XPATH, '//input[@formcontrolname="password"]')
        self.login_button_locator = (By.XPATH, '//button[@type="submit"]')
        

    def login(self, username, password):
        try:
            self.driver.get(self.url)
            self.wait_visible_element(10, self.username_locator).send_keys(username)
            self.wait_visible_element(10, self.password_locator).send_keys(password)
            self.wait_visible_element(10, self.login_button_locator).click()

            self.logger.info("Login efetuado com sucesso!")

        except NoSuchElementException as e:
            self.logger.error(f"Login - Erro ao localizar um elemento: {str(e)}")
            raise

        except TimeoutException as e:
            self.logger.error(f"Login - Tempo limite atingido ao esperar por um elemento: {str(e)}")
            raise

        except Exception as e:
            self.logger.error(f"Login - Erro inesperado ao realizar login: {str(e)}")
            raise
        
    def logout(self):
        pass
       