from functools import reduce
from datetime import datetime
from funciones_generales import registrar_error, limpiar_consola
from json_handler import importar_datos_json

def historial_compras_usuario(dni):
    '''
    Muestra las ventas que fueron realizadas por el usuario.

    Input:
    - DNI

    Output:
    - Historial de compras
    '''
    compras_realizadas = 0
    try:

        ventas = importar_datos_json('DB/ventas.json')
        for venta in ventas:
            if venta['user'] == dni:
                compras_realizadas += 1
                print(f"{'='*30}")
                print(f'Compra N°{venta['n_venta']}')
                print(f"{'-'*30}")
                print(f'-> Fecha de compra: {venta['fecha']}')
                print(f'-> Total: U$D {venta['total']:.2f}')
                print(f"{'-'*30}")
                i = 1
                for prod in venta['productos']:
                    print(f'Producto {i}')
                    print(f'├─ Marca: {prod['marca'].capitalize()}')
                    print(f'├─ Modelo: {prod['modelo'].capitalize()}')
                    print(f'├─ Color: {prod['color'].capitalize()}')
                    print(f'├─ Cantidad: {prod['cantidad']}')
                    print(f'└─ Subtotal: U$D {prod['total_prod']:.2f}')
                    i += 1
        
        if compras_realizadas == 0:
            print('No tenes ninguna compra registrada.')
    except Exception as err:
        print(f'Se produjo el siguiente error al intentar mostrar el historial de compras del usuario {dni} -> historial_compras_usuario():\n{err}')
        registrar_error(err)

def consultar_fecha():
    '''
    Input y validaciones de fecha.

    Input:
    - N/A

    Output:
    - Fecha ingresada
    '''
    while True:
        dia = input('Dia (dd): ')
        mes = input('Mes (mm): ')
        año = input('Mes (yyyy): ')

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
            print('La fecha ingresada es invalida. Al ingresar una fecha como 31/02 -> Esto no existe !!')
            continue

def menu_periodo():
    '''
    Genera el menu donde consulta el periodo a buscar.

    Input:
    - N/A

    Output:
    - Fecha de inicio y fecha de fin
    '''
    print('A continuacion indique el periodo en el que desea calcular las ventas')
    
    try:
        print('--- Fecha de inicio ---')
        fecha_inicio = consultar_fecha()

        print('--- Fecha de fin ---')
        fecha_fin = consultar_fecha()

        return fecha_inicio, fecha_fin
    except Exception as err:
        print(f'Se produjo el siguiente error al intentar conseguir la cantidad de ventas en la funcion -> menu_periodo():\n{err}')
        registrar_error(err)


def get_cant_ventas(fecha_inicio, fecha_fin, lista_ventas):
    '''
    Devuelve el total de ventas en el periodo indicado.

    Input:
    - Fecha de inicio periodo
    - Fecha de fin periodo
    - Lista de ventas

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
    - Lista de ventas

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
    '''
    Genera el menu para visualizar la facturacion y ventas del periodo ingresado.

    Input:
    - N/A

    Output:
    - Cantidad de ventas y facturacion total
    '''
    consultar_nuevamente = 's'

    try:
        ventas = importar_datos_json('DB/ventas.json')
        while consultar_nuevamente == 's':
            print('=== MENU DE FACTURACION Y VENTAS ===')
            fecha_inicio, fecha_fin = menu_periodo()
            cant_ventas = get_cant_ventas(fecha_inicio, fecha_fin, ventas)
            facturacion_total = get_fact_total(fecha_inicio, fecha_fin, ventas)
            
            limpiar_consola()

            print('=== MENU DE FACTURACION Y VENTAS ===')
            print(f'Periodo consultado: {fecha_inicio} a {fecha_fin}')
            print(f'Cantidad de ventas: {cant_ventas}')
            print(f'Facturacion total: U$D {facturacion_total}')

            consultar_nuevamente = input('Desea consultar otro periodo ? (S/N): ').lower()
        
        limpiar_consola()

    except Exception as err:
        print(f'Se produjo el siguiente error al intentar mostrar el menu de ventas -> menu_ventas():\n{err}')
        registrar_error(err)
