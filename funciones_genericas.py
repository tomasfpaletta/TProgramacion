from datetime import datetime

error_logs = 'logs/error_logs.txt'

def registrar_error(err):
    '''
    Registra las excepciones que ocurran durante la ejecucion del script en el archivo "error_logs.txt", si no existe lo crea.

    Inputs:
    - Error/Exception

    Output:
    - Agrega la excepcion al registro
    '''
    timestamp = datetime.now().strftime('%d/%m/%y %H:%M:%S')
    registro = f'{timestamp} TIPO: {type(err)} - ERROR: {str(err)}\n'
    try:
        with open(error_logs, 'a', encoding='utf-8') as archivo:
            archivo.write(registro)
    except FileNotFoundError:
        with open(error_logs, 'w', encoding='utf-8') as archivo:
            archivo.write(registro)
    except Exception as err:
        print(f'No se pudo registrar el error:\n{err}')