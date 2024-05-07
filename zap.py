from bs4 import BeautifulSoup
import re
from urllib.request import Request, urlopen
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import math
import pandas as pd
import time
# from selenium import webdriver

# Crie um objeto do navegador
# driver = webdriver.Chrome()

bairros = []
cidades = []
aluguel = []
periodos = []
cond = []
iptu = []
quartos = []
area = []
banheiros = []
# vagas =[]


headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}

link = 'https://www.zapimoveis.com.br/aluguel/apartamentos/es+vitoria/?__ab=exp-aa-test:control,webp-rlt:webp,rp-imob:control&transacao=aluguel&onde=,Esp%C3%ADrito%20Santo,Vit%C3%B3ria,,,,,city,BR%3EEspirito%20Santo%3ENULL%3EVitoria,-20.319664,-40.338475,;,Esp%C3%ADrito%20Santo,Vila%20Velha,,,,,city,BR%3EEspirito%20Santo%3ENULL%3EVila%20Velha,-20.351808,-40.30797,&tipos=apartamento_residencial&pagina=1'


requisicao = Request(link,headers = headers)

try:
    response = urlopen(requisicao)
    html = response.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
except HTTPError as e:
    print(e.status(), e.reason())
except URLError as e:
    print(e.reason()) 

locations = soup.find_all('h2',class_='card__address')

anuncios = len(locations)
print(anuncios)

results = soup.find('div',class_='result-wrapper__title')
n_results  = int(re.findall(r'\d+',results.h1.get_text())[0])
print(n_results)

n_pages = math.ceil(n_results/anuncios)


for i in range(1,11):
  link = f'https://www.zapimoveis.com.br/aluguel/apartamentos/es+vitoria/?__ab=exp-aa-test:control,webp-rlt:webp,rp-imob:control&transacao=aluguel&onde=,Esp%C3%ADrito%20Santo,Vit%C3%B3ria,,,,,city,BR%3EEspirito%20Santo%3ENULL%3EVitoria,-20.319664,-40.338475,;,Esp%C3%ADrito%20Santo,Vila%20Velha,,,,,city,BR%3EEspirito%20Santo%3ENULL%3EVila%20Velha,-20.351808,-40.30797,&tipos=apartamento_residencial&pagina={i}'


  requisicao = Request(link,headers = headers)

  try:
      response = urlopen(requisicao)
      html = response.read().decode('utf-8')
      soup = BeautifulSoup(html, 'html.parser')
  except HTTPError as e:
      print(e.status(), e.reason())
  except URLError as e:
      print(e.reason()) 
      
      
  locations = soup.find_all('h2',class_='card__address')
  streets = soup.find_all('p',class_='card__street')
  amenity = soup.find_all('p',class_='card__amenity')

  prices = soup.find_all('div',class_='listing-price')
  #### LOCALIZAÇÃO
  for location in locations:
    value = location.get_text().split(',')
    
    
    bairros.append(value[0].strip())
    cidades.append(value[1].strip())
    
    
  #### CARACTERÍSTICAS
  for amen in amenity:
    prop = amen.attrs.get('itemprop')
    if prop =='floorSize':
      area.append(amen.get_text())
    elif prop =='numberOfRooms':
      quartos.append(amen.get_text())
    elif prop =='numberOfBathroomsTotal':
      banheiros.append(amen.get_text())
    # elif prop =='numberOfParkingSpaces':
    #   if amen.get_text() != '' and amen.get_text() != None:
    #     vagas.append(amen.get_text())
    #   else:
    #     vagas.append(None)
        


  #### PREÇOS
  for price in prices:
    pr = price.get_text().replace('.','')
    
    preco = re.findall(r"(?<=R\$ )\d+(?=\/\w+)", pr)[0]
    
    periodo = re.findall(r'\/\w{3}',pr)[0]
    periodo = periodo.split('/')[1].strip()
    
    if 'Cond' in pr:
      condominio = re.findall(r"(?<=Cond R\$ )\d+", pr)[0]
    else:
      condominio = None
      
    if 'IPTU' in pr:
      iptup = re.findall(r"(?<=IPTU R\$ )\d+", pr)[0]
    else:
      iptup = None
    
    aluguel.append(preco)
    periodos.append(periodo)
    cond.append(condominio)
    iptu.append(iptup)
  print(f'Página {i}')
  time.sleep(1)
    
print(len(bairros),len(cidades),len(quartos),len(banheiros),len(cond),len(iptu),len(aluguel),len(periodos))
df = pd.DataFrame(data={
  'bairro':bairros,
  'cidade':cidades,
  'quartos':quartos,
  'banheiros':banheiros,
  # 'vagas':vagas,
  'condominio':cond,
  'iptu':iptu,
  'aluguel':aluguel,
  'periodo':periodos,
})

df.to_excel('result.xlsx')