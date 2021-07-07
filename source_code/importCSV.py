import csv

import MySQLdb

mydb = MySQLdb.connect(host="localhost", user="root", password="", database="ta_dataset1000")

with open('dataset 1000.csv') as csv_file:
    csvfile = csv.reader(csv_file, delimiter=',')
    all_value = []
    for row in csvfile:
        value = (row[0], row[1], row[2])
        all_value.append(value)

query = "insert into `news`(`judulBerita`, `teksBerita`, `label`) values (%s,%s,%s)"

mycursor = mydb.cursor()
mycursor.executemany(query, all_value)
mydb.commit()