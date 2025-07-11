from json_handler import importar_datos_json, cargar_datos_json
from funciones_generales import generar_id, registrar_error, limpiar_consola
import re

def centrar_con_metodo(texto, ancho):
    '''
    Centra un texto dentro de un ancho determinado.

    Input:
    - Cadena a centrar.
    - Cantidad total de caracteres del campo.

    Output:
    - Texto centrado como string.
    '''
    try:
        return texto.center(ancho)
    except Exception:
        print('No se pudo centrar el texto. Se imprime por default.')
        return texto

def mostrar_prod(producto):
    '''
    Muestra el producto de una manera mas legible y prolija

    Input:
    - Producto (Diccionario)

    Output:
    - Producto de forma mas legible
    '''
    try:
        print('-------------------------------------')
        print(f"Marca: {producto['marca'].capitalize()}")
        print(f"Modelo: {producto['modelo'].capitalize()}")
        print(f"Categoría: {producto['categoria'].capitalize()}")
        print(f"Color: {producto['color'].capitalize()}")
        print(f"Stock: {producto['stock']}")
        print(f"Precio: {producto['precio']}")
        print(f"Disponible: {'Sí' if producto['disponible'] else 'No'}")
    except Exception:
        print('No se pudo mostrar el producto.')


def mostrar_productos(productos):
    '''
    Muestra los productos en forma de tabla (filas y columnas).

    Input:
    - Lista de productos (Lista de diccionarios)

    Output:
    - Print de productos de forma legible
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

    try:
        ancho_total = sum(anchos.values()) + 9  # 8 columnas + bordes

        print("=" * ancho_total)
        print("|" + centrar_con_metodo("CATÁLOGO DE PRODUCTOS", ancho_total - 2) + "|")
        print("=" * ancho_total)

        mostrar_encabezado(anchos)
        print("-" * ancho_total)

        for producto in productos:
            print(formatear_fila(producto, anchos))

        print("=" * ancho_total)
    except Exception:
        print('No se pudo mostrar la lista de productos.')

def mostrar_encabezado(anchos):
    '''
    Muestra los encabezados de la tabla de productos con el ancho definido por campo.

    Input:
    - Diccionario que contiene el ancho de cada columna.

    Output:
    - Imprime los encabezados de cada columna.
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

    try:
        for campo in encabezados:
            fila += "|" + encabezados[campo].center(anchos[campo])
        fila += "|"
        print(fila)
    except Exception:
        print('No se logro generar los encabezados de las columnas.')


def formatear_fila(producto, anchos):
    '''
    Formatea los valores de un producto en una fila para la tabla de catálogo.

    Input:
    - Producto (Diccionario)
    - Anchos (Diccionario con las medidas de ancho)

    Output:
    - Devuelve un string que representa una fila de la tabla.
    '''
    try:
        valores = {
            'pid': str(producto['pid']),
            'marca': str(producto['marca'].capitalize()),
            'modelo': str(producto['modelo'].capitalize()),
            'categoria': str(producto['categoria'].capitalize()),
            'color': str(producto['color'].capitalize()),
            'stock': str(producto['stock']),
            'precio': f"{producto['precio']:.2f}",
            'disponible': 'Sí' if producto['disponible'] else 'No'
        }

        fila = ""
        for campo in ['pid', 'marca', 'modelo', 'categoria', 'color', 'stock', 'precio', 'disponible']:
            fila += "|" + valores[campo].center(anchos[campo])
        fila += "|"
        return fila
    except Exception:
        print('Error al intentar formater la fila del producto.')
        return producto

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
    try:
        return [prod for prod in productos if prod['pid'] == pid_buscado]
    except Exception as err:
        print(f'Ocurrio el siguiente error al intentar retornar el producto:\n{err}')
        registrar_error(err)
        return []


def seleccionar_producto(productos):
    '''
    Permite al usuario seleccionar un producto ingresando su PID.
    Se valida la existencia del producto en la lista.

    Input:
    - Productos (Lista de diccionarios)

    Output:
    - Producto (Diccionario)
    '''
    try:
        pid = int(input("Ingrese el PID del producto: "))
        prod = retornar_prod(pid, productos)
        if not prod:
            print("PID no encontrado.")
            return {}
        return prod[0] # Hacemos 'prod[0]' porque la funcion retornar_prod lo devuelve empaquetado, asi que seleccionamos el unico y primer indice.
    except ValueError:
        print(f'PID no encontrado -> ValueError al indicar PID del producto a agregar')
        return {}
    except Exception as err:
        print(f'Se produjo el siguiente error al intentar seleccionar el producto en la funcion -> seleccionar_prod():\n{err}')
        registrar_error(err)
        return {}

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
    try:
        for producto in lista_prods:
            if producto['pid'] == pid:
                producto['stock'] -= cantidad
                if producto['stock'] == 0:
                    producto['stock'] = 0
                    producto['disponible'] = False
                break
        return lista_prods
    except Exception as err:
        print(f'Ocurrio el siguiente error al intentar restar el stock del producto.\n{err}')
        print('Se devuelve la lista de productos sin los cambios de stock')
        registrar_error(err)
        return lista_prods 

