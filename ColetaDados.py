from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd


# site que queremos abrir
site = 'https://www.ukclubsport.com/br/futebol/brazilian-serie-a/results/'

# criamos uma máquina do mozzila firefox
maquina = webdriver.Firefox()

# caso a maquina nao tenha sido aberta, o codigo se conecta a minha conta do twilio
# e manda um sms para o meu telefone

maquina.maximize_window()

# dizemos pra máquina qual site queremos acessar
# e aqui a mesma coisa, se não acessar vai me avisar por sms
maquina.get(site)

# esperamos o site abrir
WebDriverWait(maquina, timeout=2)

# ----------------------------------------------------------------------------------------------#

# 2 vezes a mesma atividade pois o site pode não responder

# buscamos o botão com as opções dos anos referentes aos dados disponíveis
maquina.find_element(
    By.CSS_SELECTOR, 'div[class="select d-none d-md-block"]').click()

WebDriverWait(maquina, timeout=2)

# buscamos o botão com as opções dos anos referentes aos dados disponíveis
maquina.find_element(
    By.CSS_SELECTOR, 'div[class="select d-none d-md-block"]').click()

WebDriverWait(maquina, timeout=2)

# selecionamos a opção do ano em que temos todos os dados, o ano de 2024
maquina.find_element(By.XPATH, "//div[contains(text(), '2024')]").click()

# ----------------------------------------------------------------------------------------------#

WebDriverWait(maquina, timeout=10)

maquina.find_element(By.CLASS_NAME, "cookie__image").click()

WebDriverWait(maquina, timeout=4)


while (maquina.find_element(By.CSS_SELECTOR, "button.btn.btn-default.btn-outline.btn-xs.btn--full")):
    try:
        botao = maquina.find_element(
            By.CSS_SELECTOR, "button.btn.btn-default.btn-outline.btn-xs.btn--full")
        maquina.execute_script("arguments[0].scrollIntoView();", botao)
        maquina.execute_script("arguments[0].click();", botao)
    except:
        print("Ignorando o erro")
        break

dataframe = pd.DataFrame()

lista = maquina.find_elements(By.CLASS_NAME, 'time-table__match')

x = 1

jogo = []
time1 = []
time2 = []
vencedor = []
gol_time1 = []
gol_time2 = []
odd_vitoria_time1 = []
odd_empate = []
odd_vitoria_time2 = []
odd_vencedor = []
maior_odd = []

# print(item.find_elements(By.CLASS_NAME, 'time-table__team-title-text'))

for item in lista:
    
    jogo.append(x)
    times = item.find_elements(By.CLASS_NAME, 'time-table__team-title-text')
    WebDriverWait(maquina, timeout=5)
    time1.append(times[0].text)
    time2.append(times[1].text)
    WebDriverWait(maquina, timeout=5)

    try:
        vencedor.append(item.find_element(By.CSS_SELECTOR, 'div.time-table__team.time-table__team--winner div.time-table__team-title span.time-table__team-title-text').text)
    except:
        vencedor.append('Empate')

    WebDriverWait(maquina, timeout=5)
    gols = item.find_elements(By.CSS_SELECTOR, 'div.score-item__team div')
    WebDriverWait(maquina, timeout=5)
    gol_time1.append(gols[0].text)
    gol_time2.append(gols[1].text)
    WebDriverWait(maquina, timeout=5)
    odds = item.find_elements(By.CLASS_NAME, 'ratio__count')
    WebDriverWait(maquina, timeout=5)
    odd1 = float(odds[0].text)
    odd2 = float(odds[1].text)
    odd3 = float(odds[2].text)
    WebDriverWait(maquina, timeout=5)
    maior = max(odd1, odd2, odd3)
    WebDriverWait(maquina, timeout=5)
    odd_vitoria_time1.append(odd1)
    odd_empate.append(odd2)
    odd_vitoria_time2.append(odd3)
    WebDriverWait(maquina, timeout=5)
    maior_odd.append(maior)
    WebDriverWait(maquina, timeout=5)
    odd4 = float(item.find_element(By.CSS_SELECTOR, "a.ratio.ratio--active.ratio--finished div.ratio__wrap div.ratio__count").text)
    WebDriverWait(maquina, timeout=5)
    odd_vencedor.append(odd4)
    
    print(F'{x} do laço deu certo')
    x+=1 

    WebDriverWait(maquina, timeout=5)


dataframe['Jogo'] = jogo
dataframe['Time 1'] = time1
dataframe['Time 2'] = time2
dataframe['Time Vencedor'] = vencedor
dataframe['Gol Time 1'] = gol_time1
dataframe['Gol Time 2'] = gol_time2
dataframe['Odd Vitoria Time 1'] = odd_vitoria_time1
dataframe['Odd Vitoria Time 2'] = odd_vitoria_time2
dataframe['Odd Empate'] = odd_empate
dataframe['Odd Vencedor'] = odd_vencedor
dataframe['Maior Odd'] = maior_odd


# precisamos imprimir so pra ver se foi tudo correto
print(dataframe)


dataframe.to_csv("Brasileirao2024.csv", index=False)


# pedimos para a maquina aguardar um tempo curto, e fechamos para partir para a próxima coleta de dados
WebDriverWait(maquina, timeout=4)

maquina.close()
