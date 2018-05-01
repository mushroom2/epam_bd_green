import csv
import sqlite3 as lite
import sys
con = lite.connect('db')

def add_row_interests(cat, id):

    cur = con.cursor()
    cur.execute("insert into Interests values ('{}', {})".format(cat, id))
    con.commit()


def update_row_interests(cat, id):
    cur = con.cursor()
    cur.execute('''update Interests set "InterestName" = '{}', "InterestId" = {} where "InterestId" = {}'''.format(cat, id, id))
    con.commit()


with open('user_data_full_list.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        if row[0] != 'Category':
            try:
                add_row_interests(row[0], row[1])
            except lite.IntegrityError:
                update_row_interests(row[0], row[1])


con.close()