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

fatura = navegador.find_element("link text", "Faturas")

fatura.click()


time.sleep(5)
