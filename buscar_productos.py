def mostrar_productos(productos):
    '''
    Iteracion para mostrar todos los productos que se encuentran dentro de la lista 'Productos'.

    Input:
    - Lista de productos (Lista de tuplas)
    Output:
    - Print de productos

    '''
    for ID, marca, modelo, color, stock, precio in productos:
        print(f'ID: {ID} | Marca: {marca.upper()} | Modelo: {modelo.upper()} | Color: {color.upper()} | Stock: {stock} unidades | Precio: {precio} U$D |')

def retornar_prod(pid, productos): 
    '''
    Devulve la mostrando la lista [()] y no solo la tupla. Si no encuentra nada devuelve []
    '''
    return [prod for prod in productos if prod[0] == pid]

productos = [(1111, 'Samsung', 'S25 Ultra', 'Negro', 10, 1000), (1112, 'Samsung', 'S25', 'Plata', 20, 700), (1113, 'Samsung', 'S25FE', 'Light blue', 5, 500)]

pid = int(input('Ingrese el ID del producto a buscar: '))

producto_encontrado = retornar_prod(pid, productos)
if producto_encontrado:
    print(f'ID: {producto_encontrado[0][0]} |\n Marca: {producto_encontrado[0][1].upper()} |\n Modelo: {producto_encontrado[0][2].upper()} |\n Color: {producto_encontrado[0][3].upper()} |\n Stock: {producto_encontrado[0][4]} unidades |\n Precio: {producto_encontrado[0][5]} U$D |')
else:
    print('No se encuentra el producto')


