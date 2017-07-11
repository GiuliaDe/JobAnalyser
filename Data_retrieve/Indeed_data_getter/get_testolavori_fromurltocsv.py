import csv

from Data_manager import htmlprocessor as hp

fw = open('testi_lavori.csv', 'w')
file_writer = csv.writer(fw, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)


with open('url_indeed.csv','r') as f:


    for line in f:
        job= line.split(',')

        #print tokens[1]
        try:
            url=job[1]
            testo = hp.get_testolavoroindeed_fromurl(url)
            info = [unicode(job[0]).encode('utf-8'), unicode(testo).encode('utf-8')]
            file_writer.writerow(info)
        except Exception, e:
            continue


fw.close()