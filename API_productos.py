import random
from json_handler import importar_datos_json, cargar_datos_json
from funciones_generales import generar_id, registrar_error, actualizar_lista, limpiar_consola
from API_comprador import seleccionar_producto
"""Estructura principal del programa"""
listado_productos = importar_datos_json('DB/prods.json')
listado_usuarios = importar_datos_json('DB/users.json')

def centrar_con_metodo(texto, ancho):
    '''
    Centra un texto dentro de un ancho determinado.

    Input:
    - cadena a centrar.
    - cantidad total de caracteres del campo.

    Output:
    - Texto centrado como string.
    '''
    return texto.center(ancho)

def mostrar_productos(productos):
    '''
    Muestra los productos en forma de tabla.

    Input:
    - diccionario con la información de un producto.
    '''
    anchos = {
        'pid': 6,
        'marca': 12,
        'modelo': 18,
        'categoria': 13,
        'color': 10,
        'stock': 6,
        'precio': 12,
        'disponible': 12
    }

    ancho_total = sum(anchos.values()) + 9  # 8 columnas + bordes

    print("=" * ancho_total)
    print("|" + centrar_con_metodo("CATÁLOGO DE PRODUCTOS", ancho_total - 2) + "|")
    print("=" * ancho_total)

    mostrar_encabezado(anchos)
    print("-" * ancho_total)

    for producto in productos:
        print(formatear_fila(producto, anchos))

    print("=" * ancho_total)

def mostrar_encabezado(anchos):
    '''
    Muestra los encabezados de la tabla de productos con el ancho definido por campo.

    Input:
    - diccionario que contiene el ancho de cada columna.

    Output:
    - Imprime en consola la fila de encabezados.
    '''
    encabezados = {
        'pid': "PID",
        'marca': "MARCA",
        'modelo': "MODELO",
        'categoria': "CATEGORÍA",
        'color': "COLOR",
        'stock': "STOCK",
        'precio': "PRECIO (U$D)",
        'disponible': "DISPONIBLE"
    }

    fila = ""
    for campo in encabezados:
        fila += "|" + encabezados[campo].center(anchos[campo])
    fila += "|"
    print(fila)


def formatear_fila(producto, anchos):
    '''
    Formatea los valores de un producto en una fila para la tabla de catálogo.

    Input:
    - diccionario con la información de un producto.
    - diccionario con los anchos de cada columna.

    Output:
    - Devuelve un string que representa una fila de la tabla.
    '''
    valores = {
        'pid': str(producto['pid']),
        'marca': str(producto['marca']),
        'modelo': str(producto['modelo']),
        'categoria': str(producto['categoria']),
        'color': str(producto['color']),
        'stock': str(producto['stock']),
        'precio': f"{producto['precio']:.2f}",
        'disponible': 'Sí' if producto['disponible'] else 'No'
    }

    fila = ""
    for campo in ['pid', 'marca', 'modelo', 'categoria', 'color', 'stock', 'precio', 'disponible']:
        fila += "|" + valores[campo].center(anchos[campo])
    fila += "|"
    return fila

def retornar_prod(pid_buscado, productos):
    '''
    Devuelve el producto basandose en el PID que le pasemos de la lista de productos.
    Devuelve una lista con el diccionario del producto si se encuentra.

    Input:
    - El PID del producto a buscar.
    - Listado de diccionarios de productos.

    Output:
    - Producto 'empaquetado' = [{producto}] o [] si no se encuentra.
    '''
    return [prod for prod in productos if prod['pid'] == pid_buscado]

def restar_stock(cantidad, pid, lista_prods):
    '''
    Reduce la cantidad de stock, si llega a 0 el producto pasa a estar deshabilitado.

    Input:
    - Cantidad de stock a restar
    - El PID del producto a buscar
    - Lista de productos (Lista de diccionarios)

    Output:
    - Lista de productos con el prod actualizado
    '''
    for producto in lista_prods:
        if producto['pid'] == pid:
            producto['stock'] -= cantidad
            if producto['stock'] == 0:
                producto['stock'] = 0
                producto['disponible'] = False
            break
    return lista_prods      

def sumar_stock(cantidad, pid, lista_prods):
    '''
    Esta funcion esta pensada para devolver la cantidad de stock que se le resto al producto mas que nada.

    Input:
    - Cantidad de stock a sumar

    Output:
    - Lista de productos con el prod actualizado
    '''
    for producto in lista_prods:
        if producto['pid'] == pid:
            producto['stock'] += cantidad
            producto['disponible'] = True
            break
    return lista_prods

