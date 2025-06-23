import re
from json_handler import importar_datos_json, cargar_datos_json
from funciones_generales import registrar_error, actualizar_lista

lista_usuarios = importar_datos_json('DB/users.json')

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
    try:
        for usuario in usuarios:
            if usuario['DNI'] == input_dni:
                if usuario ['password'] == input_password:
                    return True
        return False
    except Exception as err:
        print(f'Ocurrio un error al intentar validar el login -> login_correcto()\n{err}')
        registrar_error(err)        

def get_user(dni, usuarios):
    '''
    Devuelve el usuario indicado.
    
    Inputs:
    - DNI (identificador unico del usuario)
    - Lista de usuarios

    Output:
    - Usuario buscado
    '''
    try:
        for usuario in usuarios:
            if usuario['DNI'] == dni:
                return usuario
                  
        print(f'No existe el usuario con el DNI -> {dni}')
        return {}
    except Exception as err:
        print(f'Ocurrio un error al intentar devolver el usuario -> get_user()\n{err}')
        registrar_error(err)

def crear_user(dni, nombre, apellido, email, password, preguntas_seguridad):
    '''
    Crea un nuevo usuario. Se genera el diccionario'
    
    Inputs:
    - DNI
    - Nombre
    - Apellido
    - Contraseña
    - Email
    - Preguntas de seguridad

    Output:
    - Nuevo usuario (diccionario)
    '''
    try:
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

        return nuevo_usuario
    except Exception as err:
        print(f'Ocurrio un error al intentar crear el usuario -> crear_user()\n{err}')
        registrar_error(err)

def mostrar_usuarios(usuarios):
    '''
    Muestra la lista de usuarios
    
    Inputs:
    - Usuarios (Lista de diccionarios)

    Output:
    - Nuevo usuario (diccionario)
    '''
    i = 1
    try:
        for usuario in usuarios:
            print(f'---> {i}')
            print(f'- DNI: {usuario["DNI"]}\n- Nombre: {usuario["nombre"]}\n- Apellido: {usuario["apellido"]}\n- Email: {"@".join(usuario["email"])}\n')
            print()
            i += 1
    except Exception as err:
        print(f'Ocurrio un error al intentar mostrar los usuarios -> mostrar_usuarios()\n{err}')
        registrar_error(err)

