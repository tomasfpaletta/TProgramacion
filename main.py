from API_productos import mostrar_productos, alta_producto, asignar_pid, editar_producto, obtener_indice, retornar_prod, eliminar_producto
from API_usuarios import existe_dni, login_correcto, crear_user, mostrar_usuarios

"""Estructura principal del programa"""
listado_productos = [(1111, 'Samsung', 'S25 Ultra', 'Celular','Negro', 10, 1200),
                     (1112, 'Samsung', 'S25FE', 'Celular','Plata', 20, 500),
                     (1113, 'Apple', 'Iphone 16 Pro', 'Celular','Plata', 5, 1300),
                     (1114, 'Motorola', 'Edge 50', 'Celular','Gris', 40, 600),
                     (1115, 'Samsung', '65" 4K', 'TV','Negro', 100, 400)
                    ]

#Diccionario
usuarios = [{"DNI": 40946880, 
             "nombre": "Nicolas", 
             "apellido": "Lazaro",
             "email": ['nlazaro', 'uade.edu.ar'], # Usuario y Dominio de mail por si quisieramos sacar estadisticas de cantidad mails etc.
             "password": 12345,
             "admin": True,
             "historial_compras": []},
             {"DNI": 44362800, 
             "nombre": "Tomas", 
             "apellido": "Paletta",
             "email": ['tpaletta', 'uade.edu.ar'],
             "password": 12345,
             "admin": True,
             "historial_compras": []}]

print('Bienvenido al E-Commerce')
eleccion_home = int(input('Elija la seccion a la que quiere ingresar:\n1. Productos\n2. Usuarios\n'))

while eleccion_home < 1 or eleccion_home > 2:
    eleccion_home = int(input('La opcion ingresada no es valida. Porfavor indique con numero:\n1. Usuarios\n2. Productos\n'))

if eleccion_home == 1:
    seguir_menu_productos = True
    while seguir_menu_productos:
        eleccion_productos = int(input('Indique que desea hacer:\n1. Visualizar productos\n2. Cargar nuevo producto\n3. Modificar producto\n4. Eliminar producto\n'))
        if eleccion_productos == 1:
            mostrar_productos(listado_productos)
            fin = input('Enter para terminar')
        elif eleccion_productos == 2:
            pid_random = asignar_pid(listado_productos)
            alta_producto(listado_productos, pid_random)
            print(listado_productos[-1])
            
            fin = input('Enter para terminar')
        elif eleccion_productos == 3:

            resp_editar = 1
            while resp_editar == 1:
                mostrar_productos(listado_productos)
                input_pid = int(input('Indique el ID del producto a buscar: '))
                producto_empaquetado = retornar_prod(input_pid, listado_productos)

                while not producto_empaquetado:
                    input_pid = int(input('No se encontro el PID. Ingrese otro. (-1 para salir): '))
                    if input_pid == -1:
                        resp_editar = -1
                        break

                if producto_empaquetado and resp_editar == 1:
                    producto = producto_empaquetado[0]
                    indice = obtener_indice(input_pid, listado_productos)
                    lista_actualizada = editar_producto(producto, indice, listado_productos)

                    print(f'Lista original:\n{listado_productos}')
                    print(f'Asi quedo su nueva lista de productos:\n{lista_actualizada}')

                    resp_editar = int(input('Desea editar otro producto?\n1. SI\n2. NO\n'))
            
            print('Salio de la edicion.')
            fin = input('Enter para terminar')
        elif eleccion_productos == 4:
            resp_eliminar = 1
            while resp_eliminar == 1:
                indice = int(input(f'Indique indice del producto a eliminar -> 0 a {len(listado_productos) - 1}(-1 para salir): '))
                if indice >= 0 and indice < len(listado_productos):
                    lista_actualizada = eliminar_producto(indice, listado_productos)
                    print(f'Asi quedo la lista de productos:\n{lista_actualizada}')
                    resp_eliminar = int(input('Desea eliminar otro producto?\n1. SI\n2. NO\n'))

                    if resp_eliminar != 1:
                        resp_eliminar = -1   
                elif indice == -1:
                    resp_eliminar = -1    
                else:
                    print('Indice invalido. Vuelva a intentar.')
            print('Proceso para eliminar producto finalizado.')
            fin = input('Enter para terminar')
elif eleccion_home == 2:
    seguir_menu_usuarios = True
    while seguir_menu_usuarios:
        eleccion_usuarios = int(input('Indique que desea hacer:\n1. Login\n2. Crear cuenta\n3. Ver usuarios\n'))
        if eleccion_usuarios == 1:
            flag = True
            while flag:
                input_dni = int(input('Ingrese su DNI:\n'))
                input_password = int(input('Ingrese su contraseña:\n'))
                if login_correcto(input_dni, input_password, usuarios):
                    flag = False
                else:
                    print('Contraseña y/o DNI incorrecto/s. Vuelva a intentarlo.')
            print('Login Exitoso')

            fin = input('Enter para terminar')
        elif eleccion_usuarios == 2:
            print('Crear cuenta')
            input_dni = int(input('Ingrese su DNI:\n'))
            while not existe_dni(input_dni, usuarios) and len(str(input_dni)) != 8:
                input_dni = int(input('El DNI ingresado ya existe o no cumple los requisitos(8 numeros), pruebe con otro:\n'))
            
            input_nombre = input('Ingrese su nombre:\n')
            input_apellido = input('ingrese su apellido:\n')
            input_email = input('ingrese su Email:\n').split('@')
            input_password = int(input('Ingrese una password (Solo numeros):\n'))

            crear_user(input_dni, input_nombre, input_apellido, input_email, input_password, usuarios)
            print('Usuario creado exitosamente')
            print(f'El usuario quedo de esta manera:\n{usuarios[-1]}')

            fin = input('Enter para terminar')
        elif eleccion_usuarios == 3:
            mostrar_usuarios(usuarios)
            fin = input('Enter para terminar')
        else:
            print('La opcion ingresada es incorrecta. Vuelva a intentar.')
