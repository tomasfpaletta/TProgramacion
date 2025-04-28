import random
from buscar_productos import retornar_prod, mostrar_productos

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

lista_productos = []

'Alta nuevos productos'
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
    categoria = input('Categoria del producto:\n')
    marca = input('Marca del producto:\n')
    modelo= input('Modelo del producto:\n')
    precio = int(input('Precio del producto:\n'))
    stock = int(input('Stock del producto:\n'))

    print(f'Producto {marca} dado de alta con exito!')

    nuevo_producto = (pid , marca, modelo, precio, stock, categoria)
    lista_productos.append(nuevo_producto)
    return lista_productos

# TODO Esto Lo podemos hacer en el menu directamente
# '''Sirve para hacer un bucle y dar de alta varios productos. ''' 
# def alta_produto(): 
#     continuar = 's'
#     while continuar == 's':
#         alta_productos()
#         continuar = input(('Desea dar de alta otro producto? (s/n): ')).lower()
#         while continuar != 's' and continuar != 'n':
#             continuar = input('Respuesta no valida. Desea dar de alta otro producto? (s/n): ')

def eliminar_producto(producto, lista_productos):
    '''
    Elimina el producto de la lista productos con el producto que se le pase (El retornar_prod() le pasa el producto)

    Input:
    - producto = retornar_prod()
    - Lista de productos

    Output:
    - Lista de productos actualizada sin el producto
    '''
    lista_productos.remove(producto)
    return lista_productos

# Boiler [(1111, 'Samsung', 'S25 Ultra', 'Celular','Negro', 10, 1000)]   
def editar_producto(prod_seleccionado, lista_productos): # El producto viene como [()] asi que previamente en una variable hay que sacar el prod. Ej: prod_selecciondo = producto[0]
    '''
    Se edita el producto que le pasemos como argumento de la lista de productos
    '''
    producto_editable = list(prod_seleccionado) # Las tuplas no son editables por eso la convierto a lista.
    seguir_editando = True # Basicamente un flag
    opcion = 1 # Lo dejamos ya seteado para que de entrada este en el while. Lo mismo arriba.

    while seguir_editando:
        while opcion < 1 or opcion > 7:
            print('Que deseas editar?')
            print('Indicar con numero de indice')
            opcion = int(input('1. Marca\n2. Modelo\n3. Categoria\n4. Color\n5. Stock \n6. Precio\n 7. ---> CANCELAR <---'))

            if opcion == 1:
                cambio = input('Ingrese la marca:\n')
                producto_editable[1] = cambio
            elif opcion == 2:
                cambio = input('Ingrese el modelo:\n')
                producto_editable[2] = cambio
            elif opcion == 3:
                cambio = input('Ingrese la categoria:\n')
                producto_editable[3] = cambio
            elif opcion == 4:
                cambio = input('Ingrese el color:\n')
                producto_editable[4] = cambio
            elif opcion == 5:
                cambio = int(input('Ingrese el stock:\n'))
                producto_editable[5] = cambio
            elif opcion == 6:
                cambio = int(input('Ingrese el precio:\n'))
                producto_editable[6] = cambio
            else:
                seguir_editando = False
                opcion = -1
                print('Edicion cancelada!')
        
        print(f'Asi quedo tu producto:\n {producto_editable}')
        respuesta = input('Desea seguir editando ?\nIndicar con indice 1 o 2:\n1. SI\n2. NO\n')

        if respuesta == 2:
            seguir_editando = False
            print('Edicion Terminada')

def modificar_producto(productos):
    '''
    Modifica un producto existente buscando por su ID.
    '''
    mostrar_productos(productos) 

    pid = int(input('Ingrese el ID del producto a modificar: '))
    producto_encontrado = retornar_prod(pid, productos)

    if not producto_encontrado:
        print('No se encuentra el producto.')
        return
    
    print('\nProducto encontrado:')
    mostrar_productos(producto_encontrado)

    producto_actual = producto_encontrado[0]  # Como retornar_prod devuelve una lista, tomamos el primer elemento
    indice = productos.index(producto_actual)  # Buscamos la posición en la lista

    print('\nIngrese los nuevos datos del producto (deje en blanco para no modificar):')
    nueva_marca = input('Marca (actual: {}): '.format(producto_actual[1]))
    nuevo_modelo = input('Modelo (actual: {}): '.format(producto_actual[2]))
    nuevo_color = input('Color (actual: {}): '.format(producto_actual[3]))
    nuevo_stock = input('Stock (actual: {}): '.format(producto_actual[4]))
    nuevo_precio = input('Precio (actual: {}): '.format(producto_actual[5]))

    # Creamos una nueva tupla con los cambios aplicados
    nueva_tupla = (
        producto_actual[0],
        nueva_marca if nueva_marca != '' else producto_actual[1],
        nuevo_modelo if nuevo_modelo != '' else producto_actual[2],
        nuevo_color if nuevo_color != '' else producto_actual[3],
        int(nuevo_stock) if nuevo_stock != '' else producto_actual[4],
        float(nuevo_precio) if nuevo_precio != '' else producto_actual[5]
    )

    productos[indice] = nueva_tupla
    print('\nProducto modificado con éxito.')  
    
alta_producto()
modificar_producto()
print(lista_productos)
    