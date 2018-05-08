import csv
import sqlite3 as lite

class SqliteConnector(object):
    def __init__(self):
        self.con = lite.connect('db')
        self.cur = self.con.cursor()

    def add_row_interests(self, id, name, address, lon, lat, rating, tags):
        self.cur.execute('''insert into "Places"  values ('{}', '{}', '{}', {}, {}, {}, '{}')'''.format(id, name, address, lon, lat, rating, tags))

    def commit_and_close(self):
        self.con.commit()
        #self.con.close()

'''
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
'''