def sumar_stock(cantidad, pid, lista_prods):
    '''
    Suma la cantidad de stock que se le resto al producto cuando se lo agrego al carrito.

    Input:
    - Cantidad de stock a sumar

    Output:
    - Lista de productos con el prod actualizado
    '''
    try:
        for producto in lista_prods:
            if producto['pid'] == pid:
                producto['stock'] += cantidad
                producto['disponible'] = True
                break
        return lista_prods
    except Exception as err:
        print(f'Ocurrio el siguiente error al intentar sumar el stock del producto.\n{err}')
        print('Se devuelve la lista de productos sin los cambios de stock')
        registrar_error(err)
        return lista_prods 


def validar_stock_precio(valor):
    '''
    Valida que el stock o el precio no excedan los limites

    Input:
    - Valor: el input

    Output:
    - True o False
    '''

    if 0 <= valor <= 100000:
        return True
    else:
        return False

def validar_input_alta_mod(texto):
    '''
    Valida que los inputs de Marca, Modelo, Categoria y Color, no sean cualquier  cosa.

    Input:
    - Texto a validar

    Output:
    - True o False
    '''

    patron = r"^[a-zA-Z0-9\s]{3,20}$"
    if re.fullmatch(patron, texto.strip()):
        return True
    else:
        limpiar_consola()
        print(f'Ingresaste un valores que no estan permitidos')
        print(f'Solo Letras y Numeros hasta 20 caracteres. Sin simbolos')
        return False 
        

