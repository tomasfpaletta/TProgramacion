import random

def asignar_pid(productos): # Recibe como argumento la lista de productos y otorga un PID dispobile para no haber duplicados.
    pid_random = random.randint(1000, 9999)
    pids_existentes = [prod[0] for prod in productos] # Guardo los PID que existen en una lista
    
    while pid_random in pids_existentes: # Si no existe lo agrego, sino vuelve a probar otro numero
        pid_random = random.randint(1000, 9999)
    
    return pid_random

# Niquito estuvo aqui 😊👍❤️😍👌👆

"""Funcion donde irian todas las funciones de productos"""
lista_productos = []

"Alta nuevos productos"
def alta_productos():
    """Funcion para dar de alta un nuevo producto"""
    print("Alta de nuevo producto")
    marca_producto = input("Marca del producto: ")
    modelo_producto = input("Modelo del producto: ")
    precio_producto = float(input("Precio del producto: "))
    stock_producto = int(input("Stock del producto: "))
    categoria_producto = input("Categoria del producto: ")

    #Agregar signo pesos al precio del producto.
    precio_producto_con_signo = "$" + str(precio_producto)

    print(f"Producto {marca_producto} dado de alta con exito!")

    lista_auxiliar = [marca_producto,modelo_producto, precio_producto_con_signo, stock_producto, categoria_producto]
    return lista_productos.append(lista_auxiliar)

def alta_produto():
    continuar = 's'
    while continuar == 's':
        alta_productos()
        continuar = input(("Desea dar de alta otro producto? (s/n): ")).lower()
        while continuar != 's' and continuar != 'n':
            continuar = input("Respuesta no valida. Desea dar de alta otro producto? (s/n): ")

def eliminar_productos():
    """Funcion para eliminar productos"""
    print("Eliminar producto de mi lista")
    print('¿Por qué campo querés buscar?')
    print('1. marca del producto')
    print('2. Modelo del producto')
    opcion = input('Ingrese una opción (1 o 2): ')

    while opcion != '1' and opcion != '2':
        opcion = input('Opción no válida. Ingrese una opción (1 o 2): ')
    
    campo = 0 if opcion == '1' else 1

    valor_busqueda = input('Ingrese el valor a buscar: ')

    encontrados = []
    for producto in lista_productos:
        if valor_busqueda.lower() in producto[campo].lower():
            encontrados.append(producto)
    
    if len(encontrados) == 0:
        print('No se encontraron productos con ese valor.')
        eliminar_productos()
    
    print("Productos encontrados:")
    for i in range(len(encontrados)):
        print(str(i+1) + ". " + str(encontrados[i]))
    
    confirmar = input('¿Desea eliminar alguno de estos productos? (s/n): ').lower()
    while confirmar != 's' and confirmar != 'n':
        confirmar = input('Respuesta no válida. ¿Desea eliminar alguno de estos productos? (s/n): ').lower()
    
    if confirmar == 's':
        for producto in encontrados:
            lista_productos.remove(producto)
        print('Productos eliminados con éxito.')
    else:
        print('No se eliminaron productos.')

def modificar_producto():
    """Función para modificar productos existentes sin usar enumerate()"""
    print("Modificar producto de mi lista")
    print('¿Por qué campo querés buscar?')
    print('1. Marca del producto')
    print('2. Modelo del producto')
    opcion = input('Ingrese una opción (1 o 2): ')

    while opcion != '1' and opcion != '2':
        opcion = input('Opción no válida. Ingrese una opción (1 o 2): ')
    
    campo = 0 if opcion == '1' else 1
    valor_busqueda = input('Ingrese el valor a buscar: ')

    encontrados = []
    i = 0
    while i < len(lista_productos):
        producto = lista_productos[i]
        if valor_busqueda.lower() in producto[campo].lower():
            encontrados.append([i, producto])  # Guardamos el índice y el producto
        i = i + 1

    if len(encontrados) == 0:
        print('No se encontraron productos con ese valor.')
        return  # Salimos de la función

    print("\nProductos encontrados:")
    j = 0
    while j < len(encontrados):
        print(str(j + 1) + ". " + str(encontrados[j][1]))
        j = j + 1

    eleccion = input('¿Cuál producto desea modificar? Ingrese el número (o "n" para cancelar): ')
    if eleccion.lower() == 'n':
        print('No se modificaron productos.')
        return
    
    while not eleccion.isdigit() or int(eleccion) < 1 or int(eleccion) > len(encontrados):
        eleccion = input('Opción no válida. Ingrese un número válido: ')

    elegido_idx = int(eleccion) - 1
    indice_original = encontrados[elegido_idx][0]
    producto_actual = lista_productos[indice_original]

    print("\nIngrese los nuevos datos del producto (deje en blanco para no modificar):")
    marca = input("Marca (actual: {}): ".format(producto_actual[0]))
    modelo = input("Modelo (actual: {}): ".format(producto_actual[1]))
    precio = input("Precio (actual: {}): ".format(producto_actual[2]))
    stock = input("Stock (actual: {}): ".format(producto_actual[3]))
    categoria = input("Categoría (actual: {}): ".format(producto_actual[4]))

    if marca != "":
        producto_actual[0] = marca
    if modelo != "":
        producto_actual[1] = modelo
    if precio != "":
        producto_actual[2] = float(precio)
    if stock != "":
        producto_actual[3] = int(stock)
    if categoria != "":
        producto_actual[4] = categoria

    lista_productos[indice_original] = producto_actual
    print("\nProducto modificado con éxito.")


alta_produto()
modificar_producto()
print(lista_productos)
    