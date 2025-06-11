import json

def importar_datos_json(archivo_json):
    '''
    Importa los datos que se encuentren dentro del archivo JSON que se pase como argumento. Se decidio hacer de esta forma para evitar la repititvidad con los 3 archivos (users, products y carts).

    Inputs:
    - Archivo JSON

    Output:
    - Lista (de diccionarios)
    '''
    try:
        with open(archivo_json, 'r', encoding='utf-8') as contentido:
            lista_importada = json.load(contentido)
            return lista_importada
    except FileNotFoundError:
        print(f'El archivo "{archivo_json}.json" no existe!')
    except PermissionError:
        print('No posees permisos para el archivo')
    except json.JSONDecodeError:
        print('Revisa que el archivo tenga un forma JSON valido!')
    except Exception as err:
        print(f'No se logro abrir el archivo. El error es: {err}')

def cargar_datos_json(archivo_json, lista_nueva):
    '''
    Carga los datos en la lista que se le pase por parametro al JSON indicado por parametro.

    Inputs:
    - Lista (de diccionarios)
    - Archivo JSON (destino)

    Output:
    - Archivo JSON Actualizado
    '''
    try:
        with open(archivo_json, 'w', encoding='utf-8') as contentido:
            json.dump(lista_nueva, contentido, indent=4) # Indent le da formato para que sea legible despues en el JSON
    except PermissionError:
        print('No posees permisos para el archivo')
    except Exception as err:
        print(f'No se logro abrir el archivo. El error es: {err}')