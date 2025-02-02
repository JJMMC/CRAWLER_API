from bs4 import BeautifulSoup
import requests


def soup_generator(url):
	res = requests.get(url,timeout=10)
	content = res.text
	soup = BeautifulSoup(content, "html.parser")
	return soup

#Corrección de lista Categorias para importar nombres sin espacios en columnas de SQLite
def correc_list_spaces(lista_categorias):
    for i in lista_categorias:
        i = i.replace(",","")
        i = i.replace(" ", "")
        yield i

def request_categorias_and_main_urls(url = "https://www.rtrvalladolid.es/87-crawler"):
	soup = soup_generator(url)
	soup_categorias = soup.find("ul", class_="category-sub-menu").find_all("a")
	los_submenus = soup.find("ul", class_="category-sub-menu").find_all("a",class_="category-sub-link")
	soup_categorias = [url for url in soup_categorias if url not in los_submenus]
	categorias = [i.string for i in soup_categorias]
	categorias_corregidas =correc_list_spaces(categorias)
	main_urls = [i.get("href") for i in soup_categorias]
	final_zip = zip(categorias,main_urls,categorias_corregidas)
	return final_zip


# Función que dada la main url de la familia retorna list() de las url que descuelgan de ella para extraer los datos
def find_child_urls(url):
	for i in range (1,10):
		
		test_url = f"{url}?page={str(i)}" # formato de las urls de RTR para moverse entre páginas
		soup = soup_generator(test_url)
		vacio = soup.find(class_="page-content page-not-found") #Buscamos esta clase para encontrar la página sin datos
		
		if vacio == None:
			#total_paginas_url.append(test_url)
			yield test_url
			
		else:
			break			
		
	#Retorna list con urls de la catergoría YIELD


# Damos formato al precio para dejarlo como queremos	
def formating_price(price_list):
	formated_price = []
	for i in price_list:
		precio = i.text.replace("€","").replace(",",".").strip()
		if len(precio) > 6:
			precio = precio.replace(".","",1)
			formated_price.append(precio)
		else:
			formated_price.append(precio)
	return formated_price
	

# Func para obtener los datos de artículo y precio output: -> tuples, list [(a,b),(c,d)]
def get_items_price(url):	# Whe get the data from a single URL
	soup = soup_generator(url)
	items_list = [i.h2.string for i in soup.find_all("div", class_="product-description")]
	price_list = [i.string for i in soup.find_all(class_="price")]
	price_list = formating_price(price_list)
	category_list = []
	for i in range(len(price_list)):
		category_list.append(soup.title.string)

	item_price_list = [(i,v) for i,v in zip(items_list,price_list)]
	item_price_category_list = [(h,i,v) for h,i,v in zip(category_list, items_list,	price_list)]

	return item_price_category_list

#result = get_items_price("https://www.rtrvalladolid.es/134-llantas-crawler?page=2")
#print(result)

	





