from archivos import list_of_dbs


def mostrar_menu(opciones):
    print('Seleccione una opción:')
    for clave in sorted(opciones):
        print(f' {clave}) {opciones[clave][0]}')


def leer_opcion(opciones):
    while (a := input('Opción: ')) not in opciones:
        print('Opción incorrecta, vuelva a intentarlo.')
    return a


def ejecutar_opcion(opcion, opciones):
    opciones[opcion][1]()


def generar_menu(opciones, opcion_salida):
    opcion = None
    while opcion != opcion_salida:
        mostrar_menu(opciones)
        opcion = leer_opcion(opciones)
        ejecutar_opcion(opcion, opciones)
        print()

### Programa de Menus:
def menu_principal():
	opciones = {
		'1': ('Editar BD', menu_editar),
		'2': ('Consultar BD', menu_consultar),
		'3': ('Comparar BD', menu_comparar),
		'4': ('Salir', salir)
		}

	generar_menu(opciones, '4')


def menu_editar():
	print('Has elegido la opción 1')
	print('Editar BD')
	opciones = {
		'1': ('Borrar BD', 'borrar_db'),
		'2': ('Descargar nueva BD', 'descargar_nueva_db'),
		'3': ('Listas de BD', 'listas_de_db'),
		'4': ('Salir', salir)
		}
	
	generar_menu(opciones, '4')

def selec_db():
    print("\nEstos son las bases de datos disponibles: \n")
    dbs = list_of_dbs()
    numbers_list = [str(i+1) for i in range(len(dbs))]
    menu_list = zip(dbs,numbers_list)
    db_dict = {num:database for database,num in menu_list}
    for num,database in db_dict.items():
         print(f"{num}.- {database}")
    entrada = input("Elige la BD")
    print(db_dict[entrada])
    return db_dict[entrada]

   
selec_db()

def menu_consultar():
	print('Has elegido la opción 2')
	print('Consultar BD')
	opciones = {
		'1': ('Consultar una tabla de BD', 'menu_consultar_por_tabla'),
		'2': ('Consultar una BD completa', 'menu_consultar_por_db'),
		'3': ('Atras', salir)
		}

	generar_menu(opciones, '4')

	
def menu_comparar():
	print('Has elegido la opción 3')
	print('Comparar BD')

def salir():
    print('Saliendo')


# if __name__ == '__main__':
#     menu_principal() 
