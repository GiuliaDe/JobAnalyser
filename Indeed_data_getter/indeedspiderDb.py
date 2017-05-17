import mysql.connector

from indeed import IndeedClient

from Data_manager import indeed_csv_handler as ch

publisher = "254856305429325"
publisherMax =""


cities=[]

locations = ch.import_listdata_from_csv('province-sigle.csv')
job_titles = ch.import_listdata_from_csv('lista_lavori.csv')


client = IndeedClient(publisher)
params = {
    'q': "Manager"
    ,'userip' : "127.0.0.1"
    ,'useragent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
    ,"format": "json"
    ,'v' : 2
    ,'start': 0
    ,'limit': 0
    ,'end' : 1000000
    #,'sort':'date'
    ,'co': 'it'
    ,"fromage":114
    ,"latlong" : 1
    ,"l":"Milano"
#	,"chnl" : "prjct"
}

storage = []



db=mysql.connector.connect(host="localhost",user="giulia",
                  passwd="giulia",db="JobTest")

cursor = db.cursor()

add_job = ("INSERT INTO lavori_all "
               "(hours, city, date, location_full, url, jobtitle, company, stations, "
           "onmousedown,snippet, source, state, sponsored, country, formatted_location, jobkey, "
           "expired,indeedApply,latitude, longitude)"
               "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,"
           "%s,%s,%s,%s,%s,%s,%s,%s,"
           "%s,%s,%s,%s)")

for loc in locations:
    params['l']=loc
    print "Nuova Location ", loc

    for jt in job_titles:
        params['q']= jt
        print "Inizio ricerca per ", loc, jt
        check = False

        for i in range(25,1025,25):# il secondo parametro va impostato = al n di offerte tot
            params['limit']=i
            params['start']= i-25
            client.search(**params)
            request = client.search(**params)
            #storage.append(request)
            print "Richiesta: ", loc, jt, ". Ciclo: ", i,", numero restituite: ", len(request['results'])

            if (len(request['results'])<25):
                if(check):
                    break
                else:
                    check=True

            num_errors=0
            #for block in storage:
            for job in request['results']:
                data_job = (job['formattedRelativeTime'],job['city'],job['date'],job['formattedLocationFull'],job['url'],job['jobtitle'],job['company'],job['stations'],
                job['onmousedown'],job['snippet'],job['source'],job['state'],job['sponsored'],job['country'],job['formattedLocation'],job['jobkey'],
                job['expired'],job['indeedApply'],job['latitude']  if 'latitude' in job else "",job['longitude']  if 'longitude' in job else "")
                try:
                    cursor.execute(add_job, data_job)
                except Exception, e:
                    num_errors+=1
                    #print e
                    continue
            print "Numero errori o gia esistenti in database: ", num_errors
            db.commit()

cursor.close()
db.close()


