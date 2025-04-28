import random

def asignar_pid(productos):
    '''
    Genera un numero random el cual sera el Product ID (PID). Va de 1000 a 9999.
    Se valida ademas que no exista duplicados.

    Input:
    - Lista de productos

    Output:
    - Numero PID
    '''
    pid_random = random.randint(1000, 9999)
    pids_existentes = [prod[0] for prod in productos] # Guardo los PID que existen en una lista
    
    while pid_random in pids_existentes: # Si no existe lo agrego, sino vuelve a probar otro numero
        pid_random = random.randint(1000, 9999)
    
    return pid_random

def mostrar_productos(productos):
    '''
    Iteracion para mostrar todos los productos que se encuentran dentro de la lista 'Productos'.

    Input:
    - Lista de productos (Lista de tuplas)
    Output:
    - Print de productos

    '''
    for ID, marca, modelo, color, stock, precio in productos:
        print(f'ID: {ID} | Marca: {marca.upper()} | Modelo: {modelo.upper()} | Color: {color.upper()} | Stock: {stock} unidades | Precio: {precio} U$D |')

def retornar_prod(pid, productos):
    '''
    Devuelve el producto basandose en el PID que le pasemos de la lista de productos.
    Importante: Devuelve una lista y dentro el producto entero como una tupla debido a que la comprension de listas te hace eso
    
    Input:
    - PID del producto
    - Listado de productos

    Output:
    - Producto 'empaquetado' = [(producto)]
    '''
    return [prod for prod in productos if prod[0] == pid]


def alta_producto(lista_productos, pid):
    '''
    Genera un producto (Tupla) y lo agrega a la lista 'Productos.' 

    Input:
    - Productos (Lista de tuplas)
    - PID generado previamente con la funcion asignar_pid()

    Output:
    - Devuelve la lista actualizada de productos con el nuevo prod.
    '''
    print('Alta de nuevo producto')
    marca = input('Marca del producto:\n')
    modelo= input('Modelo del producto:\n')
    categoria = input('Categoria del producto:\n')
    color= input('Color del producto:\n')
    precio = int(input('Precio del producto:\n'))
    stock = int(input('Stock del producto:\n'))

    print(f'Producto {marca} dado de alta con exito!')

    nuevo_producto = (pid , marca, modelo, categoria, color, stock, precio)
    lista_productos.append(nuevo_producto)
    return lista_productos

def eliminar_producto(indice_prod, lista_productos):
    '''
    Elimina el producto de la lista productos con el indice que se le indique.

    Input:
    - Indice del producto
    - Lista de productos

    Output:
    - Lista de productos actualizada sin el producto
    '''
    del lista_productos[indice_prod]
    return lista_productos

def obtener_indice(id, lista):
    '''
    Funcion para obetener el indice en una lista en base a un Identificador unico como puede ser el PID.

    Input:
    - Recibe un ID, como el PID
    - Lista sobre la que iterar

    Output:
    - Si encuentra te devuelve la posicion (Indice)
    - Si no te devuelve -1
    '''
    i = 0
    for algo in lista:
        if algo[0] == id:
            return i
        i += 1
    
    return -1

# Modelo de datos [(1111, 'Samsung', 'S25 Ultra', 'Celular','Negro', 10, 1000), (1112, 'Samsung', 'S25', 'Celular','Negro', 10, 1000)]   
def editar_producto(prod_seleccionado, indice_producto, lista_productos): # El producto viene como [()] asi que previamente en una variable hay que sacar el prod. Ej: prod_selecciondo = producto[0]
    '''
    Permite editar los campos que se deseen hasta que el usuario rompa el bucle.
    
    Input:
    - Producto seleccionado viene de una variable que contiene el resultado de retornar_prod().
    - Indice del producto para luego reemplazarlo en la lista de productos.
    - Lista de productos.

    Output:
    - Lista de productos actualizada con los cambios

    '''
    producto_final = list(prod_seleccionado) # Las tuplas no son editables por eso la convierto a lista.
    seguir_editando = True # Basicamente un flag
    opcion = -1 # Lo dejamos ya seteado para que de entrada entre en el while. Lo mismo arriba.

    while seguir_editando:
        while opcion < 1 or opcion > 7:
            print('Que deseas editar?')
            print('Indicar con numero de indice')
            opcion = int(input('1. Marca\n2. Modelo\n3. Categoria\n4. Color\n5. Stock \n6. Precio\n7. ---> CANCELAR <---\n'))

            if opcion == 1:
                cambio = input('Ingrese la marca:\n')
                producto_final[1] = cambio
            elif opcion == 2:
                cambio = input('Ingrese el modelo:\n')
                producto_final[2] = cambio
            elif opcion == 3:
                cambio = input('Ingrese la categoria:\n')
                producto_final[3] = cambio
            elif opcion == 4:
                cambio = input('Ingrese el color:\n')
                producto_final[4] = cambio
            elif opcion == 5:
                cambio = int(input('Ingrese el stock:\n'))
                producto_final[5] = cambio
            elif opcion == 6:
                cambio = int(input('Ingrese el precio:\n'))
                producto_final[6] = cambio
            else:
                seguir_editando = False
                opcion = -1
                print('Edicion cancelada!')
        
        if opcion != 7:
            print(f'Asi va quedando tu producto:\n {producto_final}')
            respuesta = int(input('Desea seguir editando ?\nIndicar con indice 1 o 2:\n1. SI\n2. NO\n'))

            if respuesta == 2:
                seguir_editando = False
                print('Edicion Terminada')
            else:
                opcion = -1 # Reseteo esto porque sino no vuelve a preguntar los campos

    cargar = input('Cargar cambios ? S/N').lower()
    if cargar == 's':
        lista_productos[indice_producto] = tuple(producto_final)
        print('Cambios guardados')
        return lista_productos
    else:
        print('No se guardaron los cambios')
        return lista_productos