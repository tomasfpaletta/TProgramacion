def agregar_producto_carrito(lista_productos, usuario): # Lista de productos para mostrar en la API
    '''
    Agrega productos al carrito del cliente hasta que el cliente decida detener el proceso.

    Input:
    - Lista de productos (Lista de tuplas)
    Output:
    - Carrito del comprador (Matriz de productos)

    '''
    carrito_cliente = []
    total_final = 0

    respuesta = input()
    while respuesta.lower() == 's':
        id_producto = int(input('Ingrese el indice del producto a agregar al carrito: '))
        producto = lista_productos[id_producto]
        input_cantidad = int(input(f'Cantidad ? Existen {producto['stock']} unidades disponibles\n'))

        while input_cantidad > producto['stock'] or input_cantidad < 1:
            print('Cantidad indicada fuera de rango. Indique nuevamente')
            input_cantidad = int(input(f'Cantidad ? Existen {producto["stock"]} unidades disponibles\n'))
        
        producto['stock'] -= input_cantidad
        if producto['stock'] == 0:
            producto['disponible'] = False

        compra = {
            'marca': producto['marca'],
            'modelo': producto['modelo'],
            'color': producto['color'],    
            'cantidad': input_cantidad,
            'total': producto['precio'] * input_cantidad
        }

        carrito_cliente.append(compra)

        print(f'Producto agregado al carrito: {carrito_cliente}')
        print('desea agregar otro producto? (s/n)')
        respuesta = input()
    
    if len(carrito_cliente) > 0:
        print(f'Agregaste los siguientes productos: {carrito_cliente}')
    else:
        print('No se agrego ningun producto al carrito')
    
    for compra in carrito_cliente:
        total_final += compra['total']
        carrito_cliente.append()

    return carrito_cliente # Retornamos el carrito con el producto agregado
