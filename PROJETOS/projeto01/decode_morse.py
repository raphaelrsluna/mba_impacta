'''
O Código Morse é um sistema de representação de letras, algarismos e sinais de pontuação através
de um sinal codificado enviado de modo intermitente. Foi desenvolvido por Samuel Morse em 1837, 
criador do telégrafo elétrico, dispositivo que utiliza correntes elétricas para controlar eletroímãs 
que atuam na emissão e na recepção de sinais. 
O script tem a finalidade de decifrar uma mensagem em código morse e salvá-la em texto claro.
'''

import os
import sys
import datetime
import pandas as pd
from config import file_path, dict_morse

def decode_morse(msg):
    '''
    input : mensagem em código morse com as palavras separadas por 2 espaços
    output : frase escrita em letras e algarismos
    '''
    msg_lst = msg.split("  ")
    msg_claro = []
    for phrase in msg_lst:
        msg_claro.append(decode_morse_palavras(phrase))
    return " ".join(msg_claro)

def decode_morse_palavras(plv):
    '''
    input : mensagem em código morse com as letras separadas por espaços
    output : palavra escrito em letras e algarismos
    '''
    plv_lst = plv.split(" ")
    plv_claro = []
    for letter in plv_lst:
        plv_claro.append(str(dict_morse[letter]))
    return "".join(plv_claro)

def save_clear_msg_csv_hdr(msg_claro):
    '''
    input : mensagem em texto claro
    output : palavra escrito em letras e algarismos, salva em arquivo txt
    '''
    now = datetime.datetime.now()
    df = pd.DataFrame([[msg_claro, now]], columns=["mensagem", "datetime"])
    hdr = not os.path.exists(file_path)
    df.to_csv(file_path, mode ="a", index = False, header=hdr)

if __name__ == "__main__":
    msg_claro = decode_morse(sys.argv[1])
    save_clear_msg_csv_hdr(msg_claro)