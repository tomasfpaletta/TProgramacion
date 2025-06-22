from funciones_generales import registrar_error, limpiar_consola
from json_handler import importar_datos_json
from API_productos import mostrar_productos, ordenar_por_precio
from API_usuarios import es_admin, menu_login, actualizar_password
from API_comprador import menu_comprar_productos
from API_ventas import historial_compras_usuario

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
                    gen_panel_admin()
                else:
                    limpiar_consola()
                    print(f"¡Bienvenido/a, {usuario['nombre'].capitalize()}!")
                    gen_menu_cliente(usuario, usuarios, productos)
            # print('No se ingreso a la cuenta.')
        else:
            limpiar_consola()
            print('Volviendo al inicio...')
    except Exception as err:
        print(f'Error al intentar generar el HOME en gen_home()\n{err}')
        registrar_error(err)

def gen_panel_admin():
    '''
    Genera el panel de gestion para el admin/vendedor.

    Inputs:
    - N/A

    Output:
    - Menu de Admin/Vendedor
    '''
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
            while seleccion < 1 or seleccion > 5:
                seleccion = int(input(f'--- Opcion incorrecta. Indique nuevamente la seccion a la que quiere ingresar ---\n'))
        except ValueError:
            print('Solo se toman indices numericos como 1, 2 , etc.')

        if seleccion == 1:
            print()
        if seleccion == 2:
            print()
        if seleccion == 3:
            print()
        if seleccion == 4:
            print()
        if seleccion == 5:
            print()
        if seleccion == 6:
            print()
    except Exception as err:
        print(f'Error al intentar generar el PANEL ADMIN en gen_menu_admin()\n{err}')
        registrar_error(err)

def gen_menu_cliente(usuario, usuarios, lista_prod):
    '''
    Genera el menu Cliente / Usuario  

    Inputs:
    - DNI

    Output:
    - Menu de Cliente / Usuario
    '''
    try:
        print('Opciones disponibles:')
        print('├─ 1. Visualizar productos')
        print('├─ 2. Ordenar productos por precio de Mayor a Menor')
        print('├─ 3. Ordenar productos por precio de Menor a Mayor')
        print('├─ 4. Comprar productos')
        print('├─ 5. Historial de compras')
        print('├─ 6. Cambiar contraseña')
        print('└─ 7. Salir')

        seleccion = 0
        while seleccion < 1 or seleccion > 6:
            try:
                seleccion = int(input(f'--- Elija la seccion a la que quiere ingresar ---\n'))
            except ValueError:
                print('Solo se toman indices numericos como 1, 2 , etc.')
                continue

        if seleccion == 1:
            limpiar_consola()
            mostrar_productos(lista_prod)
        elif seleccion == 2:
            limpiar_consola()
            lista_prod_ordenada = ordenar_por_precio(lista_prod)
            mostrar_productos(lista_prod_ordenada[::-1])
        elif seleccion == 3:
            limpiar_consola()
            lista_prod_ordenada = ordenar_por_precio(lista_prod)
            mostrar_productos(lista_prod_ordenada)
        elif seleccion == 4:
            limpiar_consola()
            menu_comprar_productos(usuario['DNI'], lista_prod)
        elif seleccion == 5:
            limpiar_consola()
            historial_compras_usuario(usuario['DNI'])
        elif seleccion == 6:
            # limpiar_consola()
            actualizar_password(usuario, usuarios)
    except Exception as err:
        print(f'Error al intentar generar el MENU ADMIN en gen_menu_admin()\n{err}')
        registrar_error(err)


gen_home()