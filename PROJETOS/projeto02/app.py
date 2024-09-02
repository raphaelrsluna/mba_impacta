import sqlite3
import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import assets.utils as utils
from assets.utils import logger
import datetime

load_dotenv()

def data_clean(df, metadados):
    '''
    Função principal para saneamento dos dados
    INPUT: Pandas DataFrame, dicionário de metadados
    OUTPUT: Pandas DataFrame, base tratada
    '''
    df["data_voo"] = pd.to_datetime(df[['year', 'month', 'day']]) 
    df = utils.null_exclude(df, metadados["cols_chaves"])
    df = utils.convert_data_type(df, metadados["tipos_originais"])
    df = utils.select_rename(df, metadados["cols_originais"], metadados["cols_renamed"])
    df = utils.string_std(df, metadados["std_str"])

    df.loc[:,"datetime_partida"] = df.loc[:,"datetime_partida"].str.replace('.0', '')
    df.loc[:,"datetime_chegada"] = df.loc[:,"datetime_chegada"].str.replace('.0', '')

    for col in metadados["corrige_hr"]:
        lst_col = df.loc[:,col].apply(lambda x: utils.corrige_hora(x))
        df[f'{col}_formatted'] = pd.to_datetime(df.loc[:,'data_voo'].astype(str) + " " + lst_col)
    
    logger.info(f'Saneamento concluido; {datetime.datetime.now()}')
    return df

def feat_eng(df):
    '''
    Função para Criação de novos campos / Engenharia de Features
    INPUT: Pandas DataFrame
    OUTPUT: Pandas DataFrame, base tratada
    '''
    df["tempo_voo_esperado"] = (df["datetime_chegada_formatted"] - df["datetime_partida_formatted"]) / pd.Timedelta(hours=1)
    df["tempo_voo_hr"] = df["tempo_voo"] /60
    df["atraso"] = df["tempo_voo_hr"] - df["tempo_voo_esperado"]
    df["dia_semana"] = df["data_voo"].dt.day_of_week #0=segunda

    df["horario"] = df.loc[:,"datetime_partida_formatted"].dt.hour.apply(lambda x: utils.classifica_hora(x))

    df["flg_status"] = df.loc[:,"atraso"].apply(lambda x: utils.flg_status(x))

    df["flg_potencial_erro"] = np.where(df["atraso"]<= -10, True, False)
    df["flg_atraso"] = np.where(df["atraso"] > 0.6, True, False)
    df["flg_adiantado"] = np.where(
        (df["atraso"]< -0.5) & (df["atraso"] > -10), True, False)    
    
    logger.info(f'Engenharia de Features concluido; {datetime.datetime.now()}')
    return df

def save_data_sqlite(df):
    '''
    Antiga função para gravação no Banco de Dados
    INPUT: Pandas DataFrame
    OUTPUT: --
    '''    
    try:
        conn = sqlite3.connect("data/NyflightsDB.db")
        logger.info(f'Conexao com banco estabelecida ; {datetime.datetime.now()}')
    except:
        logger.error(f'Problema na conexao com banco; {datetime.datetime.now()}')
    c = conn.cursor()
    df.to_sql('nyflights', con=conn, if_exists='replace')
    conn.commit()
    logger.info(f'Dados salvos com sucesso; {datetime.datetime.now()}')
    conn.close()

def fetch_sqlite_data(table):
    '''
    Função principal para gravação no Banco de Dados
    INPUT: Nome da Tabela para efetuar o select
    OUTPUT: Print com os primeiros 5 registros da tabela
    '''    
    try:
        conn = sqlite3.connect("data/NyflightsDB.db")
        logger.info(f'Conexao com banco estabelecida ; {datetime.datetime.now()}')
    except:
        logger.error(f'Problema na conexao com banco; {datetime.datetime.now()}')
    c = conn.cursor()
    c.execute(f"SELECT * FROM {table} LIMIT 5")
    print(c.fetchall())
    conn.commit()
    conn.close()


if __name__ == "__main__":
    logger.info(f'Inicio da Execucao ; {datetime.datetime.now()}')
    logger.info(f'Lendo Metadados; {datetime.datetime.now()}')
    metadados  = utils.read_metadado(os.getenv('META_PATH'))
    logger.info(f'Lendo Dados; {datetime.datetime.now()}')
    df = pd.read_csv(os.getenv('DATA_PATH'),index_col=0)
    logger.info(f'Limpeza dos dados; {datetime.datetime.now()}')
    df = data_clean(df, metadados)
    logger.info(f'Validando Nulos; {datetime.datetime.now()}')
    utils.null_check(df, metadados["null_tolerance"])
    logger.info(f'Validando Chaves; {datetime.datetime.now()}')
    utils.keys_check(df, metadados["cols_chaves_renamed"])
    logger.info(f'Engenharia de Features; {datetime.datetime.now()}')
    df = feat_eng(df)
    #save_data_sqlite(df)
    logger.info(f'Gravando no Banco; {datetime.datetime.now()}')
    fetch_sqlite_data(metadados["tabela"][0])
    logger.info(f'Fim da Execucao ; {datetime.datetime.now()}')