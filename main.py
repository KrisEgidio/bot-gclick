import time

from src.pages.login_page import LoginPage
from src.pages.clients_page import Clients
from src.utils.webdriver import get_driver
from dotenv import load_dotenv
import os


def main():
    load_dotenv()
    driver = get_driver()

    try:
        username = os.getenv('USER')
        password = os.getenv('PASSWORD')
        
        login_page = LoginPage(driver)
        login_page.login(username, password)

        clients_page = Clients(driver)

        time.sleep(5)

        dt_clients = clients_page.get_clients()
        print(dt_clients)


    except Exception as e:
        print(e)
    finally:
        driver.quit()



if __name__ == '__main__':
    main()