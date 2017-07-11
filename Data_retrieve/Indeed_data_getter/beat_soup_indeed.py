import Data_manager.htmlprocessor as hp
from Data_manager import dbdatahandler as ddh

tot_iterazioni = 1000
numjobs = 25

db, cursor = ddh.open_connection()

for i in range(0, tot_iterazioni):

    print "Numero iterazione: ", i

    try:
        jobs = ddh.getjobsnoprocessedurl(numjobs)

        print "Inizio scaricamento dati"

        for job in jobs:
            try:
                url=job['url']
                testo = hp.get_testolavoroindeed_fromurl(url)

                ddh.updatelavoriNoCommit(db, cursor, testo, job['jobkey'])

            except Exception, e:
                print "Error"
                ddh.setlavorourlprocessed(db, cursor, job['jobkey'])
                continue

        ddh.dbcommit(db)

    except Exception, e:
        continue

ddh.closeconnection(cursor, db)
