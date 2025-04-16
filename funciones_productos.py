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

def cargar_produtos():
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


cargar_produtos()
eliminar_productos()
print(lista_productos)
    