import pandas as pd
import numpy as np
from datetime import date
import calendar
import os
from scipy.spatial.distance import squareform, pdist


nome_arquivo = "estacoes_pluvi_pe.csv"
# diretorio com os arquivos CSV das estações
diretorio_estacoes = 'dados'
# diretorio para salvar a matriz gerada
diretorio_resultados = 'resultados'


dados =  pd.read_csv(diretorio_estacoes+'/'+nome_arquivo, delimiter=',', decimal='.')

dados = dados[ [ 'Código' ,'Estação', 'x' , 'y'] ]

# print(dados)

dist_matrix = pd.DataFrame( squareform(pdist(dados.iloc[:, 2:]) ), columns=dados['Código'].unique(), index=dados['Código'].unique() )


# print(dist_matrix)

lista_estacoes = dist_matrix.columns
colunas_matriz = ['codigo_combinado','codigo_1','estacao_1', 'codigo_2', 'estacao_2']
matriz_similares = pd.DataFrame(columns=colunas_matriz)
for estacao in lista_estacoes:
	#seleciona coluna da estacao alvo
	dados_selecionados = dist_matrix[estacao]
	dados_selecionados = pd.DataFrame(dados_selecionados)

	#ordenar ascendente pelo coluna da estacao alvo
	dados_ordenados = dados_selecionados.sort_values(by=estacao, ascending=True)
	
	# seleciona as estações com distancia maior que 1 metro

	dados_similares = dados_ordenados[dados_ordenados[estacao] < 5]
	if (dados_similares.size > 1):

		# print(dados_similares.index[0],dados_similares.index[1])
		codigo_1 = dados_similares.index[0]

		nome_1 = dados[ dados['Código'] == codigo_1]
		nome_1 = nome_1['Estação'].values[0]	

		print(nome_1)
		codigo_2 = dados_similares.index[1]
		nome_2 = dados[ dados['Código'] == codigo_2]
		nome_2 = nome_2['Estação'].values[0]
		print(nome_2)

		# raise Exception()
		codigo_combinado = str(codigo_1) + '_'+ str(codigo_2)
		df = pd.DataFrame([[ codigo_combinado, codigo_1, nome_1, codigo_2, nome_2]], columns=colunas_matriz)
		matriz_similares = matriz_similares.append(df,ignore_index=True)
matriz_similares = matriz_similares.drop_duplicates()
matriz_similares.to_csv(diretorio_resultados+'/matriz_estacoes_similares.csv', decimal=',', encoding='utf-8')

print(matriz_similares)




