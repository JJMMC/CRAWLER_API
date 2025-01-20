import os
import time

def number_of_files():
	lst = os.listdir("database/") # your directory path
	number_files = len(lst)
	return number_files

def list_of_dbs():
	lst = os.listdir("database/")
	lst_filtered = [i for i in lst if i[0]!="."] #Filter the OS .files
	return lst_filtered



def path_of_file(path):
	
	path = f"database/{path}"
	print(path)
	lst = os.path.abspath(path)
	print(lst)
	path =""

	
def date_of_files(path):
		
	# Both the variables would contain time
	# elapsed since EPOCH in float
	ti_c = os.path.getctime(path)
	ti_m = os.path.getmtime(path)
	
	# Converting the time in seconds to a timestamp
	c_ti = time.ctime(ti_c)
	m_ti = time.ctime(ti_m)
	
	print(f"The file located at the path {path} 	was created at {c_ti} and was last modified at {m_ti}")

