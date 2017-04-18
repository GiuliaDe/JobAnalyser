from indeed import IndeedClient
import csv
from unidecode import unidecode
from selenium import webdriver

publisher = ""
publisherMax =""

client = IndeedClient(publisher)
params = {
	'q': "*"
	,'userip' : "127.0.0.1"
	,'useragent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
	,"format": "json"
	,'v' : 2
	,'start': 0	
	,'limit': 0
	,'end' : 10000
	,'sort':'date'	
	,'co': 'it'	
	,"fromage":7
	,"latlong" : 1
#	,"chnl" : "prjct"
}

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


with open('crwlinddeed.csv', 'w') as file:
	file_writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
	headers = ["hours", "city", "date", "location_full", "url", "jobtitle", "company", "stations", "onmousedown",
			   "snippet", "source", "state", "sponsored", "country", "formatted_location", "jobkey", "expired", "indeedApply",
			   "latitude", "longitude",
			   "text"]
	file_writer.writerow(headers)

	for block in storage:
		for job in block['results']:
			info = [unicode(job['formattedRelativeTime']).encode('utf-8'), unicode(job['city']).encode('utf-8'),
				unicode(job['date']).encode('utf-8'), unicode(job['formattedLocationFull']).encode('utf-8'),
				unicode(job['url']).encode('utf-8'), unicode(job['jobtitle']).encode('utf-8'),
				unicode(job['company']).encode('utf-8'), unicode(job['stations']).encode('utf-8'),
				unicode(job['onmousedown']).encode('utf-8'), unicode(job['snippet']).encode('utf-8'),
				unicode(job['source']).encode('utf-8'), unicode(job['state']).encode('utf-8'),
				unicode(job['sponsored']).encode('utf-8'), unicode(job['country']).encode('utf-8'),
				unicode(job['formattedLocation']).encode('utf-8'), unicode(job['jobkey']).encode('utf-8'),
				unicode(job['expired']).encode('utf-8'), unicode(job['indeedApply']).encode('utf-8'),
				unicode(job['latitude']).encode('utf-8') if 'latitude' in job else "",
                unicode(job['longitude']).encode('utf-8') if 'longitude' in job else ""
				,unicode(job['text']).encode('utf-8')
				]
			file_writer.writerow(info)


#il problema ora resta per latitude e longitude che il csv per qualche oscuro motivo rifiuta'''