def alta_producto(lista_productos): #Stock valueError
    '''
    Genera un producto (Diccionario) y lo agrega a la lista 'lista_productos'.

    Input:
    - lista_productos (Lista de diccionarios)

    Output:
    - Devuelve la lista actualizada de productos con el nuevo prod.
    '''
    print('Alta de nuevo producto')
    marca = input('Marca del producto:\n')
    modelo= input('Modelo del producto:\n')
    categoria = input('Categoria del producto:\n')
    color= input('Color del producto:\n')
    precio = float(input('Precio del producto:\n'))
    stock = int(input('Stock del producto:\n'))
    disponible = True

    print(f'Producto {marca} dado de alta con exito!')

    pid = generar_id(lista_productos, 'pid')

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
    cargar_datos_json('DB/prods.json', lista_productos)
    return lista_productos

def eliminar_producto(pid, lista_productos):
    '''
    Elimina el producto que se pase como argumento de la lista productos.

    Input:
    - Producto (Diccionario)
    - Lista de productos (Lista de diccionarios)

    Output:
    - Lista de productos actualizada sin el producto
    '''
    try:
        for prod in lista_productos:
            if prod['pid'] == pid:
                prod['disponible'] = False
                prod['stock'] = 0
                break
        print('Producto eliminado')
        return lista_productos
    except Exception as err:
        print(f'Se produjo el siguiente error al intentar eliminar el producto de la lista de productos -> historial_compras_usuario():\n{err}')
        registrar_error(err)

def obtener_indice(pid_buscado, lista):
    '''
    Función para obtener el índice en una lista en base a un Identificador unico como puede ser el PID.

    Input:
    - pid_buscado: Recibe un PID.
    - Lista sobre la que iterar (debe ser de diccionarios).

    Output:
    - Si encuentra te devuelve la posicion (Indice)
    - Si no te devuelve -1
    '''
    # CORREGIDO: Itera sobre diccionarios y accede por clave 'pid'
    for i, prod_dict in enumerate(lista):
        if prod_dict['pid'] == pid_buscado: 
            return i
    
    return -1

