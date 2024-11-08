import time

from src.pages.login_page import LoginPage
from src.pages.clients_page import ClientPage
from src.pages.upload_page import UploadPage
from src.utils.webdriver import get_driver
from src.pages.pgmei_page import PgemeiPage
from dotenv import load_dotenv
from src.utils.file import delete_all_files
import os


def main():
    load_dotenv()
    driver = get_driver()

    try:
        delete_all_files()
        username = os.getenv('USER')
        password = os.getenv('PASSWORD')
        
        login_page = LoginPage(driver)
        login_page.login(username, password)

        clients_page = ClientPage(driver)

        time.sleep(5)

        dict_clients = clients_page.get_clients()
        print(dict_clients)

        pgmei_page = PgemeiPage(driver)
        pgmei_page.baixar_boleto_das(dict_clients)

        upload_page = UploadPage(driver)
        upload_page.upload_files()

    except Exception as e:
        print(e)
    finally:
        driver.quit()



if __name__ == '__main__':
    main()