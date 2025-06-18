import random

def asignar_pid(productos):
    '''
    Genera un numero random el cual sera el Product ID (PID). Va de 1000 a 9999.
    Se valida ademas que no exista duplicados.

    Input:
    - Lista de productos (donde cada producto es un diccionario)

    Output:
    - Numero PID
    '''
    pid_random = random.randint(1000, 9999)
    # Accede al PID usando la clave 'pid' del diccionario
    pids_existentes = [prod['pid'] for prod in productos] 
    
    while pid_random in pids_existentes: 
        pid_random = random.randint(1000, 9999)
    
    return pid_random

def mostrar_logo():
    print("===============================================================================")
    print("|                       Bienvenido al sistema CLI E-SHOP                        |")
    print("===============================================================================\n")

# Función para centrar texto (si aún la quieres, aunque podrías hacerla inline)
def centrar_con_metodo(texto, ancho):
    return texto.center(ancho)

def mostrar_productos(productos):
    '''
    Muestra los productos en forma de tabla usando métodos de cadena como ljust y rjust.
    '''
    # Anchos por columna
    ancho_pid = 6
    ancho_marca = 12
    ancho_modelo = 18
    ancho_categoria = 13
    ancho_color = 10
    ancho_stock = 6
    ancho_precio = 12
    ancho_disponible = 12

    # Calculamos el ancho total para los bordes (ajustado para los | entre columnas)
    ancho_total = ancho_pid + ancho_marca + ancho_modelo + ancho_categoria + \
                  ancho_color + ancho_stock + ancho_precio + ancho_disponible + 9

    # Encabezado principal del catálogo
    print("=" * ancho_total)
    print("|" + centrar_con_metodo("CATÁLOGO DE PRODUCTOS", ancho_total - 2) + "|")
    print("=" * ancho_total)

    # Encabezado de tabla
    header_line = (
        "|" + "PID".center(ancho_pid) +
        "|" + "MARCA".center(ancho_marca) +
        "|" + "MODELO".center(ancho_modelo) +
        "|" + "CATEGORÍA".center(ancho_categoria) +
        "|" + "COLOR".center(ancho_color) +
        "|" + "STOCK".center(ancho_stock) + 
        "|" + "PRECIO (U$D)".center(ancho_precio) + 
        "|" + "DISPONIBLE".center(ancho_disponible) +
        "|"
    )
    print(header_line)
    print("-" * ancho_total)

    # Filas de datos
    for producto in productos:
        pid_str = str(producto.get('pid', 'N/A'))
        marca_str = str(producto.get('marca', 'N/A'))
        modelo_str = str(producto.get('modelo', 'N/A'))
        categoria_str = str(producto.get('categoria', 'N/A'))
        color_str = str(producto.get('color', 'N/A'))
        stock_str = str(producto.get('stock', 'N/A'))
        precio_str = f"{producto.get('precio', 0):.2f}"
        disponible_str = 'Sí' if producto.get('disponible', False) else 'No'

        fila = (
            "|" + pid_str.center(ancho_pid) +
            "|" + marca_str.center(ancho_marca) +
            "|" + modelo_str.center(ancho_modelo) +
            "|" + categoria_str.center(ancho_categoria) +
            "|" + color_str.center(ancho_color) +
            "|" + stock_str.center(ancho_stock) +
            "|" + precio_str.center(ancho_precio) +
            "|" + disponible_str.center(ancho_disponible) +
            "|"
        )
        print(fila)

    print("=" * ancho_total)

def retornar_prod(pid_buscado, productos):
    '''
    Devuelve el producto basandose en el PID que le pasemos de la lista de productos.
    Devuelve una lista con el diccionario del producto si se encuentra.

    Input:
    - pid_buscado: El PID del producto a buscar.
    - productos: Listado de diccionarios de productos.

    Output:
    - Producto 'empaquetado' = [{producto}] o [] si no se encuentra.
    '''
    # CORREGIDO: Accede al PID usando la clave 'pid' del diccionario
    return [prod for prod in productos if prod['pid'] == pid_buscado]

