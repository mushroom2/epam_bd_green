import csv
import sqlite3 as lite
import sys
con = lite.connect('db')
cur = con.cursor()
def add_row_interests(cat, id):


    cur.execute('''insert into "Interests"  values ('{}', {})'''.format(cat, id))



def update_row_interests(cat, id):

    cur.execute('''update "Interests" set "InterestName" = '{}', "InterestId" = {} where "InterestId" = {}'''.format(cat, id, id))




with open('user_data_full_list.csv', newline='') as csvfile:
    dialect = csv.Sniffer().sniff(csvfile.read(1024))
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect)
    for row in reader:
        print(row)
        if row[0] != 'Category':
            try:
                add_row_interests(row[0].replace('"', ''), row[1])
            except lite.IntegrityError:
                update_row_interests(row[0].replace('"', ''), row[1])

con.commit()
con.close()