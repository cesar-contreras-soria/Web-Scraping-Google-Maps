
import os
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_experimental_option('prefs', {
        "download.prompt_for_download": False,
        "download.default_directory" : r"C:\Users\CESAR\Desktop\GitHub",
        "savefile.default_directory": r"C:\Users\CESAR\Desktop\GitHub"})
chromedriver =  r'C:\Program Files\Chromedriver\chromedriver.exe'
os.environ["webdriver.chrome.driver"] = chromedriver

driver = webdriver.Chrome(chromedriver, chrome_options=options)

#Excel de ejemplo
base_importada = pd.read_excel(io=r"C:\Users\CESAR\Desktop\GitHub\Ejemplo.xlsx")
vector_tiempo = []

#Pagina web
driver.get('https://www.google.com/maps/@-12.1831424,-76.9589248,12z')
time.sleep(12)

#Boton ¿Como llegar?
driver.find_element('id','hArJGc').click()
time.sleep(8)

#Medio de transporte en particular, pero se pueden escoger otros incluso hacer un loop
driver.find_element('xpath','/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[2]/div/div/div/div[2]/button/img').click()
time.sleep(6)

#Ubicaciones. Se hace distinto el origen porque marca la ubicacion de la maquina.
driver.find_element('xpath','/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[2]/div[1]/div/input').clear()
#Limpiar lugar de origen
driver.find_element('xpath','/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[2]/div[1]/div/input').send_keys("-12.132799, -76.939699")
#Limpiar lugar de destino
driver.find_element('xpath','/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[2]/div[2]/div[1]/div/input').send_keys("-12.216028, -76.919786")

#Buscar
driver.find_element('xpath','/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[2]/div[2]/button[1]').click()
time.sleep(8)

#Tiempo de salida
driver.find_element('xpath','/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/span/div/div/div/div[2]').click()
time.sleep(6)
driver.find_element('xpath','/html/body/div[7]/div[2]').click()

#Escoger hora de ejemplo. Notar que div[23] equivale a 11 am
driver.find_element('xpath','/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/span[1]/input').clear()
driver.find_element('xpath','/html/body/div[8]/div[23]').click()
time.sleep(6)

#Escoger fecha de ejemplo.
driver.find_element('xpath','/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/span[2]/span[1]').click()
while True:
	driver.find_element('xpath','/html/body/div[9]/table/thead/tr/td[1]').click()
	fecha = driver.find_element('xpath','/html/body/div[9]/table/thead/tr/td[2]').text
	if fecha=='agosto de 2017':
		break

#Seleccionar cada observacion de la base
for observacion in range(len(base_importada)):
	#Limpiar
	driver.find_element('xpath','/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[2]/div[1]/div/input').clear()
	driver.find_element('xpath','/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[2]/div[2]/div[1]/div/input').clear()

	#Lugar de origen
	x_ori = base_importada.loc[[observacion],['origen_x']]
	x_ori = x_ori.values.tolist()
	x_ori = str(x_ori)
	x_ori = x_ori.replace("[[","").replace("]]","")

	y_ori = base_importada.loc[[observacion],['origen_y']]
	y_ori = y_ori.values.tolist()
	y_ori = str(y_ori)
	y_ori = y_ori.replace("[[","").replace("]]","")
	driver.find_element('xpath','/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[2]/div[1]/div/input').send_keys(str(y_ori)+" "+str(x_ori))

	#Lugar de destino
	x_des = base_importada.loc[[observacion],['destino_x']]
	x_des = x_des.values.tolist()
	x_des = str(x_des)
	x_des = x_des.replace("[[","").replace("]]","")

	y_des = base_importada.loc[[observacion],['destino_y']]
	y_des = y_des.values.tolist()
	y_des = str(y_des)
	y_des = y_des.replace("[[","").replace("]]","")
	driver.find_element('xpath','/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[2]/div[2]/div[1]/div/input').send_keys(str(y_des)+" "+str(x_des))

	#Buscar
	time.sleep(2)
	driver.find_element('xpath','/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[2]/div[2]/button[1]').click()
	time.sleep(6)
	localizacion = driver.find_element('xpath','/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]')
	informacion = localizacion.find_elements(By.TAG_NAME,'img')
	time.sleep(2)
	if len(informacion)!=0:					
		tiempo_estimado = driver.find_element('xpath','/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[1]/div[1]/div[1]/div[1]/div[1]').text
	else:
		tiempo_estimado = "sin informacion"
	
	#Exportar
	vector_tiempo.append([tiempo_estimado])
	vector = pd.DataFrame(vector_tiempo,columns=['tiempo'])
	#Union de base y vector
	base_exportada = pd.concat([base_importada,vector],axis=1)
	base_exportada.to_csv('Ejemplo_Distancia.csv',encoding='utf-8-sig',index=False)

driver.close()