def alta_producto(lista_productos, pid):
    '''
    Genera un producto (Diccionario) y lo agrega a la lista 'lista_productos'.

    Input:
    - lista_productos (Lista de diccionarios)
    - PID generado previamente con la funcion asignar_pid()

    Output:
    - Devuelve la lista actualizada de productos con el nuevo prod.
    '''
    print('Alta de nuevo producto')
    marca = input('Marca del producto:\n')
    modelo= input('Modelo del producto:\n')
    categoria = input('Categoria del producto:\n')
    color= input('Color del producto:\n')
    # CORREGIDO: Asegurarse de convertir a float o int
    precio = float(input('Precio del producto:\n'))
    stock = int(input('Stock del producto:\n'))
    disponible = True

    print(f'Producto {marca} dado de alta con exito!')

    # CORREGIDO: Crear un diccionario en lugar de una tupla
    nuevo_producto = {
        "pid": pid,
        "marca": marca,
        "modelo": modelo,
        "categoria": categoria,
        "color": color,
        "stock": stock,
        "precio": precio,
        "disponible": disponible
    }
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
    # Esta función ya estaba bien, solo agregué un mensaje de confirmación.
    if 0 <= indice_prod < len(lista_productos):
        del lista_productos[indice_prod]
        print(f"Producto en índice {indice_prod} eliminado.")
    else:
        print("Índice de eliminación inválido.")
    return lista_productos

def obtener_indice(pid_buscado, lista):
    '''
    Función para obtener el índice en una lista en base a un Identificador unico como puede ser el PID.

    Input:
    - pid_buscado: Recibe un PID.
    - lista: Lista sobre la que iterar (debe ser de diccionarios).

    Output:
    - Si encuentra te devuelve la posicion (Indice)
    - Si no te devuelve -1
    '''
    # CORREGIDO: Itera sobre diccionarios y accede por clave 'pid'
    for i, prod_dict in enumerate(lista):
        if prod_dict['pid'] == pid_buscado: 
            return i
    
    return -1

