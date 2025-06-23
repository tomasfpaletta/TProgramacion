from datetime import datetime
from funciones_generales import registrar_error, generar_id, limpiar_consola
from json_handler import importar_datos_json, cargar_datos_json
from API_productos import mostrar_productos, restar_stock, sumar_stock, seleccionar_producto

listado_productos = importar_datos_json('DB/prods.json')
ventas = importar_datos_json('DB/ventas.json')

def pedir_cantidad(producto):
    '''
    Solicita al usuario la cantidad de unidades deseadas para un producto determinado.
    Se valida que la cantidad esté dentro del stock disponible.

    Input:
    - Producto (Diccionario)

    Output:
    - Cantidad (numero int)
    '''
    try:
        cantidad = int(input(f"¿Cuántas unidades desea? (Disponibles: {producto['stock']}): "))
        while cantidad < 1 or cantidad > producto['stock']:
            print("Cantidad fuera de rango.")
            cantidad = int(input(f"Ingrese una cantidad válida (1 a {producto['stock']}): "))
        return cantidad
    except ValueError:
        print("Cantidad inválida.")
        return 0

def eliminar_del_carrito(producto, carrito):
    '''
    Elimina el producto (diccionario) del carrito (lista de diccionarios). Devolviendo asi el carrito actualizado sin el producto indicado

    Input:
    - Producto (Diccionario)
    - Carrito (lista de diccionarios)

    Output:
    - Carrito actualizado sin el producto indicado (Lista de diccionarios)
    '''

    try:
        nuevo_carrito = [prod for prod in carrito if prod["pid"] != producto['pid']]
        print('Producto eliminado')
        return nuevo_carrito
    except Exception as err:
        print(f'Se produjo el siguiente error al intentar eliminar el producto del carrito en la funcion -> eliminar_del_carrito():\n{err}')
        registrar_error(err)
        return carrito

def generar_carrito(productos):
    '''
    Permite al usuario agregar productos al carrito de compra seleccionando con el PID.
    Muestra el catálogo, valida la disponibilidad del producto y la cantidad ingresada,
    actualiza el stock y construye una lista con los productos seleccionados.

    Input:
    - Productos (Lista de diccionarios)

    Output:
    - Carrito (Lista de diccionarios)
    '''
    carrito = []

    while input("¿Deseás agregar un producto al carrito? (S/N): ").lower() == 's':
        limpiar_consola()
        mostrar_productos(productos)
        producto = seleccionar_producto(productos)

        if not producto or not producto['disponible']:
            print("Producto no válido o no disponible.")
            continue

        cantidad = pedir_cantidad(producto)
        if not cantidad:
            continue

        pid = producto['pid']
        productos = restar_stock(cantidad, pid, productos)

        item = {
            'pid': producto['pid'],
            'marca': producto['marca'],
            'modelo': producto['modelo'],
            'color': producto['color'],
            'cantidad': cantidad,
            'total_prod': producto['precio'] * cantidad
        }

        carrito.append(item)
        print("Producto agregado al carrito.")

    if carrito:
        limpiar_consola()
        print("\nProductos en el carrito:")
        for prod in carrito:
            marca_upper, modelo_upper = map(str.upper, [prod['marca'], prod['modelo']])
            print(f"- PID: {prod['pid']} | {marca_upper} | {modelo_upper} x{prod['cantidad']} = U$D {prod['total_prod']:.2f}")

        return carrito, productos
    else:
        print("No se agregó ningún producto.")
        return carrito, productos

def calcular_total(carrito):
    '''
    Calcula el valor total/final del carrito.

    Input:
    - Carrito (Lista de diccionarios)

    Output:
    - Costo total
    '''
    total = 0
    try:
        for prod in carrito:
            total += prod['total_prod']
        return total
    except Exception as err:
        print(f'Se produjo el siguiente error al intentar calcular el total del carrito en la funcion -> calcular_total():\n{err}')
        registrar_error(err)
        return total

def generar_venta(carrito, dni, lista_historial_ventas):
    '''
    Simula la finalizacion de la compra guardando el carrito en el json 'carts.json' y devolviendo el comprobante (Numero de venta)

    Input:
    - Carrito (Lista de diccionarios)
    - DNI
    - Historial de ventas (Lista de diccionarios)

    Output:
    - Venta (Lista de diccionarios)
    - ventas.json actualizado
    '''
    try:
        timestamp = datetime.now().strftime('%d/%m/%Y')
        total = 0
        
        n_venta = generar_id(lista_historial_ventas, 'DNI')

        for prod in carrito:
            total += prod['total_prod']

        venta = {
            'n_venta': n_venta,
            'user': dni,
            'fecha': timestamp,
            'total': total,
            'productos': carrito
        }

        lista_ventas = importar_datos_json('DB/ventas.json')
        lista_ventas.append(venta)
        cargar_datos_json('DB/ventas.json', lista_ventas)

        return venta
    except Exception as err:
        print('No se pudo cargar la venta debido al siguiente error:\n{err}')
        registrar_error(err)
        return {}

def menu_comprar_productos(dni, listado_productos):
    '''
    Genera el menu de compra de productos.

    Input:
    - DNI
    - listado_productos: Lista de productos disponibles (diccionarios).

    Output:
    - Si la compra se confirma, guarda los datos en ventas.json y muestra al cliente la confirmacion.
    '''
    try:
        carrito, productos_stock_actualizado = generar_carrito(listado_productos)
        quitar = input('Desea sacar algun producto del carrito ? (S/N): ').lower()

        while quitar == 's' and carrito:
            prod_to_del = seleccionar_producto(carrito)
            carrito = eliminar_del_carrito(prod_to_del, carrito)
            productos_stock_actualizado = sumar_stock(prod_to_del['pid'], prod_to_del['cantidad'], productos_stock_actualizado) # Devolvemos el stock que se quito en memoria
            if carrito:
                quitar = input('Desea sacar otro producto del carrito ? (S/N): ').lower()
            else:
                print('Quitaste todos los productos del carrito.')


        if carrito: # Validamos que el carrito no este vacio.
            total = calcular_total(carrito)
            for prod in carrito:
                marca_upper, modelo_upper = map(str.upper, [prod['marca'], prod['modelo']])
                print(f"- PID: {prod['pid']} | {marca_upper} | {modelo_upper} x{prod['cantidad']} = U$D {prod['total_prod']:.2f}")
            print(f"\nTotal de la compra: U$D {total:.2f}")
            
            confirmar = input("Confirmar la compra (S/N): ").lower()
            if confirmar == 's':
                cargar_datos_json('DB/prods.json', productos_stock_actualizado) # Hacemos efectivo el cambio en el stock en disco
                venta = generar_venta(carrito, dni, ventas)
                print("\n=== Compra realizada con éxito ===")
                print(f"N° de venta : {venta['n_venta']}")
                print(f"Total: U$D {venta['total']:.2f}")
                print(f"Fecha: {venta['fecha']}\n")

                print('Gracias por confiar en nostros!')
                return productos_stock_actualizado
            else:
                print("Compra cancelada.")
                return listado_productos    
        else:
            print('Para proceder a la compra debes tener al menos un producto en el carrito.')
            return listado_productos
    except Exception as err:
        print('Ocurrio un error al intentar ejecutar el menu_comprar_productos()')
        print('VENTA NO CARGADA debido al siguiente error:\n{err}')
        registrar_error(err)