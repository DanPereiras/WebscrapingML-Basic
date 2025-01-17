import requests #BIBLIOTECAS
from bs4 import BeautifulSoup
import re
import math
import pandas as pd

url = "https://lista.mercadolivre.com.br/teclado-mecanico#D[A:Teclado%20mecanico]" #LINK QUE DESEJA EXTRAIR OS DADOS
headers = {
    'User-Agent': ""
} # DEFINE O HEADER PARA O SITE RECONHECER O DISPOSITIVO

response = requests.get(url, headers=headers) #RESPOSTA DA REQUISIÇÃO

lista_produtos = [] # ARMAZENA A LISTA DO DADOS ENCONTRATOS

if response.status_code == 200: #CONDIÇÃO CASO A REQUISIÇÃO DÊ CERTO
    soup = BeautifulSoup(response.text, "html.parser")
    qtd_itens = soup.find('span', class_="ui-search-search-result__quantity-results").text #TRAZ A QUANTIDADE DE ITENS ENCONTRADOS

    index = qtd_itens.find(' ')  #TIRA O ESPAÇO DO DADO ENCONTRATO
    qtd = qtd_itens[:index]  # QUANTIDADE DE ITENS SEM STR
    num_itens = int(qtd.replace('.', ''))  #DEFINE A VARIÁVEL QTD_ITENS PARA NUMERO INTEIRO E TIRA O "."
    itens_por_pagina = 48 #QUANTIDADE DE ITENS POR PAGINA
    ultima_pagina = math.ceil(num_itens / itens_por_pagina)  #QUANTIDADE TOTAL DE ITENS ENCONTRADOS

    for i in range(0, ultima_pagina):  #PEGA DA PAGINA 1 ATÉ A ULTIMA PAGINA.

        item_inicial = (i * itens_por_pagina + 1)
        url_pag = f"https://lista.mercadolivre.com.br/informatica/perifericos-pc/mouses-teclados/teclados/teclados-fisicos/teclado-mecanico_Desde_{item_inicial}_NoIndex_True" #URL COM NUMERO DE PAGINA/ITENS
        response = requests.get(url_pag, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        produtos = soup.find_all("li", class_="ui-search-layout__item") #BUSCA TODOS OS PRODUTOS

        for produto in produtos:
            titulo_produto = produto.find("h2", class_=re.compile("ui-search-item__title ui-search-item__group__element"))
            # caso não encontre o título, tenta a outra classe do nome de produto
            if not titulo_produto:
                titulo_produto = produto.find("h2", class_=re.compile("poly-box poly-component__title"))
            titulo_produto = titulo_produto.text
            preco_produto = produto.find("span", class_=re.compile("andes-money-amount__fraction")).text

            dic_produto = {"titulo": titulo_produto, "preco": (preco_produto + ",00")} #DICIONARIO PARA DEFINIR CADA TAG ENCONTRADA, NOME E PREÇO

            lista_produtos.append(dic_produto) #LISTA DE PRODUTOS
      
        print(lista_produtos)
        print(url_pag)

# df = pd.DataFrame(lista_produtos)
# df.to_csv('C:/Users/Área de Trabalho/Python/teclado.csv', encoding='utf-8', sep=';') #SALVA ARQUIVOS EM CSV
