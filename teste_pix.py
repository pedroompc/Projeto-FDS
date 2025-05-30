from selenium  import webdriver
import time
from selenium.webdriver.common.by import By

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

botao_cadastrar = navegador.find_element(By.XPATH, "//button[text()='Entrar']")

botao_cadastrar.click()

time.sleep(3)

novo_pix = navegador.find_element("link text", "Nova Transferência")

novo_pix.click()



time.sleep(2)

user = navegador.find_element("id", "id_destinatario")

user.send_keys("Lucas")



time.sleep(2)

valor = navegador.find_element("id", "id_valor")
valor.send_keys("50,00")




time.sleep(2)

desc = navegador.find_element("id", "id_descricao")
desc.send_keys("pagamento da fatura")



time.sleep(2)

novo_pix = navegador.find_element(By.XPATH, "//button[text()='Confirmar Transferência']")

novo_pix.click()



time.sleep(2)