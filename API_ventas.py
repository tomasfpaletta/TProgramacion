from functools import reduce
from datetime import datetime
from funciones_generales import registrar_error
from json_handler import importar_datos_json

def consultar_fecha():
    while True:
        dia = input('Dia (dd): ')
        mes = input('Mes (mm): ')
        año = input('Mes: (yyyy)')

        if not (dia.isdigit() and mes.isdigit() and año.isdigit()):
            print('Todos los campos deben ser numericos. Ejemplo 01, 20, etc.')
            continue

        if len(dia) != 2 or not ('01' <= dia <= '31'):
            print('Dia invalido. Usa dos digitos entre 01 y 31')
            continue

        if len(mes) != 2 or not ('01' <= mes <= '12'):
            print('Mes invalido. Usa dos digitos entre 01 y 12')
            continue

        if len(año) != 4 or not ('2024' <= año <= '2025'):
            print('Año invalido. Usa cuatro digitos entre 2024 y 2025')
            continue

        fecha = f'{dia}/{mes}/{año}'

        try:
            fecha_ingresada = datetime.strptime(fecha, '%d/%m/%Y').date()
            hoy = datetime.today().date()
            if fecha_ingresada > hoy:
                print('No podes ingresar una fecha futura.')
                continue
            return fecha
        except ValueError:
            print('La fecha ingresada es invalida. Ingresar una fecha como 31/02 -> Esto no existe !!')
            return None

def menu_periodo():
    print('A continuacion indique el periodo en el que desea calcular las ventas')
    
    try:
        print('--- Fecha de inicio ---')
        fecha_inicio = consultar_fecha()

        print('--- Fecha de fin ---')
        fecha_fin = consultar_fecha()
    except Exception as err:
        print(f'Se produjo el siguiente error al intentar conseguir la cantidad de ventas en la funcion -> menu_periodo():\n{err}')
        registrar_error(err)
        return fecha_inicio, fecha_fin


def get_cant_ventas(fecha_inicio, fecha_fin, lista_ventas):
    '''
    Devuelve el total de ventas en el periodo indicado.

    Input:
    - Fecha de inicio periodo
    - Fecha de fin periodo

    Output:
    - Cantidad de ventas (num int)
    '''
    cant_ventas = 0
    try:
        cant_ventas = reduce(lambda acc, venta: acc + (1 if fecha_inicio <= venta['fecha'] <= fecha_fin else 0), lista_ventas, 0)

        return cant_ventas
    except Exception as err:
        print(f'Se produjo el siguiente error al intentar conseguir la cantidad de ventas en la funcion -> get_cant_ventas():\n{err}')
        registrar_error(err)
        return cant_ventas
    
def get_fact_total(fecha_inicio, fecha_fin, lista_ventas):
    '''
    Devuelve el total facturado en el periodo indicado

    Input:
    - Fecha de inicio periodo
    - Fecha de fin periodo

    Output:
    - Cantidad de ventas (num int)
    '''
    facturado = 0
    try:
        facturado = reduce(lambda suma, venta: suma + (venta['total'] if fecha_inicio <= venta['fecha'] <= fecha_fin else 0), lista_ventas, 0)

        return facturado
    except Exception as err:
        print(f'Se produjo el siguiente error al intentar conseguir la facturacion total en la funcion -> get_fact_total():\n{err}')
        registrar_error(err)
        return facturado
    
def menu_ventas():
    try:
        ventas = importar_datos_json('DB/ventas.json')
    except Exception as err:

# cant = get_cant_ventas('10/05/2025', '22/05/2025', ventas)
# print(cant)

# fact = get_fact_total('10/05/2025', '22/05/2025', ventas)
# print(fact)