def alta_producto(lista_productos):
    '''
    Genera un producto (Diccionario) y lo agrega a la lista 'lista_productos'.

    Input:
    - lista_productos (Lista de diccionarios)

    Output:
    - Devuelve la lista actualizada de productos con el nuevo prod.
    '''
    campo_invalido = True

    while campo_invalido:
        print('Alta de nuevo producto')
        marca = input('Marca del producto:\n').lower()
        modelo= input('Modelo del producto:\n').lower()
        categoria = input('Categoria del producto:\n').lower()
        color= input('Color del producto:\n').lower()
        if validar_input_alta_mod(marca) and validar_input_alta_mod(modelo) and validar_input_alta_mod(categoria) and validar_input_alta_mod(color):
            try:
                while campo_invalido:
                    try:
                        precio = float(input('Precio del producto:\n'))
                        stock = int(input('Stock del producto:\n'))

                        if validar_stock_precio(precio) and validar_stock_precio(stock):
                            campo_invalido = False
                        else:
                            print('Los valores ingresados superan los limites. Minimo: 0 | Maximo: 100.000')
                            continue
                    except ValueError:
                        print('Los campos de Precio y Stock solo aceptan valores numericos.')
                        continue


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

            except Exception as err:
                print(f'Ocurrio el siguiente error al intentar dar de alta el producto.\n{err}')
                print('Se devuelve la lista de productos sin los cambios')
                registrar_error(err)
                campo_invalido = False
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
    Función para obtener el índice en una lista en base a un identificador unico como puede ser el PID.

    Input:
    - PID (El id unico del producto)
    - Lista de diccionarios

    Output:
    - Si encuentra te devuelve la posicion (Indice)
    - Si no te devuelve -1
    '''
    try:
        for i, prod_dict in enumerate(lista):
            if prod_dict['pid'] == pid_buscado: 
                return i
        
        return -1
    except Exception as err:
        print(f'Ocurrio un error al intentar obtener el indice del producto:\n{err}')
        registrar_error(err)
        return -1

def editar_producto(prod_seleccionado, lista_productos):
    '''
    Edita los campos que se deseen hasta que el usuario rompa el bucle.
    
    Input:
    - prod_seleccionado: El diccionario del producto a editar.
    - indice_producto: El índice del producto para luego reemplazarlo en la lista de productos.
    - lista_productos (lista de diccionarios)

    Output:
    - Lista de productos actualizada con los cambios
    '''
    producto_final = prod_seleccionado.copy() 
    seguir_editando = True 
    
    try:
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

            campo_invalido = True
            while campo_invalido:
                if opcion == 1:
                    cambio = input('Ingrese la marca: ').lower()
                    if validar_input_alta_mod(cambio):
                        producto_final['marca'] = cambio
                        campo_invalido = False
                elif opcion == 2:
                    cambio = input('Ingrese el modelo: ').lower()
                    if validar_input_alta_mod(cambio):
                        producto_final['modelo'] = cambio
                        campo_invalido = False
                elif opcion == 3:
                    cambio = input('Ingrese la categoria: ').lower()
                    if validar_input_alta_mod(cambio):
                        producto_final['categoria'] = cambio
                        campo_invalido = False
                elif opcion == 4:
                    cambio = input('Ingrese el color: ').lower()
                    if validar_input_alta_mod(cambio):
                        producto_final['color'] = cambio
                        campo_invalido = False
                elif opcion == 5:
                    try:
                        cambio = int(input('Ingrese el stock: '))
                        while cambio < 0:
                            print('Solo se aceptan numeros positivos o 0')
                            cambio = int(input('Ingrese el stock: '))
                        if cambio == 0:
                            producto_final['disponible'] == False

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
                    resp_disponible = input('¿Está disponible? (S/N):\n').lower()
                    producto_final['disponible'] = True if resp_disponible == 's' else False
                elif opcion == 8:
                    seguir_editando = False
                    print('Edicion cancelada!')
                else:
                    print('La opcion ingresada no es valida. Vuelva a intentar.')
                    continue # Vuelve a pedir la opción

            if seguir_editando: # Solo pregunta si seguir editando si no se canceló
                print(f'\nAsí va quedando tu producto:')
                mostrar_prod(producto_final)
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
    except Exception as err:
        print(f'Ocurrio un error al intentar editar el producto:\n{err}')
        print('No se guardaron los cambios a la lista de productos ')
        registrar_error(err)
        return lista_productos

def buscar_productos(productos, criterio, valor):
    '''
    Busca productos en la lista. Devuelve productos cuyo campo 'criterio'
    contenga las letras (o subcadena) ingresadas en 'valor' para campos de texto.
    Para los campos numéricos ('pid', 'stock', 'precio'), busca coincidencias exactas.

    Input:
    - Lista de diccionarios de productos.
    - La clave del diccionario por la cual buscar (ej. "marca", "modelo", "categoria", "color", "pid", "stock", "precio").
    - Las letras (subcadena) o el valor numérico a buscar.

    Output:
    - Lista de diccionarios con los productos que coinciden con la búsqueda.
    '''
    resultados = []
    
    try:
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
    except Exception as err:
        print(f'Ocurrio un error al intentar editar el producto:\n{err}')
        print('No se guardaron los cambios a la lista de productos ')
        registrar_error(err)
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

def menu_busqueda_productos(productos):
    '''
    Muestra un menu para buscar productos por distintos campos (marca, modelo, etc).

    Input:
    - N/A

    Output:
    - Muestra en consola los productos filtrados o mensaje de no encontrados.
    '''
    print("\n=== MENÚ DE BÚSQUEDA DE PRODUCTOS ===")
    print("├─ 1. Buscar por marca")
    print("├─ 2. Buscar por modelo")
    print("├─ 3. Buscar por categoría")
    print("├─ 4. Buscar por color")
    print("└─ 5. Buscar por precio")

    opcion = input("Ingrese el número correspondiente a la búsqueda: ").strip()

    campos = {
        "1": "marca",
        "2": "modelo",
        "3": "categoria",
        "4": "color",
        "5": "precio"
    }
    try:
        if opcion in campos:
            valor = input(f"Ingrese el valor para buscar en {campos[opcion]}: ").strip()
            resultados = filtrar_productos(valor, productos, campos[opcion])

            if resultados:
                limpiar_consola()
                print("\n--- Resultados encontrados ---")
                mostrar_productos(resultados)
            else:
                print("No se encontraron productos con ese criterio.")
        else:
            print("Opción inválida. Intente nuevamente.")
    except Exception as err:
        print(f'Ocurrio un error al intentar mostrar el menu de busqueda de productos:\n{err}')
        registrar_error(err)

def filtrar_productos(valor_busqueda, lista_productos, key):
    '''
    Filtra productos de una lista comparando el valor del campo especificado con el valor de búsqueda.

    Inputs:
    - Texto que debe coincidir al inicio del campo especificado.
    - lista_productos (lista de diccionarios)
    - Key del diccionario sobre la que se aplicará el filtro.

    Output:
    - Lista de productos que cumplen el filtro.
    '''
    try:
        valor_busqueda = str(valor_busqueda).lower()
        productos_filtrados = list(filter(lambda p: str(p[key]).lower().startswith(valor_busqueda), lista_productos))
        return productos_filtrados
    except Exception as err:
        registrar_error(err)
        return lista_productos

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
    

