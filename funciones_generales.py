import random
import os
from datetime import datetime

def generar_id(lista):
    '''
    Genera un numero random el cual sera el ID (PID/CID). Va de 1000 a 9999.
    Se valida que no exista duplicados.

    Input:
    - Lista de productos

    Output:
    - Numero PID
    '''
    id_random = random.randint(1000, 9999)
    ids_existentes = {item['DNI'] for item in lista if 'DNI' in item}
    
    while id_random in ids_existentes: # Si no existe lo agrego, sino vuelve a probar otro numero
        id_random = random.randint(1000, 9999)
    
    return id_random

def registrar_error(err):
    '''
    Registra las excepciones que ocurran durante la ejecucion del script en el archivo "error_logs.txt", si no existe lo crea.

    Inputs:
    - Error/Exception

    Output:
    - Registro actualizado/nuevo
    '''
    timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    registro = f'{timestamp} TIPO: {type(err)} - ERROR: {str(err)}\n'
    try:
        with open('logs/error_logs.txt', 'a', encoding='utf-8') as archivo:
            archivo.write(registro)
    except FileNotFoundError:
        with open('logs/error_logs.txt', 'w', encoding='utf-8') as archivo:
            archivo.write(registro)
    except Exception as err:
        print(f'No se pudo registrar el error:\n{err}')

def limpiar_consola():
    '''
    Limpia la consola.   

    Inputs:
    - N/A

    Output:
    - Consola limpia ('cls' en Windows / 'clear' en GNULinux)
    '''
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except Exception as err:
        print(f'Error al tratar de limpiar la consola:\n---->{err}')
        registrar_error(err)
