def agregar_producto_carrito(lista_productos): # Lista de productos para mostrar en la API
    '''
    Agrega productos al carrito del cliente hasta que el cliente decida detener el proceso.

    Input:
    - Lista de productos (Lista de tuplas)
    Output:
    - Carrito del comprador (Matriz de productos)

    '''
    carrito_cliente = []

    print('desea agregar algun producto a tu carrito? (s/n)')
    respuesta = input()
    while respuesta.lower() == 's':
        seleccion = input('Ingrese el indice del producto a agregar al carrito: ')
        carrito_cliente.append(list(lista_productos[int(seleccion)])) # Convertimos la tupla en lista y la agregamos al carrito
        print(f'Producto agregado al carrito: {carrito_cliente}')
        print('desea agregar otro producto? (s/n)')
        respuesta = input()

    print(f'Agregaste los siguientes productos: {carrito_cliente}')

    return carrito_cliente # Retornamos el carrito con el producto agregado

