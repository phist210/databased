import csv
import psycopg2
from databased import *

conn = psycopg2.connect("dbname=sql_tour user=Friese host=/tmp/")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS life_saver(id serial PRIMARY KEY, bill varchar, amount money, month varchar, day integer) ; ")


def close_connection(conn, cursor):
    conn.commit()
    cursor.close()
    conn.close()


def write_csv_to_database():
    csv_file = open("life_saver.csv", "r")
    reader = csv.reader(csv_file, delimiter='\t')
    for row in reader:
        print(row)
        cursor.execute("INSERT INTO life_saver(bill, amount, month, day) VALUES (%s, %s, %s, %s)", (row[0], row[1], row[2], row[3]))
    return csv_file
