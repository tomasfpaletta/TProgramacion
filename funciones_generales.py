import random
import os
from datetime import datetime

def generar_id(lista, key):
    '''
    Genera un numero random el cual sera el ID (PID/CID). Va de 1000 a 9999.
    Se valida que no exista duplicados.

    Input:
    - Lista de productos
    - Key

    Output:
    - Numero PID
    '''
    try:
        id_random = random.randint(1000, 9999)
        ids_existentes = {item[key] for item in lista if key in item}
        
        while id_random in ids_existentes: # Si no existe lo agrego, sino vuelve a probar otro numero
            id_random = random.randint(1000, 9999)
        
        return id_random
    except Exception as err:
        print(f'Error al intentar generar un ID en generar_id()\n{err}')
        registrar_error(err)

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
        print(f'Error al intentar limpiar la consola:\n---->{err}')
        registrar_error(err)

def actualizar_lista(key, value, diccionario, lista):
    '''
    Actualiza la lista que se pase por argumento con el diccionario indicado.

    Inputs:
    - Diccionario = Usuario y/o Producto
    - Lista de diccionarios = lista de productos y/o lista de usuarios

    Output:
    - Lista de diccionarios actualizada
    '''
    try:
        for i, item in enumerate(lista):
            if item[key] == value:
                lista[i] == diccionario
                break
            else:
                print('ADVERTENCIA: La lista no cambio.')
                return lista
        return lista
    except Exception as err:
        print(f'Error al intentar actualizar la lista {lista}\n{err}')
        registrar_error(err)
