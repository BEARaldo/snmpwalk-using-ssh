import sys
import schedule
import time
import threading
import os
import keyboard
from snmp_available_check import main as xlsx_generator
from ssh_command import main as snmpwalk
from ler_macs import main as ler_macs
from crud_mysql import main as insert_db

stop_program_var = False
def stop_program():
    global stop_program_var
    print('Parando programa')
    stop_program_var = True
    sys.exit(0)

def clear_console():
    os.system('cls')

def dependencies_install():
    import subprocess
    install_command = "pip install -r requirements.txt"
    try:
        subprocess.check_call(install_command, shell=True)
    except subprocess.CalledProcessError:
        print("Erro ao instalar as dependências.")


# def key_detection():
#     while True:
#         if keyboard.is_pressed('ctrl+s'):
#             print('Parando programa')
#             break
#
#
#         if keyboard.is_pressed('ctrl+l'):
#             os.system('cls')
#
#
#         time.sleep(0.5)  # Intervalo pequeno para evitar uso intensivo da CPU

def main():
    clear_console()
    xlsx_generator()
    snmpwalk()  ##argumentos snmpwalk n_threads = x(threads total, connection_lock = conexão disponivel
    insert_db()
    ler_macs()


if __name__ == '__main__':
    keyboard.add_hotkey('ctrl+s', stop_program)
    keyboard.add_hotkey('ctrl+l', clear_console)
    dependencies_install()
    # get_key = threading.Thread(target=key_detection)
    # get_key.daemon = True
    # get_key.start()
    ##schedule config
    schedule.every(35).minutes.do(main)
    while not stop_program_var:
        schedule.run_all(delay_seconds=10)
        schedule.run_pending()
        clear_console()
        print(f'Executando novamente as {schedule.next_run()}')
    input('encerrado. Pressione Enter...')

