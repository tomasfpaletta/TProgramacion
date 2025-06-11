from datetime import datetime
from funciones_generales import registrar_error, generar_id
from json_handler import importar_datos_json, cargar_datos_json

def actualizar_stock(cantidad, producto):
    '''
    Reduce la cantidad de stock, si llega a 0 el producto pasa a estar deshabilitado.

    Input:
    - Cantidad de stock a restar

    Output:
    - Producto actualizado
    '''
    producto['stock'] -= cantidad
    if producto['stock'] == 0:
        producto['disponible'] = False
    
    return producto

def generar_carrito(lista_productos):
    '''
    Agrega productos al carrito del cliente hasta que el cliente decida detener el proceso.

    Input:
    - Lista de productos

    Output:
    - Lista de diccionarios (Cada diccionario es un producto con sus propiedades)
    '''
    carrito = []

    respuesta = input()
    while respuesta.lower() == 's':
        id_producto = int(input('Ingrese el indice del producto a agregar al carrito: '))
        producto = lista_productos[id_producto]
        input_cantidad = int(input(f'Cantidad ? Existen {producto['stock']} unidades disponibles\n'))

        while input_cantidad > producto['stock'] or input_cantidad < 1:
            print('Cantidad indicada fuera de rango. Indique nuevamente')
            input_cantidad = int(input(f'Cantidad ? Existen {producto["stock"]} unidades disponibles\n'))
        
        actualizar_stock(input_cantidad, producto)

        compra = {
            'marca': producto['marca'],
            'modelo': producto['modelo'],
            'color': producto['color'],
            'cantidad': input_cantidad,
            'total_prod': producto['precio'] * input_cantidad
        }

        carrito.append(compra)

        print(f'Producto agregado al carrito: {carrito}')
        print('Desea agregar otro producto? S/N')
        respuesta = input()
    
    if len(carrito) > 0:
        print(f'Agregaste los siguientes productos: {carrito}')
    else:
        print('No se agrego ningun producto al carrito')

    return carrito

def calcular_total(carrito):
    '''
    Calcula el costo total/final del carrito.

    Input:
    - Carrito (Lista de diccionarios)

    Output:
    - Costo total
    '''
    total = 0

    for prod in carrito:
        total += prod['total_prod']

    return total

def generar_compra(carrito, usuario, cid):
    '''
    Simula la finalizacion de la compra guardando el carrito en el json 'carts.json' y devolviendo el comprobante (Numero CID)

    Input:
    - Carrito (Lista de diccionarios)
    - Usuario
    - Cart ID (N°random)

    Output:
    - Valor total
    '''
    timestamp = datetime.now().strftime('%d/%m/%Y')
    productos = []
    total = 0

    for prod in carrito:
        total += prod['total_prod']
        productos.append(prod)

    compra = {
        'cid': cid,
        'user': usuario,
        'fecha': timestamp,
        'total': total,
        'productos': productos
    }

    try:
        lista_carrito = importar_datos_json('DB/carts.json')
        lista_carrito.append(compra)
        cargar_datos_json('DB/carts.json', lista_carrito)

        return compra
    except Exception as err:
        print('No se pudo realizar la compra debido al siguiente error:\n{err}')
        registrar_error(err)

