from indeed import IndeedClient
import csv
from unidecode import unidecode
from selenium import webdriver
import mysql.connector


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

for i in range(25,50,25):# il secondo parametro va impostato = al n di offerte tot
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


db=mysql.connector.connect(host="localhost",user="",
                  passwd="",db="JobTest")

cursor = db.cursor()

add_job = ("INSERT INTO lavori "
               "(hours, city, date, location_full, url, jobtitle, company, stations, "
		   "onmousedown,snippet, source, state, sponsored, country, formatted_location, jobkey, "
		   "expired,indeedApply,latitude, longitude,testo)"
               "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,"
		   "%s,%s,%s,%s,%s,%s,%s,%s,"
		   "%s,%s,%s,%s,%s)")

for block in storage:
	for job in block['results']:
		data_job = (job['formattedRelativeTime'],job['city'],job['date'],job['formattedLocationFull'],job['url'],job['jobtitle'],job['company'],job['stations'],
					job['onmousedown'],job['snippet'],job['source'],job['state'],job['sponsored'],job['country'],job['formattedLocation'],job['jobkey'],
					job['expired'],job['indeedApply'],job['latitude'],job['longitude'],job['text'])
		cursor.execute(add_job, data_job)

db.commit()

cursor.close()
db.close()