def editar_producto(prod_seleccionado, lista_productos):
    '''
    Permite editar los campos que se deseen hasta que el usuario rompa el bucle.
    
    Input:
    - prod_seleccionado: El diccionario del producto a editar.
    - indice_producto: El índice del producto para luego reemplazarlo en la lista de productos.
    - lista_productos (lista de diccionarios)

    Output:
    - Lista de productos actualizada con los cambios
    '''
    producto_final = prod_seleccionado.copy() 
    seguir_editando = True 
    indice_producto = obtener_indice(prod_seleccionado['pid'], lista_productos)

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
        print('├─ 1. Marca')
        print('├─ 2. Modelo')
        print('├─ 3. Categoria')
        print('├─ 4. Color')
        print('├─ 5. Stock ')
        print('├─ 6. Precio')
        print('├─ 7. Disponibilidad') # Nueva opción para editar disponibilidad
        print('└─ 8. Salir')
        
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
                respuesta = input('Desea seguir editando ? (S/N): ').lower()
            except ValueError:
                print("Respuesta inválida. Continuando edición.")

            if respuesta == 's':
                continue
            elif respuesta == 'n': 
                seguir_editando = False
                print('Edicion Terminada')
            else:
                print("Opción inválida.")

    try:
        cargar = input('Cargar cambios ? S/N\n').lower()
    except ValueError:
        print("Solo se aceptan las letras -> S o N")

    if cargar == 's':
        lista_productos[indice_producto] = producto_final # Reemplaza el diccionario
        cargar_datos_json('DB/prods.json', lista_productos)
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
    - Lista de diccionarios de productos.
    - La clave del diccionario por la cual buscar (ej. "marca", "modelo", "categoria", "color", "pid", "stock", "precio").
    - Las letras (subcadena) o el valor numérico a buscar.

    Output:
    - Una lista de diccionarios con los productos que coinciden con la búsqueda.
    '''
    resultados = []
    
    # Manejo de criterios de búsqueda numéricos, texto
    if criterio in ['pid', 'stock', 'precio']:
        try:
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
            if criterio in producto and isinstance(producto[criterio], str):
                if valor_busqueda_lower in str(producto[criterio]).lower(): # Búsqueda parcial (contiene)
                    resultados.append(producto)
    
    return resultados

def menu_abm():
    '''
    Genera el menu para la alta/baja/modificacion de productos.

    Input:
    - Productos (Lista de diccionarios)

    Output:
    - Menu para la alta/baja/modificacion de productos.
    '''
    flag = True
    print(f"{'-'*30}")
    print(f'Alta / Baja / Modificacion de productos')
    print(f"{'-'*30}")

    while flag:
        try:
            productos = importar_datos_json('DB/prods.json')
            print('Opciones disponibles:')
            print('├─ 1. Visualizar productos')
            print('├─ 2. Alta')
            print('├─ 3. Baja')
            print('├─ 4. Modificacion')
            print('└─ 5. Salir')
            seleccion = int(input(f'--- Elija la seccion a la que quiere ingresar ---\n'))

            if seleccion == 1:
                mostrar_productos(productos)
            elif seleccion == 2:
                alta_producto(productos)
            elif seleccion == 3:
                prod_sel = seleccionar_producto(productos)
                productos = eliminar_producto(prod_sel['pid'], productos)
                cargar_datos_json('DB/prods.json', productos)
            elif seleccion == 4:
                prod_sel = seleccionar_producto(productos)
                editar_producto(prod_sel, productos) 
            elif seleccion == 5:
                flag = False
            else:
                print('Opcion ingresada invalida.')
                continue
        except ValueError:
            print('Solo se aceptan caracteres numericos.')
            continue
        except Exception as err:
            print(f'Error al intentar generar menu de ABM en menu_abm()\n{err}')
            registrar_error(err)

def menu_busqueda_productos():
    '''
    Muestra un menu para buscar productos por distintos campos (marca, modelo, etc).

    Input:
    - N/A

    Output:
    - Muestra en consola los productos filtrados o mensaje de no encontrados.
    '''
    print("\n=== MENÚ DE BÚSQUEDA DE PRODUCTOS ===")
    print("1. Buscar por marca")
    print("2. Buscar por modelo")
    print("3. Buscar por categoría")
    print("4. Buscar por color")
    print("5. Buscar por precio")

    opcion = input("Ingrese el número correspondiente a la búsqueda: ").strip()

    campos = {
        "1": "marca",
        "2": "modelo",
        "3": "categoria",
        "4": "color",
        "5": "precio"
    }

    if opcion in campos:
        valor = input(f"Ingrese el valor para buscar en {campos[opcion]}: ").strip()
        resultados = filtrar_productos(valor, listado_productos, campos[opcion])

        if resultados:
            print("\n--- Resultados encontrados ---")
            mostrar_productos(resultados)
        else:
            print("No se encontraron productos con ese criterio.")
    else:
        print("Opción inválida. Intente nuevamente.")

def filtrar_productos(valor_busqueda, lista_productos, campo):
    '''
    Filtra productos de una lista comparando el valor del campo especificado con el valor de búsqueda.

    Inputs:
    - texto que debe coincidir al inicio del campo especificado.
    - lista_productos (lista de diccionarios)
    - clave del diccionario sobre la que se aplicará el filtro.

    Output:
    - Lista de productos que cumplen el filtro.
    '''
    valor_busqueda = str(valor_busqueda).lower()
    productos_filtrados = list(filter(lambda p: str(p[campo]).lower().startswith(valor_busqueda), lista_productos))
    return productos_filtrados

def ordenar_por_precio(lista_productos):
    '''
    Ordena los productos de la lista_productos de Menor a Mayor.

    Inputs:
    - Lista de productos (Lista de diccionarios)

    Output:
    - Lista de productos ordenada de Menor a Mayor (Lista de diccionarios)
    '''
    try:
        productos = lista_productos.copy()
        ordenados = []
        while productos: # Voy quitando productos de la copia de la lista productos hasta que queda vacia para saber que termino
            # Encuentro el índice del producto de precio mínimo
            min_idx = 0
            for j in range(1, len(productos)):
                if productos[j]["precio"] < productos[min_idx]["precio"]:
                    min_idx = j
            # Lo extraigo y lo agrego a la lista ordenada
            ordenados.append(productos.pop(min_idx))
        
        return ordenados
    except Exception as err:
        print(f'Error al intentar ordenar la lista de productos por precio en ordenar_por_precio()\n{err}')
        registrar_error(err)
    

