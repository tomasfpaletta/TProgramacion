import re
from funciones_generales import registrar_error

def validar_duplicacion_user(input, key, usuarios):
    '''
    Valida respaldando con la key pasada por parametro como el Email o DNI con el valor del input en algun usuario.
    Si devuelve True significa que ya existe un usuario que posee ese valor en la key indicada. 

    Inputs:
    - Input a validar
    - Key con el que se hara la validacion de existencia
    - Lista de diccionarios con los usuarios

    Output:
    - True o False
    '''
    try:
        for usuario in usuarios:
            if usuario[key] == input:
                return True
        
        return False
    except Exception as err:
        print(f'Se registro el siguiente error al intentar validar el input {key}:\n {err}')
        registrar_error(err)


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

def validar_email(input_email, usuarios): # Uso de Expresion regular
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
        if re.match(patron_correo, input_email) and not validar_duplicacion_user(input_email, 'email', usuarios):
            return True
        else:
            return False
    except Exception as err:
        print(f'Ocurrio un error al intentar validar el correo -> correo_valido()\n{err}')
        registrar_error(err)

def validar_password(input_password, comprobacion):
    '''
    Valida mediante el uso de Expresiones Regulares - regEX que la contraseña cumpla con los requisitos minimos.
    - 8 caracteres, un simbolo, una mayuscula y una minuscula.

    Inputs:
    - Contraseña nueva
    - Comprobacion de contraseña ("Repetir contraseña")

    Output:
    - True o False
    '''
    requisitos = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*()_+\-=\[\]{}|;:'\",.<>/?`~])(.{8,})$"
    try:
        if input_password != comprobacion:
            print('La contraseña no coincide.')
            return False
        
        if re.fullmatch(requisitos, input_password):
            return True
        else:
            print(f'La contraseña no cumple con los requisitos minimos:\n- Minimo 8 Caracteres\n- Al menos una minuscula\n- Al menos una mayuscula\n- Al menos un simbolo')
            return False
    except Exception as err:
        print(f'No se pudo validar la contraseña -> validar_password()\n{err}')
        registrar_error(err)      


def menu_nuevo_usuario(usuarios):
    try:
        print('Creacion de cuenta')
        input_dni = int(input('Ingrese su DNI:\n'))
        while validar_duplicacion_user(input_dni, 'DNI', usuarios) and len(str(input_dni)) != 8:
            input_dni = int(input('El DNI ingresado ya existe o no cumple los requisitos (8 numeros). Ingrese otro: '))

        input_email = input('ingrese su Email: ')
        while not validar_email(input_email, usuarios):
            print('El correo ya existe o no cumple con los requisitos (ej: micorreo@uade.edu.ar)')
            input_email = int(input('Ingrese otro: '))

        input_nombre = input('Ingrese su nombre: ')
        input_apellido = input('ingrese su apellido: ')
        input_password = input('Ingrese una contraseña: ')

        input_pregunta = input('')

        
    except Exception as err:
        print(f'Se produjo el siguiente error al generar el usuario:\n{err}')
        registrar_error(err)