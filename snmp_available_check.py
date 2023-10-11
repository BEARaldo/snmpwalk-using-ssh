from pyzabbix import ZabbixAPI
from openpyxl import Workbook
from pathlib import Path
import re
import time
import requests
import json
import pandas as pd
# from unidecode import unidecode


requests.packages.urllib3.disable_warnings() #desativa erro InsecureRequestWarning

#zabbix logon
with open('zabbix_authdata.json', 'r') as auth_file:
    data = json.load(auth_file)

with open("sshsnmp_config.json", 'r') as config_file:
    config_path = json.load(config_file)

zapi = ZabbixAPI(data['zabbix_url'])
zapi.session.verify = False
zapi.login(data['user'], data['password'])


#excel save

def save_excel(host_list, qnt=0):
    path = Path(f'{config_path["save_filePath"]}hosts com falha SNMP.xlsx')
    wb = Workbook()
    hosts_xlsx = wb.active
    count = 1

    hosts_xlsx[f'A{count}'] = 'hostname'
    hosts_xlsx[f'B{count}'] = 'IP'
    hosts_xlsx[f'C{count}'] = 'Disponibilidade SNMP'
    hosts_xlsx[f'D{count}'] = 'Erro SNMP'

    count += 1

    for host in host_list:
        # city_str = ', '.join(host['city'])
        hosts_xlsx[f'A{count}'] = host['name']
        hosts_xlsx[f'B{count}'] = host['ip']
        hosts_xlsx[f'C{count}'] = host['disponivel_snmp']
        hosts_xlsx[f'D{count}'] = host['erro_snmp']
        count += 1


    hosts_xlsx['F1'] = 'Quantidade total de switches em falha SNMP'
    hosts_xlsx['F2'] = qnt
    hosts_xlsx['G1'] = f'Gerada as {time.strftime("%H:%M:%S")}'




    wb.save(path)
    print(f'salvo em {path}')





# Função para obter informações do host associado a um problema
def test_severity():
    discovery_hosts_in_sla = zapi.host.get(output='extend',
                                           groupids=['407'],
                                          )
    count = 0

    no_snmp_host = []
    for host in discovery_hosts_in_sla:
        if host['snmp_error'] != '' or host['snmp_available'] == 2:
            host_info = {'name': host['name'],
                         'ip': host['host'],
                         'disponivel_snmp': host['snmp_available'],
                         'erro_snmp': host['snmp_error']}

            no_snmp_host.append(host_info)
            count +=1
    return no_snmp_host, count

def main():
    no_snmp_host, count = test_severity()
    save_excel(no_snmp_host, count)

if __name__ == '__main__':
    inicio = time.time()
    main()
    fim = time.time()
    total_t = fim - inicio
    print(f'Tempo de execução: {total_t:.2f} segundos.')

