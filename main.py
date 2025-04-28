from API_productos import mostrar_productos, alta_producto, asignar_pid, editar_producto, obtener_indice, retornar_prod
"""Estructura principal del programa"""
listado_productos = [(1111, 'Samsung', 'S25 Ultra', 'Celular','Negro', 10, 1200),
                     (1112, 'Samsung', 'S25FE', 'Celular','Plata', 20, 500),
                     (1113, 'Apple', 'Iphone 16 Pro', 'Celular','Plata', 5, 1300),
                     (1114, 'Motorola', 'Edge 50', 'Celular','Gris', 40, 600),
                     (1115, 'Samsung', '65" 4K', 'TV','Negro', 100, 400)
                    ]

usuarios = [{"DNI": 40946880, 
             "nombre": "Nicolas", 
             "apellido": "Lazaro",
             "password": 12345,
             "admin": True,
             "historial_compras": []},
             {"DNI": 11111111, 
             "nombre": "Tomas", 
             "apellido": "Paletta",
             "password": 12345,
             "admin": True,
             "historial_compras": []}]

print('Bienvenido al E-Commerce')
eleccion_home = int(input('Elija la seccion a la que quiere ingresar:\n1. Productos\n2. Usuarios\n'))

while eleccion_home < 1 or eleccion_home > 3:
    eleccion_home = int(input('La opcion ingresada no es valida. Porfavor indique con numero:\n1. Usuarios\n2. Productos\n'))

if eleccion_home == 1:
    eleccion_productos = int(input('Indique que desea hacer:\n1. Visualizar productos\n2. Cargar nuevo producto\n3. Modificar producto\n4. Eliminar producto\n'))
    if eleccion_productos == 1:
        mostrar_productos(listado_productos)
    elif eleccion_productos == 2:
        pid = asignar_pid(listado_productos)
        alta_producto(listado_productos, pid)
    elif eleccion_productos == 3:
            # TODO Seguir 
        pid_encontrado = int(input('Indique el ID del producto a buscar: '))
        producto_empaquetado = retornar_prod(pid_encontrado, listado_productos)
        producto = producto_empaquetado[0]
        indice = obtener_indice(pid_encontrado, listado_productos)

        editar_producto(producto, indice, listado_productos)
    # elif eleccion_productos == 4:
# elif eleccion_home == 2:
#     eleccion_usuarios = int(input('Indique que desea hacer:\n1. Login\n2. Crear cuenta\n3. Ver usuarios\n'))