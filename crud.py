import pymongo
import const


def connect(conn):
    return pymongo.MongoClient(conn)


base = {}
client = connect(const.conn)
users = client['url-checker']['users']
for document in users.find():
    base = document


def user_add(login, email, password):
    user = {'login': login, 'email': email, 'password': password, 'urls': []}
    response = users.insert_one(user)
    if response.acknowledged:
        print("OK")
    else:
        print("No")
    client.close()


if base == {} or base['login'] != document['email']:
    user_add('Tema', 'aaa@mail.ru', 'Best_Proger')
else:
    print("Такой пользователь уже существует")
