import MySQLdb

mydb = MySQLdb.connect(host="localhost", user="root", password="", database="ta_dataset1000")

if (mydb):
    print("Berhasil terhubung ke database")