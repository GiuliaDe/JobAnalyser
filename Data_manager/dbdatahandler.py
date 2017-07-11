import mysql.connector


def open_connection():
    db = mysql.connector.connect(host="localhost", user="giulia",
                                 passwd="giulia", db="Jobs")
    cursor = db.cursor()
    return db, cursor


def dbcommit(db):
    db.commit()


def closeconnection(cursor,db):
    cursor.close()
    db.close()

def getjobswithtext(numjobs=10):
    db,cursor = open_connection()
    query_select = "SELECT id,jobtitle,testo,jobkey FROM lavori_all WHERE testo IS NOT NULL AND url_processed=1 LIMIT %s"
    cursor.execute(query_select, (numjobs if numjobs > 0 else 0,))
    sqljobs = cursor.fetchall()
    closeconnection(cursor,db)
    jobs=[]
    for sqljob in sqljobs:
        jobinfo={
            "id" : sqljob[0],
            "jobtitle": sqljob[1],
            "testo": sqljob[2],
            "jobkey": sqljob[3]
        }
        jobs.append(jobinfo)
    return jobs

def getjobsnoprocessedurl(numjobs=10):
    db,cursor = open_connection()
    query_select = "SELECT jobkey, url FROM lavori_all WHERE url_processed=0 AND testo IS NULL LIMIT %s"
    cursor.execute(query_select, (numjobs if numjobs > 0 else 0,))
    sqljobs = cursor.fetchall()
    closeconnection()
    jobs=[]
    for sqljob in sqljobs:
        jobinfo={
            "jobkey": sqljob[0],
            "url": sqljob[1]
        }
        jobs.append(jobinfo)
    return jobs


def updatelavoriNoCommit(db,cursor,testo,jobkey):
    query_update = "UPDATE lavori_all SET testo=%s , url_processed=%s WHERE jobkey=%s"
    data_update = (testo, 1, jobkey)
    cursor.execute(query_update, data_update)


def setlavorourlprocessed(db,cursor,jobkey):
    query_update = "UPDATE lavori_all SET url_processed=%s WHERE jobkey=%s"
    data_update = (1, jobkey)
    cursor.execute(query_update, data_update)

def insertnewjob(db, cursor, job):
    query_insert = ("INSERT INTO lavori_all "
               "(hours, city, date, location_full, url, jobtitle, company, stations, "
               "onmousedown,snippet, source, state, sponsored, country, formatted_location, jobkey, "
               "expired,indeedApply,latitude, longitude,testo)"
               "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,"
               "%s,%s,%s,%s,%s,%s,%s,%s,"
               "%s,%s,%s,%s,%s)")
    data_insert=[job["hours"],job["city"],job["date"],job["location_full"],job['url'],
                 job["jobtitle"], job["company"], job["stations"],
                 job["onmousedown"],job["snippet"],job["source"],job["state"],bool(job["sponsored"]), job["country"],
                 job["formatted_location"], job["jobkey"],
                 bool(job["expired"]), bool(job["indeedApply"]), job["latitude"],job["longitude"],job["text"]]
    cursor.execute(query_insert, data_insert)

def getjobsnotagmeentities(db, cursor,limite):
    query_select =""

