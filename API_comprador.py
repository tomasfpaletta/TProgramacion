productos = [(1, 'Samsung', 'S25 Ultra', 'Negro', 10, 1000), (2, 'Samsung', 'S25', 'Plata', 20, 700), (3, 'Samsung', 'S25FE', 'Light blue', 5, 500)]

# Mostrar lista de productos en la API del cliente. Esto va a mostarse como una matriz de .
def agregar_producto_carrito(): # Lista de productos para mostrar en la API
    '''Comprador accede al menu de productos, elige uno y lo agrega al carrito. El producto se agrega al carrito como una Lista.
    carrito = [[producto 1],[producto 2],[producto 3]]
    Lista de productos es una lista de tuplas, una vez que se muestra el usuario elige un producto y se trae la tupla. Esta tupla hay que convertila en lista para poder traerla al carrito.

    productos [(),(),()] TUPLA 
    carrito.append(producto[1]) -> No se puede, es una tupla. Entonces hay que usar una metodo para convertir la tupla de productos en lista y usar luego el carrito.append(producto[1]).
    metodo para convertir es list()
    '''
    carrito_cliente = []

    print('desea agregar algun producto a tu carrito? (s/n)')
    respuesta = input()
    while respuesta.lower() == 's':
        seleccion = input('Ingrese el indice del producto a agregar al carrito: ')
        carrito_cliente.append(list(productos[int(seleccion)])) # Convertimos la tupla en lista y la agregamos al carrito
        print(f'Producto agregado al carrito: {carrito_cliente}')
        print('desea agregar otro producto? (s/n)')
        respuesta = input()

    print(f'Agregaste los siguientes productos: {carrito_cliente}')

    return carrito_cliente # Retornamos el carrito con el producto agregado

def mostrar_productos():
    print('Lista de productos disponibles:')
    indice = -1
    for producto in productos:
        indice += 1
        producto_texto = f'{indice} {producto[1]} {producto[2]} {producto[3]}'
        partes = producto_texto.split(' ')
        
        print(f'{indice}. {partes[1]} -> Modelo: {partes[2]}, Color: {partes[3]}, Stock: {producto[4]}, Precio: ${producto[5]}')

mostrar_productos()
agregar_producto_carrito()

