### PROJETO 02 
#### TRATAMENTO DE BASE DE DADOS DE VÔOS

O Projeto apresenta o tratamento dos dados disponibilizados na planilha:
https://raw.githubusercontent.com/JackyP/testing/master/datasets/nycflights.csv

### Descrição das Pastas:

Os arquivos estão dentro da pasta principal "projeto02".
Arquivo ".env" com o link do arquivo de metadados e o link da planilha a ser tratada. 
Arquivo "requirements.txt" foi criado para instalação dos arquivos necessários.
Arquivo "app.py" que contém todo processo.
Na pasta "assets" se encontram arquivos para conexão com a tabela, arquivo com funções e o arquivo de emtadados.
Na pasta "data" está o arquivo de dados e o arquivo de log de execução.

### Como utilizar:

1. Crie um ambiente virtual
```
python -m venv env
```
2. Ative o ambiente virtual
3. Instale o requirements (se necessário)
```
pip install -r requirements.txt
```
4. Execute o script principal
```
python .\app.py
```

