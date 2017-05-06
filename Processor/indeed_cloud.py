import os
from tagcloud import *
from collections import Counter
from tagme import *
import mysql.connector
import pprint


min_rho= 0.2

db=mysql.connector.connect(host="localhost",user="",
                  passwd="",db="JobTest")

cursor = db.cursor(buffered=True)
query_select = "SELECT id,jobtitle,testo FROM lavori_all WHERE testo IS NOT NULL AND entity_processed=0 LIMIT 1"
cursor.execute(query_select)
jobs = cursor.fetchall()



query_insert = "INSERT INTO entities (title,wikipedia_id,lavoro_id) VALUES (%s,%s,%s)"
query_update = "UPDATE lavori_all SET entity_processed=%s WHERE id=%s"


print len(jobs)


entities = []

for job in jobs:
    testo = job[2]
    print testo
    #print testo
    if testo:
        qr=query_tagme(testo)
        qr_ann=qr['annotations']
        print "annotations"
        ann = [a for a in qr_ann if float(a["rho"]) > min_rho]

        for a in ann:
            data_insert=(a['title'], a['id'], job[0])
            print data_insert
            cursor.execute(query_insert, data_insert)

        data_update = (1,job[0])
        cursor.execute(query_update,data_update)

        db.commit()

        #for parola in text_entities:


        #entities += text_entities
        #entities.append(testo)

c = Counter(entities)
print "Parole piu frequenti"
print c.most_common(100)
#generate_tag_cloud(c.most_common(100), "lavoro.png")

cursor.close()
db.close()