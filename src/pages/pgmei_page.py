import re
import shutil
import pyautogui
from datetime import datetime
from src.utils.logger import Logger
import unicodedata
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time
import os


class PgemeiPage:
    def __init__(self, driver):
        self.logger = Logger()
        self.driver = driver

    def baixar_boleto_das(self, dicionario_mei):
        try:
            for raw_cnpj, raw_nome in dicionario_mei.items():
                try:
                    pagina_principal = "https://www8.receita.fazenda.gov.br/SimplesNacional/Aplicacoes/ATSPO/pgmei.app/Identificacao"
                    pagina_emissao = "https://www8.receita.fazenda.gov.br/SimplesNacional/Aplicacoes/ATSPO/pgmei.app/emissao"
                    download_dir = os.path.join(os.getcwd(), "output")

                    cnpj = self.remover_pontuacao_cnpj(raw_cnpj)
                    nome = self.formatar_nome(raw_nome)

                    self.driver.get(pagina_principal)

                    if self.pesquisar_cnpj(cnpj, self.driver):
                        self.driver.get(pagina_emissao)

                    self.selecionar_ano_vigente(self.driver, ano_das=None)
                    self.selecionar_mes_vigente(self.driver, mes_das=None)
                    self.gerar_e_imprimir(cnpj, nome, download_dir, self.driver)
                    self.registrar_log(f'Sucesso: Boleto D.A.S. baixado para CNPJ: {cnpj}, Nome: {nome}')
                    #driver.quit()

                except Exception as e:
                    #driver.quit()
                    self.registrar_log(f'Erro ao processar CNPJ: {cnpj}, Nome: {nome} - {str(e)}', 'info')

        except Exception as e:
            #driver.quit()
            print(f"Erro ao carregar informações: {e}")

    def pesquisar_cnpj(self, cnpj, driver):
        try:
            wait = WebDriverWait(driver, 5)
            campo_cnpj = wait.until(EC.element_to_be_clickable((By.ID, "cnpj")))
            campo_cnpj.send_keys(cnpj)
            time.sleep(1)
            botao_continuar = driver.find_element(By.ID, "continuar")

            url_atual = driver.current_url
            driver.execute_script("arguments[0].click();", botao_continuar)

            try:
                # Aguarde até que a URL mude
                WebDriverWait(driver, 10).until(EC.url_changes(url_atual))
                return True

            except TimeoutException:
                try:
                    aviso_container = driver.find_element(By.ID, 'toast-container')
                    aviso = aviso_container.find_element(By.CLASS_NAME, 'toast-error')
                    if "23008 - Contribuinte não optante pelo SIMEI." in aviso.text:
                        raise Exception("Contribuinte não optante pelo SIMEI.")
                except Exception as e:
                    raise Exception(f"Erro ao pesquisar cnpj: {e}")
        except Exception as e:
            raise Exception(f"Erro na função pesquisar_cnpj: {e}")

    def selecionar_ano_vigente(self, driver, ano_das=None):
        wait = WebDriverWait(driver, 10)
        try:
            if ano_das is None:
                ano_das = datetime.now().strftime("%Y")

            dropdown_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-id='anoCalendarioSelect']")))
            dropdown_button.click()

            opcao_ano = wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//ul[@class='dropdown-menu inner']//span[text()='{ano_das}']")))
            opcao_ano.click()
            time.sleep(1)

            botao_ok = driver.find_element(By.XPATH, "//button[contains(@class, 'btn-success') and contains(., 'Ok')]")
            botao_ok.click()
            time.sleep(2)
        except Exception as e:
            raise Exception(f"Erro na função selecionar_ano_vigente: {e}")

    def selecionar_mes_vigente(self, driver, mes_das=None):
        try:
            if mes_das is None:
                mes_das = datetime.now().strftime("%Y%m")
            checkboxes = driver.find_elements(By.CLASS_NAME, 'paSelecionado')

            # Marca o checkbox referente ao mês atual
            for checkbox in checkboxes:
                if checkbox.get_attribute("value") == mes_das:
                    checkbox.click()
                    break
        except Exception as e:
            raise Exception(f'Erro na função selecionar_mes_vigente: {e}')

    def gerar_e_imprimir(self, cnpj, nome, download_dir, driver):
        wait = WebDriverWait(driver, 10)
        try:
            botao_gerar = driver.find_element(By.ID, 'btnEmitirDas')
            driver.execute_script("arguments[0].click();", botao_gerar)

            botao_imprimir = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Imprimir/Visualizar PDF')))
            driver.execute_script("arguments[0].click();", botao_imprimir)
            time.sleep(2)

            self.renomear_pdf(cnpj, nome, download_dir)
        except Exception as e:
            raise Exception(f'Erro na função gerar_e_imprimir: {e}')

    def renomear_pdf(self, cnpj, nome, download_dir):
        try:
            nome_pdf_desejado = f'DAS-PGMEI-{cnpj}.pdf'
            nome_arquivo = os.path.join(download_dir, nome_pdf_desejado)
            pyautogui.write(nome_arquivo)
            time.sleep(2)
            pyautogui.press("enter")

            time.sleep(2)

            arquivos_baixados = [f for f in os.listdir(download_dir) if f.endswith('.pdf')]

            if arquivos_baixados:
                ultimo_arquivo_baixado = max(arquivos_baixados,
                                             key=lambda x: os.path.getctime(os.path.join(download_dir, x)))
                #novo_caminho = os.path.join(download_dir, nome_pdf_desejado)
                #shutil.move(os.path.join(download_dir, ultimo_arquivo_baixado), novo_caminho)
            else:
                raise Exception("Arquivo não encontrado ou não renomeado.")
        except Exception as e:
            raise Exception(f'Erro na função renomear_pdf: {e}')

    def registrar_log(self, mensagem, tipo='error'):
        if tipo == 'error':
            self.logger.error(mensagem)
        else:
            self.logger.info(mensagem)

    def remover_pontuacao_cnpj(self, cnpj):
        cnpj_sem_pontuacao = re.sub(r'\D', '', cnpj)
        return cnpj_sem_pontuacao

    def formatar_nome(self, nome):
        # Remove acentos e caracteres especiais
        nome_sem_acento = unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode('ASCII')
        # Remove qualquer caractere que não seja letra ou espaço
        nome_limpo = re.sub(r'[^A-Z a-z]', '', nome_sem_acento)
        # Converte para caixa alta
        return nome_limpo.upper()