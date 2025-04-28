def existe_dni(input_dni, usuarios):
    '''
    Valida si existe o no el DNI, iterando por los diferentes diccionarios (usuarios).

    Inputs:
    - DNI del input (menu)
    - Lista de diccionarios con los usuarios

    Output:
    - True o False
    '''
    for usuario in usuarios:
        if usuario['DNI'] == input_dni:
            return True
    
    return False

def login_correcto(input_dni, input_password, usuarios):
    '''
    Valida que la contraseña y el DNI existan sean correctos iterando por los diferentes diccionarios (usuarios)
    
    Inputs:
    - DNI del input (menu)
    - Contraseña del input (menu)
    - Lista de diccionarios con los usuarios

    Output:
    - True o False
    '''
    for usuario in usuarios:
        if usuario['DNI'] == input_dni:
            if usuario ['password'] == input_password:
                return True
    
    return False


def crear_user(dni, nombre, apellido, password, usuarios):
    '''
    Crea un nuevo usuario. Se genera el diccionario y se inserta en la lista 'usuarios'
    
    Inputs:
    - DNI del input (menu)
    - Nombre del input (menu)
    - Apellido del input (menu)
    - Contraseña del input (menu)
    - Lista de diccionarios con los usuarios

    Output:
    - Return de lista 'usuarios' con el nuevo usuario
    '''
    nuevo_usuario = {
        'DNI': dni,
        'nombre': nombre,
        'apellido': apellido,
        'password': password,
        'admin': False,
        'historial_compras': []
    }

    usuarios.append(nuevo_usuario)
    return usuarios


# Menu Login
# print('Bienvenido')
# respuesta_login = int(input('Ingrese una opcion con su numero:\n 1. Loguearse\n 2. Crear cuenta\n'))
# if respuesta_login == 1:
#     flag = True
#     while flag:
#         input_dni = int(input('Ingrese su DNI:\n'))
#         input_password = int(input('Ingrese su contraseña:\n'))
#         if login_correcto(input_dni, input_password, usuarios):
#             flag = False
#         else:
#             print('Contraseña y/o DNI incorrecto/s. Vuelva a intentarlo.')
#     print('Login Exitoso')
# elif respuesta_login == 2:
#     print('Crear cuenta')
#     input_dni = int(input('Ingrese su DNI:\n'))
#     while not existe_dni(input_dni, usuarios) and len(str(input_dni)) != 8:
#         input_dni = int(input('El DNI ingresado ya existe o no cumple los requisitos(8 numeros), pruebe con otro:\n'))
    
#     input_nombre = input('Ingrese su nombre:\n')
#     input_apellido = input('ingrese su apellido:\n')
#     input_password = int(input('Ingrese una password (Solo numeros):\n'))
#     crear_user(input_dni, input_nombre, input_apellido, input_password, usuarios)
#     print('Usuario creado exitosamente')
# else: 
#     respuesta_login = int(input('Ingrese una opcion con su numero:\n 1. Loguearse\n 2. Crear cuenta\n'))