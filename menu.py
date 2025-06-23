from funciones_generales import registrar_error, limpiar_consola
from json_handler import importar_datos_json
from API_productos import mostrar_productos, ordenar_por_precio, menu_busqueda_productos, menu_abm
from API_usuarios import es_admin, menu_login, actualizar_password
from API_comprador import menu_comprar_productos, seleccionar_producto
from API_ventas import historial_compras_usuario, menu_ventas

def mostrar_logo():
    print("===============================================================================")
    print("|                       Bienvenido al sistema CLI E-SHOP                       |")
    print("===============================================================================\n")

def gen_home():
    '''
    Genera el menu de inicio.

    Inputs:
    - N/A

    Output:
    - Menu de inicio
    '''
    seguir_menu_productos = True
    while seguir_menu_productos:
        try:
            productos = importar_datos_json('DB/prods.json')
            usuarios = importar_datos_json('DB/users.json')
            mostrar_logo()
            mostrar_productos(productos)

            print('Para acceder mas opciones debera loguearse o registrarse')
            try:
                acceder = input('Desea ingresar ? (S/N): ').lower()
            except ValueError:
                print('Solo se aceptan caracteres del tipo letra. ')

            if acceder == 's':
                limpiar_consola()
                usuario = menu_login(usuarios)
                if usuario:
                    if es_admin(usuario):
                        limpiar_consola()
                        gen_panel_admin(productos)
                    else:
                        limpiar_consola()
                        print(f"¡Bienvenido/a, {usuario['nombre'].capitalize()}!")
                        gen_menu_cliente(usuario, usuarios, productos)
                # print('No se ingreso a la cuenta.')
            elif acceder == 'n':
                print('Hasta pronto...')
                seguir_menu_productos = False
            else:
                limpiar_consola()
                print('Volviendo al inicio...')
                
        except Exception as err:
            print(f'Error al intentar generar el HOME en gen_home()\n{err}')
            registrar_error(err)

def gen_panel_admin(productos):
    '''
    Genera el panel de gestion para el admin/vendedor.

    Inputs:
    - N/A

    Output:
    - Menu de Admin/Vendedor
    '''
    seguir_menu_productos = True
    while seguir_menu_productos:
        try:
            print(f"{'='*30}")
            print(f'MENU ADMIN')
            print(f"{'-'*30}")
            print('Opciones disponibles:')
            print('├─ 1. Visualizar productos')
            print('├─ 2. Alta / Baja / Modificacion de productos')
            print('├─ 3. Ver productos sin stock')
            print('├─ 4. Buscar producto')
            print('├─ 5. Facturado y Cantidad de ventas')
            print('└─ 6. Salir')

            try:
                seleccion = int(input(f'--- Elija la seccion a la que quiere ingresar ---\n'))
                while seleccion < 1 or seleccion > 6:
                    seleccion = int(input(f'--- Opcion incorrecta. Indique nuevamente la seccion a la que quiere ingresar ---\n'))
            except ValueError:
                print('Solo se toman indices numericos como 1, 2 , etc.')

            if seleccion == 1:
                mostrar_productos(productos)
            elif seleccion == 2:
                limpiar_consola()
                menu_abm(productos)
            elif seleccion == 3:
                limpiar_consola()
                productos_sin_stock = list(filter(lambda prod: prod['stock'] == 0, productos))
                mostrar_productos(productos_sin_stock)
            elif seleccion == 4:
                try:
                    prod_sel = seleccionar_producto(productos)
                    if prod_sel:
                        print('====================================')
                        print(f"Marca: {prod_sel['marca'].capitalize()}")
                        print(f"Modelo: {prod_sel['modelo'].capitalize()}")
                        print(f"Categoría: {prod_sel['categoria'].capitalize()}")
                        print(f"Color: {prod_sel['color'].capitalize()}")
                        print(f"Stock: {prod_sel['stock']}")
                        print(f"Precio: {prod_sel['precio']}")
                        print(f"Disponible: {'Sí' if prod_sel['disponible'] else 'No'}") # Muestra estado de disponibilidad
                        print('====================================')
                except Exception:
                    print('No se encontro el producto.')
            elif seleccion == 5:
                limpiar_consola()
                menu_ventas()
            elif seleccion == 6:
                seguir_menu_productos = False
            else:
                limpiar_consola()
                continue

        except Exception as err:
            print(f'Error al intentar generar el PANEL ADMIN en gen_menu_admin()\n{err}')
            registrar_error(err)

def gen_menu_cliente(usuario, usuarios, productos):
    '''
    Genera el menu Cliente / Usuario  

    Inputs:
    - DNI
    - Lista de usuarios
    - Lista de productos

    Output:
    - Menu de Cliente / Usuario
    '''
    seguir_menu = True
    while seguir_menu:
        try:
            print('Opciones disponibles:')
            print('├─ 1. Visualizar productos')
            print('├─ 2. Ordenar productos por precio de Mayor a Menor')
            print('├─ 3. Ordenar productos por precio de Menor a Mayor')
            print('├─ 4. Filtrar productos')
            print('├─ 5. Comprar productos')
            print('├─ 6. Historial de compras')
            print('├─ 7. Cambiar contraseña')
            print('└─ 8. Salir')

            seleccion = 0
            while seleccion < 1 or seleccion > 7:
                try:
                    seleccion = int(input(f'--- Elija la seccion a la que quiere ingresar ---\n'))
                except ValueError:
                    print('Solo se toman indices numericos como 1, 2 , etc.')
                    continue
            
            if seleccion == 1:
                mostrar_productos(productos)
            elif seleccion == 2:
                lista_prod_ordenada = ordenar_por_precio(productos)
                mostrar_productos(lista_prod_ordenada[::-1])
            elif seleccion == 3:
                lista_prod_ordenada = ordenar_por_precio(productos)
                mostrar_productos(lista_prod_ordenada)
            elif seleccion == 4:
                limpiar_consola()
                menu_busqueda_productos()
            elif seleccion == 5:
                menu_comprar_productos(usuario['DNI'], productos)
            elif seleccion == 6:
                limpiar_consola()
                historial_compras_usuario(usuario['DNI'])
            elif seleccion == 7:
                actualizar_password(usuario, usuarios)
            elif seleccion == 8:
                seguir_menu = False
            else:
                limpiar_consola()
                continue

        except Exception as err:
            seguir_menu = False
            print(f'Error al intentar generar el MENU ADMIN en gen_menu_admin()\n{err}')
            registrar_error(err)
    
gen_home()