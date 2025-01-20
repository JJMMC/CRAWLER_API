from querys_db import read_all_rows, colum_names



def table_to_dict(tabla = 'Coches'):
	result = read_all_rows(tabla)
	colum = colum_names(tabla)
	data = {}
	data[tabla] = []
	for item in result:
		data[tabla].append({
			colum[0]:item[0],
			colum[1]:item[1],
			colum[2]:item[2],
			colum[3]:item[3],
		})

	return data


