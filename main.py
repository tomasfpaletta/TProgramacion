from API_productos import menu_busqueda_productos, ordenar_por_precio, mostrar_productos, alta_producto, generar_id, editar_producto, obtener_indice, retornar_prod, eliminar_producto
from API_usuarios import login_correcto, crear_user, mostrar_usuarios, menu_login, es_admin
from API_comprador import menu_comprar_productos
from menu import mostrar_logo, gen_home
from json_handler import importar_datos_json

def main():
    gen_home()

if __name__ == main:
    main()