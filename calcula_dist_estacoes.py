import pandas as pd
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

dados = dados[ [ 'Código' , 'x' , 'y'] ]


dist_matrix = pd.DataFrame( squareform(pdist(dados.iloc[:, 1:]) ), columns=dados['Código'].unique(), index=dados['Código'].unique() )

dist_matrix.to_csv(diretorio_resultados+'/dist_matrix.csv',decimal=',')
# print(dist_matrix)

lista_estacoes = dist_matrix.columns
matriz_estacoes_proximas = pd.DataFrame()
for estacao in lista_estacoes:
	#seleciona coluna da estacao alvo
	dados_selecionados = dist_matrix[estacao]
	dados_selecionados = pd.DataFrame(dados_selecionados)

	#ordenar ascendente pelo coluna da estacao alvo
	dados_ordenados = dados_selecionados.sort_values(by=estacao, ascending=True)
	
	# seleciona as estações com distancia maior que 1 metro
	dados_ordenados = dados_ordenados[dados_ordenados[estacao] > 1]
	estacoes_proximas = dados_ordenados.iloc[1:4 , :]
	
	estacoes_proximas.to_csv(diretorio_resultados+'/tres_mais_estacoes_proximas/'+str(estacao)+'.csv', decimal=',')
	estacoes_proximas.to_csv(diretorio_resultados+'/tres_mais_estacoes_proximas/completo.csv', decimal=',', mode='a',)


# print(matriz_estacoes_proximas)
# matriz_estacoes_proximas.to_csv(diretorio_resultados+'/3_mais_proximas.csv',decimal=',')
# raise Exception()



