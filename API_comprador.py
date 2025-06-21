from datetime import datetime
from funciones_generales import registrar_error, generar_id
from json_handler import importar_datos_json, cargar_datos_json
from API_productos import mostrar_productos, retornar_prod, actualizar_stock

listado_productos = importar_datos_json('DB/prods.json')
ventas = importar_datos_json('DB/carts.json')

def seleccionar_producto(productos):
    '''
    Permite al usuario seleccionar un producto ingresando su PID.
    Valida la existencia del producto en la lista.

    Input:
    - productos: Lista de diccionarios de productos.

    Output:
    - producto (dict): El producto seleccionado si existe, o None si no se encuentra o hay error.
    '''
    try:
        pid = int(input("Ingrese el PID del producto a agregar: "))
        resultado = retornar_prod(pid, productos)
        if not resultado:
            print("PID no encontrado.")
            return None # podria firjarme retornar un producto (lista) vacio.
        return resultado[0]
    except ValueError:
        print("PID inválido.")
        return None

def pedir_cantidad(producto):
    '''
    Solicita al usuario la cantidad de unidades deseadas para un producto determinado.
    Valida que la cantidad esté dentro del stock disponible.

    Input:
    - producto: Diccionario del producto seleccionado.

    Output:
    - cantidad (int): Cantidad validada, o None si la entrada es inválida.
    '''
    try:
        cantidad = int(input(f"¿Cuántas unidades desea? (Disponibles: {producto['stock']}): "))
        while cantidad < 1 or cantidad > producto['stock']:
            print("Cantidad fuera de rango.")
            cantidad = int(input(f"Ingrese una cantidad válida (1 a {producto['stock']}): "))
        return cantidad
    except ValueError:
        print("Cantidad inválida.")
        return None

def generar_carrito(productos):
    '''
    Permite al usuario agregar productos al carrito de compra a través del PID.
    Muestra el catálogo, valida la disponibilidad del producto y la cantidad ingresada,
    actualiza el stock y construye una lista con los productos seleccionados.

    Input:
    - productos: Lista de productos disponibles (diccionarios).

    Output:
    - carrito: Lista de diccionarios con los productos seleccionados por el usuario.
    '''
    carrito = []

    print("\n=== CATÁLOGO DE PRODUCTOS ===")
    mostrar_productos(productos)

    while input("¿Deseás agregar un producto al carrito? (S/N): ").lower() == 's':
        producto = seleccionar_producto(productos)

        if not producto or not producto['disponible']:
            print("Producto no válido o no disponible.")
            continue

        cantidad = pedir_cantidad(producto)
        if not cantidad:
            continue

        pid = producto['pid']
        lista_prods_actualizada = actualizar_stock(cantidad, pid, productos)

        item = {
            'marca': producto['marca'],
            'modelo': producto['modelo'],
            'color': producto['color'],
            'cantidad': cantidad,
            'total_prod': producto['precio'] * cantidad
        }

        carrito.append(item)
        print("✅ Producto agregado al carrito.")

    if carrito:
        print("\n🛒 Productos en el carrito:")
        for prod in carrito:
            print(f"- {prod['marca']} {prod['modelo']} x{prod['cantidad']} = U$D {prod['total_prod']:.2f}")
    else:
        print("No se agregó ningún producto.")

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

def generar_compra(carrito, dni, lista_historial_ventas):
    '''
    Simula la finalizacion de la compra guardando el carrito en el json 'carts.json' y devolviendo el comprobante (Numero de venta)

    Input:
    - Carrito (Lista de diccionarios)
    - DNI

    Output:
    - Valor total
    '''
    timestamp = datetime.now().strftime('%d/%m/%Y')
    total = 0
    
    n_venta = generar_id(lista_historial_ventas, 'DNI')

    for prod in carrito:
        total += prod['total_prod']

    compra = {
        'n_venta': n_venta,
        'user': dni,
        'fecha': timestamp,
        'total': total,
        'productos': carrito
    }

    try:
        lista_ventas = importar_datos_json('DB/carts.json')
        lista_ventas.append(compra)
        cargar_datos_json('DB/carts.json', lista_ventas)

        return compra
    except Exception as err:
        print('No se pudo realizar la compra debido al siguiente error:\n{err}')
        registrar_error(err)

def menu_comprar_productos(dni, listado_productos):
    '''
    Genera el menu de compra de productos

    Input:
    - DNI
    - listado_productos: Lista de productos disponibles (diccionarios).

    Output:
    - Si la compra se confirma, guarda los datos en el historial y muestra el comprobante.
    '''
    carrito = generar_carrito(listado_productos)

    if carrito:
        total = calcular_total(carrito)
        print(f"\nTotal de la compra: U$D {total:.2f}")
        
        confirmar = input("¿Desea finalizar la compra? (S/N): ").lower()
        if confirmar == 's':
            venta = generar_compra(carrito, dni, ventas)
            print("\n=== Compra realizada con éxito ===")
            print(f"N° de venta : {venta['n_venta']}")
            print(f"Total: U$D {venta['total']:.2f}")
            print(f"Fecha: {venta['fecha']}")

            return venta
        else:
            print("Compra cancelada.")
            
    else:
        print("Fin del proceso de compra.")