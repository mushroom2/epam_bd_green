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

    def add_poi_type(self, name, id):
        self.cur.execute(''' insert into "Interests" ("InterestName", "InterestId") values ('{}', {})'''.format(name, id))
        self.con.commit()

    def get_users(self):
        self.cur.execute('''select u."Name", u."Id", i."InterestName", i."InterestId" from "Users" u 
                            left join "UserInterests" ui on u."Id" = ui."UserId"
                            left join "Interests" i on i."InterestId" = ui."InterestId"
                            ''')

    def get_res(self):
        return self.cur.fetchall()


class User(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.interests = []

    def append_interests(self, iid, iname):
        self.interests.append({'name': iname, 'id': iid})

    def getuser(self):
        return {'name': self.name,
                'id': self.id,
                'interests': self.interests}

    def is_thet_user(self, id):
        return id == self.id


def get_dict_of_users():
    s = SqliteConnector()
    s.get_users()
    raw = s.get_res()
    res = {}

    if raw:
        us = User(raw[0][1], raw[0][0])
        for row in raw:
            if us.is_thet_user(row[1]):
                us.append_interests(row[3], row[2])
            else:
                res[us.id] = (us.getuser())
                us = User(row[1], row[0])
                us.append_interests(row[3], row[2])
    return res
