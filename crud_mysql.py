# import time
# import mysql.connector
import pandas as pd
import os
from sqlalchemy import create_engine
import json

with open("sshsnmp_config.json", "r") as config_file:
    db_auth = json.load(config_file)

table_name = db_auth["db_Table"]
file_path = f'{db_auth["load_filePath"]}log SNMPwalk MAC-PORTA.xlsx'
def log_to_db(data, table_name):
    # connection = mysql.connector.connect(
    #     host='127.0.0.1',
    #     port='3306',
    #     user='root',
    #     password='root',
    #     database='teste'
    # )
    db = create_engine(f"mysql+mysqlconnector://{db_auth['db_Login']}:{db_auth['db_Pass']}@{db_auth['db_Ip']}:{db_auth['db_Port']}/logs")
    # engine = create_engine("mysql+mysqlconnector://root:root@127.0.0.1:3306/teste")

    print('Conectado ao Banco..')

    data.to_sql(name=table_name, con=db, if_exists='replace', index=False)
    print("Dados inseridos no MySQL com sucesso.")




def main():
    df = pd.read_excel(file_path)
    if df.empty:
        input(f"Confira se o arquivo existe no caminho {file_path}")
        sys.exit(0)
        sys.exit(-1)
    log_to_db(df, table_name)

if __name__ == '__main__':
    main()

# Fechar a conexão com o banco de dados quando terminar