def validar_email(input_email, usuarios): # Uso de Expresion regular
    '''
    Valida mediante el uso de Expresiones Regulares - regEX que el correo ingresado cumple con el patron declarado
    - Contempla que tenga letras y simbolos
    - Contempla que pueda tener un sub dominio como -> .com.ar
    - No permite correos incompletos como -> correo.domino / correo.com

    Inputs:
    - Correo (string)
    - Usuarios (diccionario)

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

def validar_nombre_apellido(input):
    '''
    Valida que el input del nombre / apellido no contenga simbolos y 3 caracteres como minimo.

    Inputs:
    - input de nombre o apellido

    Output:
    - True o False
    '''
    requisitos = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]{3,}$"
    try:
        if re.fullmatch(requisitos, input):
            return True
        else:
            print(f'El nombre/apellido no puede poseer simbolos y debe tener al menos 3 letras.')
            return False
    except Exception as err:
        print(f'No se pudo validar el nombre/apellido -> validar_nombre_apellido()\n{err}')
        registrar_error(err) 

def gen_pregunta_seguridad():
    '''
    Genera un diccionario como pregunta de seguridad para futura recuperacion de contraseña.

    Inputs:
    - NA

    Output:
    - Pregunta de seguridad (Diccionario)
    '''
    seleccion = 0
    try:
        while seleccion != 1 and seleccion != 2:
            seleccion = int(input('Seleccione una pregunta de seguridad para recuperar la contraseña:\n1. Color favorito\n2. Nombre de mascota\nElija una opcion: '))
        
        if seleccion == 1:
            color = input('Indique su color favorito: ')

            preguntas = {
                "color_favorito": color
            }

            return preguntas
        elif seleccion == 2:
            nombre_mascota = input('Indique el nombre de su mascota: ')
            preguntas = {
                "nombre_mascota": nombre_mascota
            }

            return preguntas
        else:
            print('Se genero por default la pregunta de seguidad.\nColor favorito: azul')
            preguntas = {
                "color_favorito": "azul"
            }

            return preguntas
        
    except Exception as err:
        print(f'No se pudo generar una pregunta de seguridad preguntas_seguridad()\n{err}')
        registrar_error(err) 

def form_nuevo_usuario(usuarios):
    '''
    Genera el formulario de nuevo usuario y devuelve el nuevo usuario.

    Inputs:
    - Lista de usuarios (Lista de diccionarios)

    Output:
    - Lista de usuarios actualizada con el nuevo usuario
    '''
    try:
        print('Creacion de cuenta')
        input_dni = int(input('Ingrese su DNI:\n'))
        while validar_duplicacion_user(input_dni, 'DNI', usuarios) and len(str(input_dni)) != 8:
            input_dni = int(input('El DNI ingresado ya existe o no cumple los requisitos (8 numeros). Ingrese otro: '))

        input_email = input('ingrese su Email: ')
        while not validar_email(input_email, usuarios):
            print('El correo ya existe o no cumple con los requisitos (ej: micorreo@uade.edu.ar)')
            input_email = int(input('Ingrese otro: '))
        
        input_password = input('Ingrese una contraseña: ')
        input_validacion = input('Repita la contraseña: ')
        while not validar_password(input_password, input_validacion):
            input_password = input('Vuelva a ingresar una contraseña: ')
            input_validacion = input('Repita la contraseña: ')

        input_nombre = input('Ingrese su nombre: ').lower()
        while not validar_nombre_apellido(input_nombre):
            input_nombre = input('Vuelva a ingresar su nombre: ').lower()
        
        input_apellido = input('ingrese su apellido: ').lower()
        while not validar_nombre_apellido(input_apellido):
            input_apellido = input('Vuelva a ingresar su apellido: ').lower()

        pregunta_recuperacion = gen_pregunta_seguridad()

        nuevo_usuario = crear_user(input_dni, input_nombre, input_apellido, input_email, input_password, pregunta_recuperacion)

        return nuevo_usuario
    except Exception as err:
        print(f'Se produjo el siguiente error al generar el usuario:\n{err}')
        registrar_error(err)

def form_login(usuarios):
    '''
    Genera el formulario de login.

    Inputs:
    - Lista de usuarios (Lista de diccionarios)

    Output:
    - Usuario
    '''
    print('Ingrese sus credenciales')
    try:
        try:
            dni = int(input('DNI: '))
            password = input('Contraseña: ')
        except ValueError:
            dni = 0
            password = 0

        if login_correcto(dni, password, usuarios):
            print('Login exitoso.')
            usuario = get_user(dni, usuarios)
            return usuario
        else:
            print('Las credenciales ingresadas son incorrectas.\nSi la cuenta existe puede recuperar su contraseña en el menu inicial, de lo contrario debera crear una.')
            return {} # -> Significa que no hay nada. Por ende False
    except Exception as err:
        print(f'Se produjo el siguiente error al intentar ingresar en la cuenta form_login():\n{err}')
        registrar_error(err)

def actualizar_password(usuario, usuarios):
    '''
    Actualiza la contraseña del usuario.

    Inputs:
    - Usuario (actual)
    - Usuario (diccionario)

    Output:
    - Usuario con contraseña actualizada
    '''
    try:
        print(f"{'-'*30}")
        print(f'Cambio de contraseña')
        print(f"{'-'*30}")
        nueva_password = input('Ingrese una contraseña: ')
        validacion = input('Repita la contraseña: ')
        while not validar_password(nueva_password, validacion):
                nueva_password = input('Vuelva a ingresar una contraseña: ')
                validacion = input('Repita la contraseña: ')
        
        usuario['password'] = nueva_password

        usuarios_actualizada = actualizar_lista('DNI', usuario['DNI'], usuario, usuarios)
        cargar_datos_json('DB/users.json', usuarios_actualizada)
        print('---> Contraseña actualizada <---')
    except Exception as err:
        print(f'Se produjo el siguiente error al intentar actualizar la contraseña:\n{err}')
        registrar_error(err)


def recuperar_password(dni, usuarios):
    '''
    Solicita al usuario que ingrese la respuesta de la pregunta de seguridad.
    Si hace match entonces permite cambiar la contraseña.

    Inputs:
    - DNI del usuario
    - Lista de usuarios

    Output:
    - Usuario con contraseña actualizada
    '''
    try:
        usuario = get_user(dni, usuarios)
        if usuario:
            pregunta_seguridad = usuario['pregunta_seguirdad']
            pregunta = list(pregunta_seguridad.keys())[0]
            respuesta_correcta = pregunta_seguridad[pregunta]

            print(f'Indique la respuesta la pregunta de seguridad -> {pregunta}')

            respuesta = input('Respuesta: ').strip().lower()

            if respuesta_correcta == respuesta:
                nueva_password = actualizar_password(usuario)
                usuario['password'] = nueva_password
                print('---> Contraseña reestablecida <---')
                return usuario
            else:
                print('La respuesta ingresada es incorrecta.')
                return {}
    except Exception as err:
        print(f'Se produjo el siguiente error al intentar recuperar la contraseña:\n{err}')
        registrar_error(err)

def es_admin(usuario):
    '''
    Valida si el usuario es admin.

    Inputs:
    - Usuario (diccionario)

    Output:
    - True o False
    '''
    try:
        if usuario['admin'] == True:
            return True
        else:
            return False
    except Exception as err:
        print(f'Se produjo el siguiente error al intentar validar si el usuario es admin:\n{err}')
        registrar_error(err)

def menu_login(usuarios):
    '''
    Genera el menu de login/register.

    Inputs:
    - Lista de usuarios

    Output:
    - Menu de login
    - El usuario que se registro o logueo
    '''
    print(f"{'-'*30}")
    print(f'Menu de Login')
    print(f"{'-'*30}")

    volver_a_empezar = True
    while volver_a_empezar:
        try:
            opcion = int(input(f'1. Login\n2. Registrarse\n3. Recuperar contraseña\nElija una opcion: '))

            if opcion == 1:
                usuario = form_login(usuarios)
                if usuario:
                    return usuario
            elif opcion == 2:
                nuevo_usuario = form_nuevo_usuario(usuarios)
                if nuevo_usuario:
                    return nuevo_usuario
                else:
                    print("No se pudo registrar el usuario.")
            elif opcion == 3:
                print('Recuperación de contraseña.')
                try:
                    input_dni = int(input('Indique su DNI: '))
                    usuario_actualizado = recuperar_password(input_dni, usuarios)
                    if usuario_actualizado:
                        return usuario_actualizado
                except ValueError:
                    print("DNI inválido.")
            else:
                print("Opción inválida. Debe elegir entre 1 y 3.")
        except ValueError:
            print("Entrada inválida. Ingrese solo números.")
        except Exception as err:
            print(f"Se produjo un error inesperado:\n{err}")
            registrar_error(err)
