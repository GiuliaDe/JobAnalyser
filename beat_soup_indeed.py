from indeed import IndeedClient
import csv
from unidecode import unidecode
import mysql.connector
import urllib
from bs4 import BeautifulSoup

db=mysql.connector.connect(host="localhost",user="",
                  passwd="",db="JobTest")

cursor = db.cursor(buffered=True)


query_select = "SELECT jobkey, url FROM lavori_all WHERE url_processed=0 AND testo IS NULL LIMIT 25"

query_update = "UPDATE lavori_all SET testo=%s , url_processed=%s WHERE jobkey=%s"

query_update_error = "UPDATE lavori_all SET url_processed=%s WHERE jobkey=%s"

num_it=1000



for i in range(0,num_it):

    print "Numero iterazione: ", i

    cursor.execute(query_select)

    try:
        jobs = cursor.fetchall()
        #print jobs
    except Exception, e:
        continue


    for job in jobs:
        print job


    print "Inizio scaricamento dati"

    for job in jobs:
        #print job[0]
        try:
            url=job[1]
            html = urllib.urlopen(url).read()
            soup = BeautifulSoup(html, 'html.parser')
            testo = soup.find("span", class_="summary").get_text()


            #testo = elements.text
            data_update = (testo,1,job[0])
            print data_update
            cursor.execute(query_update,data_update)

        except Exception, e:
            print "Error"
            err_data=(1,job[0])
            cursor.execute(query_update_error,err_data)
            #db.commit()
            #print e
            continue

    try:
        db.commit()
        print "dati inseriti"
    except Exception, e:
        continue

    urllib.urlcleanup()


cursor.close()
db.close()
