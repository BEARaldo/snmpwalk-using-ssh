import pandas as pd
import json

with open("sshsnmp_config.json",'r') as config_file:
    config = json.load(config_file)

with open("macs.json", 'r') as list_file:
    val = json.load(list_file)

maclist = val["macs"]
file_path = f'{config["load_filePath"]}log SNMPwalk MAC-PORTA.xlsx'
column_name = 'MAC'
discovered_mac = []
def search_values_in_column(file_path, column_name, maclist):
    try:
        # Carregar a planilha em um DataFrame
        df = pd.read_excel(file_path)  # pd.read_csv arquivo CSV

        # Verificar se a coluna especificada existe no DataFrame
        if column_name not in df.columns:
            return f"A coluna '{column_name}' não existe na planilha."

        # Filtrar o DataFrame para encontrar as linhas com os valores de busca
        filtered_df = df[df[column_name].str.startswith(tuple(maclist))]

        if not filtered_df.empty:
            # Se houver correspondências, imprimir as linhas correspondentes
            print(f"Macs encontrados:\n{filtered_df}")
            discovered_mac.append(filtered_df)
        else:
            print("Nenhuma correspondência encontrada.")

    except Exception as e:
        print(f"Erro: {str(e)}")

def main():
    search_values_in_column(file_path, column_name, maclist)
    # for i in discovered_mac:
    #     print(discovered_mac[i])

    if discovered_mac:
        combined_df = pd.concat(discovered_mac, ignore_index=True)
        output_file_path = 'resultados_encontrados.xlsx'
        combined_df.to_excel(output_file_path, index=False)
        print(f"Resultados salvos em '{output_file_path}'")
    else:
        print("Nenhum resultado para salvar.")

if __name__ == '__main__':
    main()