def editar_producto(prod_seleccionado, indice_producto, lista_productos):
    '''
    Permite editar los campos que se deseen hasta que el usuario rompa el bucle.
    
    Input:
    - prod_seleccionado: El diccionario del producto a editar.
    - indice_producto: El índice del producto para luego reemplazarlo en la lista de productos.
    - lista_productos: La lista de productos.

    Output:
    - Lista de productos actualizada con los cambios
    '''
    # CORREGIDO: 'prod_seleccionado' ya es un diccionario. Hacemos una copia para trabajar.
    producto_final = prod_seleccionado.copy() 
    seguir_editando = True 

    while seguir_editando:
        print('====================================')
        print(f"Editando producto con PID: {producto_final['pid']}")
        print(f"Marca: {producto_final['marca']}")
        print(f"Modelo: {producto_final['modelo']}")
        print(f"Categoría: {producto_final['categoria']}")
        print(f"Color: {producto_final['color']}")
        print(f"Stock: {producto_final['stock']}")
        print(f"Precio: {producto_final['precio']}")
        print(f"Disponible: {'Sí' if producto_final['disponible'] else 'No'}") # Muestra estado de disponibilidad
        print('====================================')
        
        print('\n¿Qué deseas editar?')
        print('Indicar con número de opción')
        print('1. Marca')
        print('2. Modelo')
        print('3. Categoria')
        print('4. Color')
        print('5. Stock ')
        print('6. Precio')
        print('7. Disponibilidad') # Nueva opción para editar disponibilidad
        print('8. ---> CANCELAR <---')
        
        try:
            opcion = int(input('Ingrese su opción: '))
        except ValueError:
            print("Opción inválida. Por favor, ingrese un número.")
            continue # Vuelve al inicio del buble para pedir la opción de nuevo

        if opcion == 1:
            cambio = input('Ingrese la marca:\n')
            producto_final['marca'] = cambio
        elif opcion == 2:
            cambio = input('Ingrese el modelo:\n')
            producto_final['modelo'] = cambio
        elif opcion == 3:
            cambio = input('Ingrese la categoria:\n')
            producto_final['categoria'] = cambio
        elif opcion == 4:
            cambio = input('Ingrese el color:\n')
            producto_final['color'] = cambio
        elif opcion == 5:
            try:
                cambio = int(input('Ingrese el stock:\n'))
                producto_final['stock'] = cambio
            except ValueError:
                print("Stock inválido. Ingrese un número entero.")
        elif opcion == 6:
            try:
                cambio = float(input('Ingrese el precio:\n')) # Precio puede ser decimal
                producto_final['precio'] = cambio
            except ValueError:
                print("Precio inválido. Ingrese un número.")
        elif opcion == 7: # Manejo de Disponibilidad
            resp_disponible = input('¿Está disponible? (s/n):\n').lower()
            producto_final['disponible'] = True if resp_disponible == 's' else False
        elif opcion == 8:
            seguir_editando = False
            print('Edicion cancelada!')
        else:
            print('La opcion ingresada no es valida. Vuelva a intentar.')
            continue # Vuelve a pedir la opción

        if seguir_editando: # Solo pregunta si seguir editando si no se canceló
            print(f'\nAsí va quedando tu producto:\n {producto_final}')
            try:
                respuesta = int(input('Desea seguir editando ?\nIndicar con indice 1 o 2:\n1. SI\n2. NO\n'))
                if respuesta == 2:
                    seguir_editando = False
                    print('Edicion Terminada')
                elif respuesta != 1: 
                    print("Opción inválida. Continuando edición.")
            except ValueError:
                print("Respuesta inválida. Continuando edición.")

    cargar = input('Cargar cambios ? S/N').lower()
    if cargar == 's':
        lista_productos[indice_producto] = producto_final # Reemplaza el diccionario
        print('Cambios guardados')
        return lista_productos
    else:
        print('No se guardaron los cambios')
        return lista_productos
    
def buscar_productos(productos, criterio, valor):
    '''
    Busca productos en la lista. Devuelve productos cuyo campo 'criterio'
    contenga las letras (o subcadena) ingresadas en 'valor' para campos de texto.
    Para campos numéricos ('pid', 'stock', 'precio'), busca coincidencias exactas.
    La búsqueda en texto es insensible a mayúsculas/minúsculas.

    Input:
    - productos: Lista de diccionarios de productos.
    - criterio: La clave del diccionario por la cual buscar (ej. "marca", "modelo", "categoria", "color", "pid", "stock", "precio").
    - valor: Las letras (subcadena) o el valor numérico a buscar.

    Output:
    - Una lista de diccionarios con los productos que coinciden con la búsqueda.
    '''
    resultados = []
    
    # Manejo de criterios de búsqueda numéricos vs. texto
    if criterio in ['pid', 'stock', 'precio']:
        try:
            # Para campos numéricos, convertimos el valor de búsqueda al tipo adecuado
            if criterio == 'precio':
                valor_busqueda_num = float(valor)
            else: # 'pid' o 'stock'
                valor_busqueda_num = int(valor)

            for producto in productos:
                # Búsqueda exacta para PID, Stock y Precio
                if criterio in producto and producto[criterio] == valor_busqueda_num:
                    resultados.append(producto)
        except ValueError:
            # Si el valor ingresado no es convertible al tipo numérico esperado, no hay coincidencias válidas.
            pass 
    else: # Criterios de texto (marca, modelo, categoria, color)
        valor_busqueda_lower = str(valor).lower() # Convertir valor de búsqueda a minúsculas
        for producto in productos:
            # Asegurarse de que el campo existe y es una cadena antes de intentar la búsqueda parcial
            if criterio in producto and isinstance(producto[criterio], str):
                if valor_busqueda_lower in str(producto[criterio]).lower(): # Búsqueda parcial (contiene)
                    resultados.append(producto)
    
    return resultados