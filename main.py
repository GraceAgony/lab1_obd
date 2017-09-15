import pickle
import sys

class  Database:
    teams = {}
    sportsmens = {}
    def __init__(self):
        try:
            file = open("db.bytes", 'rb')
            self.data = pickle.load(file)
            self.teams = content['teams']
            self.sportsmens = content['sportsmens']
            file.close()
        except:
            content = {}
            content['teams'] = {}
            content['sportsmens'] = {}
            pickle.dump(content, open('db.bytes', 'wb'))

    def __del__(self):
        file = open("db.bytes", "wb")
        content = {}
        content['teams'] = self.teams
        content['sportsmens'] = self.sportsmens
        pickle.dump(content, file)
        file.close()


db = Database()

def create_sportsman(args):

    if not args['name'] in db.sportsmens:
        db.sportsmens[args['name']] = {}

    db.sportsmens[args['name']]['name'] = args['name']
    db.sportsmens[args['name']]['team'] = args['team']

    try:
        db.teams[args['team']]['sportsmens'].add(args['name'])
    except KeyError:
        print("sorry, there is no this team")
        return

    if 'points' in args:
        try:
            db.sportsmens[args['name']]['points'] = int(args['points'])
        except ValueError:

            print("points must be int")
    else:
        db.sportsmens[args['name']]['points'] = 0
    return


def create_teams(args):
    if not args['name'] in db.teams:
        db.teams[args['name']] = {}

    db.teams[args['name']]['sportsmens'] = args['sportsmens']
    db.teams[args['name']]['name'] = args['name']
    for sportsman_name in args['sportsmens']:
        sportsman = {}
        sportsman['name'] = sportsman_name
        sportsman['team'] = args['name']
        create_sportsman(sportsman)


def update_team(name, key, value):
    if key == 'name':
        for sportsman in db.sportsmens:
            if db.sportsmens[sportsman]['team'] == name:
                db.sportsmens[sportsman]['team'] = value
        db.teams[value] = db.teams.pop(name)
        db.teams[value]['name'] = value

    return

def update_sportsman(name, key, value):
    if key == 'name':
        db.teams[db.sportsmens[name]['team']]['sportsmens'].add(value)
        db.teams[db.sportsmens[name]['team']]['sportsmens'].remove(name)
        db.sportsmens[name]['name'] = value
        db.sportsmens[value] = db.sportsmens.pop(name)
    elif key == 'points':
        try:
            db.sportsmens[name]['points'] = int(value)
        except ValueError:
            print("points must be int")
    elif key == 'team':
        try:
            db.teams[value]['sportsmens'].add(name)
        except KeyError:
            print("there is no this team")
            return

        db.teams[db.sportsmens[name]['team']]['sportsmens'].remove(name)
        db.sportsmens[name]['team'] = value

    return

def delete_spotsmen(name):
    db.teams[db.sportsmens[name]['team']]['sportsmen'].remove(name)
    del db.sportsmens[name]
    return

def  delete_team(name):
    for sportsman in db.teams[name]['sportsmens']:
        del db.sportsmens[sportsman]

    del db.teams[name]
    return

def filter_sportsman():
    for team in db.teams:
        maxPoints = -1
        leaders = []
        for sportsman in db.teams[team]['sportsmens']:
            if db.sportsmens[sportsman]['points'] == maxPoints:
                leaders.append(db.sportsmens[sportsman]['name'])
            elif db.sportsmens[sportsman]['points'] > maxPoints:
                maxPoints = db.sportsmens[sportsman]['points']
                del leaders[:]
                leaders.append(db.sportsmens[sportsman]['name'])

        for leader in leaders :
            select(db.sportsmens, leader)

    return

def select(table, key=None):
    if key == None:
        for key in table:
            for field in table[key]:
                print field , ':', table[key][field]


    else:
        for field in table[key]:
            print field,  ':',  table[key][field]

    print('---------------------')


def menu():
    print ("Choose option:")
    print ("1. SELECT ")
    print ("2. DELETE ")
    print ("3. INSERT ")
    print ("4. UPDATE ")
    print ("5. Show the best athletes ")
    print ("6. Exit")
    selection = raw_input()

    if ((selection != '5') and (selection != '6')):
        print ("Choose table:")
        print ("1. Teams")
        print ("2. Sportsmens")
        table_num = raw_input()
        if table_num == '1':
            table = db.teams
            table_name = "Teams"
        elif table_num == '2':
            table = db.sportsmens
            table_name = "Sportsmens"
        else:
            menu()
            return

    if selection == '1':
        key = raw_input("Enter name of field, you want to select or * for all")
        if key == '*':
            select(table)
        elif key in table:
            select(table, key)
        else:
            print( "Wrong input")

    elif selection == '2':
        name = raw_input("Enter name of item, you want to delete: ")
        if name in table:
            if table_name == "Teams":
                delete_team(name)
            elif table_name == "Sportsmans":
                delete_spotsmen(name)
        else:
            print ("Wrong input")
        return

    elif selection == '3':
        print ("Enter all values of fields:")
        if table_name == "Teams":
            print ("name spotsmens")
            keys = ('name', 'sportsmens')
            arg_list = raw_input().split()

            if len(arg_list) < 2:
                print ("Wrong input")
                menu()
                return

            args = dict(zip(keys, arg_list))
            args['sportsmens'] = set(arg_list[1:])
            create_teams(args)

        elif table_name == "Sportsmens":
            print ("name team points")
            keys = ('name', 'team', 'points')
            arg_list = raw_input().split()

            if len(arg_list) < 3:
                print("Wrong input")
                menu()
                return
            if len(arg_list) > 3:
                print ("Wrong input")
                menu()
                return

            fields = dict(zip(keys, arg_list))
            create_sportsman(fields)

    elif selection == '4':
        item = raw_input("Enter name of item that you want to change: ")
        if item in table:
            print ("Enter what field do you want to change in table:")
            if table_name == "Teams":
                print ("(name)")
                keys = ('name')
            elif table_name == "Sportsmens":
                print ("(name, team or points)")
                keys = ('name', 'team', 'points')

            key = raw_input()
            if key in keys:
                value = raw_input("Enter new value for {0}: ".format(key))

                if table_name == "Teams":
                    update_team(item, key, value)
                elif table_name == "Sportsmens":
                    update_sportsman(item, key, value)
            else:
                print("Wrong input")
            return
        else:
            print ("Wrong input")
    elif selection == '5':
        filter_sportsman()
    elif selection == '6':
        return 0
    else:
        print("Wrong input")


if __name__ == "__main__":
    res = 1
    while res != 0:
        res = menu()




