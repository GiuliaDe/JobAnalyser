import os
from tagcloud import *
from collections import Counter
from tagme import *
import mysql.connector
import pprint


min_rho= 0.2

db=mysql.connector.connect(host="localhost",user="giulia",
                  passwd="giulia",db="JobTest")

cursor = db.cursor(buffered=True)

query_select = "SELECT id,jobtitle,testo FROM lavori_all WHERE testo IS NOT NULL AND entity_processed=0 limit 100"

query_insert = "INSERT INTO entities (title,wikipedia_id,rho,link_probability, start_index,end_index,lavoro_id)" \
               " VALUES (%s,%s,%s,%s,%s,%s,%s)"

query_update = "UPDATE lavori_all SET entity_processed=%s WHERE id=%s"

for it in range(0,100):


    cursor.execute(query_select)
    jobs = cursor.fetchall()


    print "iterazione: ", it, "lavori da processare: ", len(jobs)


    entities = []

    for job in jobs:
        testo = job[2]

        #print "titolo: ",job[1]
        #print "testo: ",testo
        if testo:
            qr=query_tagme(testo)
            qr_ann=qr['annotations']
            #print "annotations"
            ann = [a for a in qr_ann if float(a["rho"]) > min_rho]

            for a in ann:
                #print a
                data_insert=(a['title'].encode('utf-8') if 'title' in a else ""
                             , a['id'],a['rho'],a['link_probability'],a['start'],a['end'], job[0])
                #print data_insert
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