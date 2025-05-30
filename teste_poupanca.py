from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select  # Importando Select para lidar com dropdown

navegador = webdriver.Chrome()
navegador.maximize_window()
navegador.get("http://127.0.0.1:8000")

time.sleep(2)

botao_login = navegador.find_element("link text", "Entrar")
botao_login.click()

time.sleep(2)

username = navegador.find_element("id", "id_username")
username.send_keys("Pedro")

time.sleep(2)

senha = navegador.find_element("id", "id_password")
senha.send_keys("123")

time.sleep(2) 

entrar = navegador.find_element(By.XPATH, "//button[text()='Entrar']")
entrar.click()

time.sleep(2)

invest = navegador.find_element("link text", "Novo Investimento")

invest.click()



time.sleep(2)

valor_invest = navegador.find_element("id", "id_valor")

valor_invest.send_keys("100,00")



time.sleep(2)

confirm_invest = navegador.find_element(By.XPATH, "//button[text()='Confirmar Investimento']")

confirm_invest.click()

time.sleep(5)