import re
from funciones_generales import registrar_error

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


def crear_user(dni, nombre, apellido, email, password, preguntas_seguridad, usuarios):
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
        'email': email,
        'password': password,
        'admin': False,
        'historial_compras': [],
        'preguntas_seguridad': preguntas_seguridad
    }

    usuarios.append(nuevo_usuario)
    return usuarios


def mostrar_usuarios(usuarios):
    i = 1
    for usuario in usuarios:
        print(f'---> {i}')
        print(f'- DNI: {usuario["DNI"]}\n- Nombre: {usuario["nombre"]}\n- Apellido: {usuario["apellido"]}\n- Email: {"@".join(usuario["email"])}\n')
        print()
        i += 1

def correo_valido(correo): # Uso de Expresion regular
    '''
    Valida mediante el uso de Expresiones Regulares - regEX que el correo ingresado contiene al menos uno de los dominios validos.

    Inputs:
    - Correo (string)

    Output:
    - True o False
    '''
    correos_validos = r'.*@(gmail\.com|outlook\.com|hotmail\.com|yahoo\.com\.ar|uade\.edu\.ar)$'
    try:
        if re.match(correos_validos, correo):
            return True
        else:
            print('El correo es invalido.')
            return False
    except Exception as err:
        print(f'Ocurrio un error al intentar verificar el dominio del correo -> correo_Valido()\n{err}')
        registrar_error(err)