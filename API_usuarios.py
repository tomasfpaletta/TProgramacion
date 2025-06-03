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

def validar_correo(correo): # Uso de Expresion regular
    '''
    Valida mediante el uso de Expresiones Regulares - regEX que el correo ingresado cumple con el patron declarado
    - Contempla que tenga letras y simbolos
    - Contempla que pueda tener un sub dominio como -> .com.ar
    - No permite correos incompletos como -> correo.domino / correo.com

    Inputs:
    - Correo (string)

    Output:
    - True o False
    '''
    patron_correo = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    try:
        if re.match(patron_correo, correo):
            return True
        else:
            print('El correo es no cumple con los requisitos:\nEjemplo: micorreo@uade.edu.ar')
            return False
    except Exception as err:
        print(f'Ocurrio un error al intentar validar el correo -> correo_Valido()\n{err}')
        registrar_error(err)