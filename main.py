from API_productos import menu_busqueda_productos, ordenar_por_precio, mostrar_productos, alta_producto, asignar_pid, editar_producto, obtener_indice, retornar_prod, eliminar_producto, mostrar_logo
from API_usuarios import login_correcto, crear_user, mostrar_usuarios
from API_comprador import menu_comprar_productos
from json_handler import importar_datos_json

dni = "40946880"  # hasta que implementemos login

"""Estructura principal del programa"""
listado_productos = importar_datos_json('DB/prods.json')
listado_usuarios = importar_datos_json('DB/users.json')

mostrar_logo()
# Manejo de la elección inicial con try-except para evitar errores si no ingresa número
try:
    eleccion_home = int(input('=== Elija la seccion a la que quiere ingresar ===\n1. Productos\n2. Usuarios\n'))
except ValueError:
    print("Opción inválida. Ingrese un número.")
    eleccion_home = 0 # Valor para que entre en el bucle de validación

while eleccion_home < 1 or eleccion_home > 2:
    try:
        eleccion_home = int(input('La opcion ingresada no es valida. Por favor, indique con numero:\n1. Productos\n2. Usuarios\n'))
    except ValueError:
        print("Opción inválida. Ingrese un número.")
        eleccion_home = 0 # Valor para que siga en el bucle de validación

if eleccion_home == 1:
    seguir_menu_productos = True
    while seguir_menu_productos: # Este es el ÚNICO bucle principal del menú de productos
        eleccion_productos_str = input('=== Indique qué desea hacer ===\n1. Visualizar productos\n2. Cargar nuevo producto\n3. Comprar producto\n4. Modificar producto\n5. Eliminar producto\n6. Buscar producto\n7. Salir\n')
        
        try:
            eleccion_productos = int(eleccion_productos_str)
        except ValueError:
            print('Opción inválida. Por favor, ingrese un número.')
            continue # Vuelve al inicio del bucle para pedir la opción de nuevo

        if eleccion_productos == 1:    
            mostrar_productos(listado_productos)

            sub_eleccion = input("\n=== ¿Querés filtrar los productos? ===\nPresioná 1 para buscar, o cualquier otra tecla para salir: ")

            if sub_eleccion == "1":
                menu_busqueda_productos()
        elif eleccion_productos == 2:
            pid_random = asignar_pid(listado_productos)
            alta_producto(listado_productos, pid_random)
            print("Producto cargado exitosamente.")
            fin = input('Enter para terminar')
        elif eleccion_productos == 3:
            menu_comprar_productos(dni, listado_productos)
        elif eleccion_productos == 4:
            resp_editar = 1
            while resp_editar == 1:
                mostrar_productos(listado_productos)
                try:
                    input_pid_str = input('Indique el PID del producto a buscar (o -1 para salir): ')
                    input_pid = int(input_pid_str)
                except ValueError:
                    print("ID inválido. Ingrese un número.")
                    continue

                if input_pid == -1:
                    resp_editar = -1
                    break

                producto_empaquetado = retornar_prod(input_pid, listado_productos)

                # Si producto_empaquetado está vacío, significa que el PID no se encontró.
                while not producto_empaquetado:
                    try:
                        input_pid_str = input('No se encontró el PID. Ingrese otro (-1 para salir): ')
                        input_pid = int(input_pid_str)
                    except ValueError:
                        print("ID inválido. Ingrese un número.")
                        continue
                    if input_pid == -1:
                        resp_editar = -1
                        break
                    producto_empaquetado = retornar_prod(input_pid, listado_productos)

                if producto_empaquetado and resp_editar == 1:
                    producto = producto_empaquetado[0] # Esto te da el diccionario del producto
                    indice = obtener_indice(input_pid, listado_productos) # Obtiene el índice correcto
                    
                    lista_actualizada = editar_producto(producto, indice, listado_productos)

                    try:
                        resp_editar = int(input('¿Desea editar otro producto?\n1. SI\n2. NO\n'))
                    except ValueError:
                        print("Opción inválida. Por favor, ingrese 1 o 2.")
                        resp_editar = 2 
            
            print('Salió de la edición.')
            fin = input('Enter para terminar')
        elif eleccion_productos == 5:
            resp_eliminar = 1
            while resp_eliminar == 1:
                mostrar_productos(listado_productos)
                try:
                    pid_a_eliminar_str = input(f'Indique el PID del producto a eliminar (-1 para salir): ')
                    pid_a_eliminar = int(pid_a_eliminar_str)
                except ValueError:
                    print("ID inválido. Ingrese un número.")
                    continue

                if pid_a_eliminar == -1:
                    resp_eliminar = -1
                    break
                
                indice_a_eliminar = obtener_indice(pid_a_eliminar, listado_productos)

                if indice_a_eliminar != -1: 
                    eliminar_producto(indice_a_eliminar, listado_productos) # eliminar_producto ya imprime confirmación
                    try:
                        resp_eliminar = int(input('¿Desea eliminar otro producto?\n1. SI\n2. NO\n'))
                    except ValueError:
                        print("Opción inválida. Por favor, ingrese 1 o 2.")
                        resp_eliminar = 2 
                else:
                    print(f"No se encontró un producto con PID {pid_a_eliminar}.")
                    try:
                        resp_eliminar = int(input('¿Desea intentar eliminar otro producto?\n1. SI\n2. NO\n'))
                    except ValueError:
                        print("Opción inválida. Por favor, ingrese 1 o 2.")
                        resp_eliminar = 2
            
            print('Proceso para eliminar producto finalizado.')
            fin = input('Enter para terminar')
        elif eleccion_productos == 6: # Sección para buscar productos
           menu_busqueda_productos()

        elif eleccion_productos == 7: # Opción para salir del menú de productos
            seguir_menu_productos = False
            print("Saliendo del menú de productos.")
        else:
            print('Opción inválida. Por favor, intente de nuevo.')
