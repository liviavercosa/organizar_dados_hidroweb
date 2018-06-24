import pandas as pd
from datetime import date
import calendar
import os, fnmatch

# diretorio com os arquivos CSV das estações
diretorio_estacoes = 'dados/chuvas'
# diretorio para salvar a matriz gerada
diretorio_resultados = 'resultados'



lista_arquivos = os.listdir(diretorio_estacoes)


print(lista_arquivos)

# matriz final Indices: datas; Colunas: códigos das estações; Valores: quantidade de chuva 
matriz_completa = pd.DataFrame()

# para cada arquivo insere os dados de chuva na matriz completa
extensao = "*.csv"  
for arquivo in lista_arquivos:
	if fnmatch.fnmatch(arquivo, extensao):
		print('########## Arquivo : ', arquivo)

		dados =  pd.read_csv(diretorio_estacoes+'/'+arquivo, delimiter=';', decimal=',', comment='/')
		if(dados.size == 0):
			continue
		
		cod_estacao = dados['EstacaoCodigo'].iloc[0]
		
		# seleciona as colunas de chuva
		dadosChuvas  = dados.iloc[: , 13:44] 
		# seleciona as colunas de data
		datas = dados['Data']
		# uniao das colunas de datas e chuvas
		dados = pd.concat([datas , dadosChuvas],axis=1,sort=True)
		

		nLinhas = dados.shape[0] # numero de meses, um para cada linha


		matriz = pd.DataFrame(columns=[cod_estacao])

		# para cada mês é selcionado o registro de chuva para cada dia
		for indice in range(nLinhas):

			year, month, day = map(int, dados.values[indice][0].split('-'))
			# monthsize quantidade de dias do mês selecionado
			weekday , monthsize = calendar.monthrange(year,month)
			
			for dia in range(day,monthsize):
				data = date(year,month, dia)
				matriz.loc[data] = dados.iloc[indice].values[dia]

		# concatena a matriz gerado de um arquivo com a matriz completa
		matriz_completa = pd.concat([matriz_completa , matriz],axis=1, sort=True)

print(matriz_completa)

# exemplo de seleção de dados entre duas datas...
matriz_completa.loc[ date(1962,1, 1): date(1963,1,1) ].to_csv(diretorio_resultados+'/teste.csv')

matriz_completa.to_csv(diretorio_resultados+'/matriz_completa.csv')