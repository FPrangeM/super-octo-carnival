from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import pyautogui
import pandas as pd

import webautomator as wa



from copy_to_clipboard import main_copiar_imagem
main_copiar_imagem()


coluna_aluno= 'Aluno'
coluna_nome= 'Responsável'
coluna_telefone= 'Telefone'

df = pd.read_excel(r'C:\Users\Prange\Downloads\Ref.xlsx',sheet_name='Consolidado')

df = df[[coluna_aluno,coluna_nome,coluna_telefone]]
df = df.rename(columns={
    coluna_aluno: 'aluno',
    coluna_nome: 'responsavel',
    coluna_telefone: 'telefone'
})



import os


pasta_raiz = fr'C:/Users/{os.getlogin()}/AppData/Local/Google/Chrome/User Data'
    
def find_whats_profile(pasta_raiz):

    profiles = [file for file in os.listdir(pasta_raiz) if 'Profile ' in file]

    for profile in profiles:
        folder = os.path.join(pasta_raiz,profile,'IndexedDB')
        
        if 'https_web.whatsapp.com_0.indexeddb.leveldb' in os.listdir(folder):
            return profile


whats_profile = find_whats_profile(pasta_raiz)

chrome_options_dict = {
    'user-data-dir': pasta_raiz,
    'profile-directory': whats_profile
}



saa = wa.WebAutomator(driver='chrome',options_dict=chrome_options_dict)

url = 'https://web.whatsapp.com/'
saa.driver.get(url)


for id,row in df.iterrows():

    aluno = row['aluno']
    responsavel = row['responsavel']
    numero = row['telefone']

    mensagem = f'Olá {responsavel}, esta mensAgem é para avisar que o aluno {aluno} não vem comparecendo com frequencia na escola'

    saa.click_wait('//span[@data-icon="new-chat-outline"]')
    saa.sendkey_wait('//div[@aria-label="Pesquisar nome ou número"]',numero)

    result_block = saa.wait_element('//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/div/div[2]')
    result_text = result_block.find_element(By.XPATH,'./div[1]').text

    cond_1 = 'CONTATOS NO WHATSAPP' in result_text
    cond_2 = 'NÃO ESTÁ NA SUA LISTA DE CONTATOS' in result_text
    cond_3 = 'Nenhum resultado encontrado' in result_text

    if cond_1 or cond_2:
        if cond_1 :
            saa.click_wait('//div[@tabindex="-1"]/div/div[2]')
        elif cond_2 :
            saa.click_wait('//*[@id="pane-side"]/div[1]/div/div/div[2]/div/div')    

        message_block = saa.wait_element('//div[@aria-placeholder="Digite uma mensagem"]')
        message_block.send_keys(mensagem)
    # saa.click_wait('//span[@data-icon="send"]')

    elif cond_3 :
        print('Contato não encontrado')
    pass



with open('teste.txt','r',encoding='utf-8') as file:
    text = file.read()

print(text.format(
    nome= 'Fernando',
    cidade = 'Campinas'
))