elif eleccion_home == 2:
    seguir_menu_usuarios = True
    while seguir_menu_usuarios:
        eleccion_usuarios_str = input('Indique que desea hacer:\n1. Login\n2. Crear cuenta\n3. Ver usuarios\n4. Salir\n') # Agregué salir
        try:
            eleccion_usuarios = int(eleccion_usuarios_str)
        except ValueError:
            print('Opción inválida. Por favor, ingrese un número.')
            continue

        if eleccion_usuarios == 1:
            flag = True
            while flag:
                try:
                    input_dni = int(input('Ingrese su DNI:\n'))
                    input_password = int(input('Ingrese su contraseña:\n'))
                    if login_correcto(input_dni, input_password, listado_usuarios):
                        flag = False
                    else:
                        print('Contraseña y/o DNI incorrecto/s. Vuelva a intentarlo.')
                except ValueError:
                    print("DNI/Contraseña inválidos. Ingrese solo números.")
            print('Login Exitoso')
            fin = input('Enter para terminar')
            """
            elif eleccion_usuarios == 2:
            print('Crear cuenta')
            input_dni = int(input('Ingrese su DNI:\n'))
            while not (input_dni, listado_usuarios) and len(str(input_dni)) != 8:
                input_dni = int(input('El DNI ingresado ya existe o no cumple los requisitos(8 numeros), pruebe con otro:\n'))
            
            input_nombre = input('Ingrese su nombre:\n')
            input_apellido = input('ingrese su apellido:\n')
            input_email = input('ingrese su Email:\n').split('@')
            input_password = int(input('Ingrese una password (Solo numeros):\n'))

            crear_user(input_dni, input_nombre, input_apellido, input_email, input_password, listado_usuarios)
            print('Usuario creado exitosamente')
            print(f'El usuario quedo de esta manera:\n{listado_usuarios[-1]}')

            fin = input('Enter para terminar')
            """
        elif eleccion_usuarios == 3:
            mostrar_usuarios(listado_usuarios)
            fin = input('Enter para terminar')
        elif eleccion_usuarios == 4: # Opción para salir del menú de usuarios
            seguir_menu_usuarios = False
            print("Saliendo del menú de usuarios.")
        else:
            print('La opcion ingresada es incorrecta. Vuelva a intentar.')