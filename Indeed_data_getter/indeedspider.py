import csv

from indeed import IndeedClient
from selenium import webdriver

import Data_manager.indeed_csv_handler as ch
from Data_manager import htmlprocessor as hp

publisher = ""
publisherMax =""

client = IndeedClient(publisher)

params = hp.get_indeedapi_default_parameters()

job_titles = ['Data scientist','Direttore','Giornalista']

storage = [] 

for i in range(25,75,25):# il secondo parametro va impostato = al n di offerte tot
	params['limit']=i
	params['start']= i-25
	client.search(**params)
 	request = client.search(**params)
	storage.append(request)

for block in storage:
	for job in block['results']:
		jurl = job['url']
		driver = webdriver.Firefox()
		driver.get(jurl)
		elements = driver.find_element_by_css_selector('#job_summary')
		driver.close()
		job['text'] = elements.text


with open('crwlinddeed.csv', 'a') as file:
    file_writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    ch.write_header(file_writer)
    for block in storage:
        for job in block['results']:
		    ch.write_job_row(file_writer,job)


#il problema ora resta per latitude e longitude che il csv per qualche oscuro motivo rifiuta'''


