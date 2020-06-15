from sched import scheduler


import pymongo
import const
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from flask import render_template, request, redirect, url_for, Flask, jsonify


app = Flask(__name__)


def connect(conn):  # подключение к базе
    return pymongo.MongoClient(conn)


res = ''
base = {}  # получение коллекции из базы
client = connect(const.conn)
users = client['url-checker']['users']
for document in users.find():
    base = document

scheduler = BackgroundScheduler()
scheduler.start()


def job_check(username, url_in_user):
    ar_inter = []
    user = users.find_one({"login": username})['urls']
    for i in range(len(user)):
        if user[i][0] == url_in_user:
            response = requests.get(url_in_user)
            sc = response.status_code
            ts = response.elapsed.total_seconds()
            ar_inter.append(url_in_user)
            ar_inter.append(user[i][1])
            ar_inter.append(sc)
            ar_inter.append(ts)
            user[i] = ar_inter
            users.update_one({"login": username}, {"$set": {"urls": user}})


@app.route('/webcheck-light')
def str_webcheck_light():  # функция отрисовки страницы с быстрой проверкой url
    return render_template('/webcheck-light.html')

@app.route('/index_ok')
def str_index_ok():  # функция отрисовки главной страницы
    return render_template('/index_ok.html')


@app.route('/', methods=['POST', 'GET'])
def index():  # функция регистрации \ авторизации
    if request.method == "POST":  # если что то отправляем
        global username
        username = request.form['user_name']  #
        pas = request.form['password']  # получение данных из полей формы
        email = request.form['email']  #
        res = username + ' ' + email + ' ' + pas
        res_lst = res.split()
        client = connect(const.conn)
        users = client['url-checker']['users']

        if email == '':  # если поле логин найдено в базе
            if users.find_one({'login': username}) is not None:
                url_db = users.find_one({"login": username})['urls']
                for i in range(len(url_db)):
                    cnt = str(i)
                    url_in_user = url_db[i][0]
                    inter = int(url_db[i][1])
                    scheduler.add_job(id=cnt, func=job_check, trigger="interval", args=(username, url_in_user), minutes=inter)
                    scheduler.print_jobs()
                return redirect(url_for('str_index_ok'))
            else:
                return "<h1>Вы не зарегистированы</h1>"
            # return redirect(url_for('user', usr=res_lst))
        else:  # иначе регистрация
            def user_add(username, email, pas):  # функция добавления пользователей в базу
                user = {'login': username, 'email': email, 'password': pas, 'urls': [], 'urls_light': []}
                response = users.insert_one(user)
                client.close()

            if base == {} or users.find_one({'email': email}) is None:
                user_add(res_lst[0], res_lst[1], res_lst[2])
                url_db = users.find_one({"login": username})['urls']
                for i in range(len(url_db)):
                    url_in_user = url_db[i][0]
                    inter = int(url_db[i][1])
                    scheduler.add_job(func=job_check, trigger="interval", args=(username, url_in_user), minutes=inter)
                scheduler.print_jobs()
                return redirect(url_for('str_index_ok'))
            else:
                return "<h1>Такой пользователь уже существует</h1>"
                # return render_template('/send_urls.html')
                # return redirect(url_for('user', usr=res_lst))
    else:
        lst_jobs = scheduler.get_jobs()
        client = connect(const.conn)
        users = client['url-checker']['users']
        cnt = 0
        if lst_jobs != []:
            for i in range(len(base['urls'])):
                scheduler.remove_job(str(cnt))
                cnt += 1
            scheduler.print_jobs()
            return render_template('index.html')
        else:
            return render_template('index.html')


@app.route('/webcheck-light', methods=['POST', 'GET'])
def send_url_db():
    if request.method == "POST":
        url = request.form['url']
        ar_url = []
        ar_url.append(url)
        print(ar_url)
        try:
            response = requests.get(url)
            sc = response.status_code
            ts = response.elapsed.total_seconds()
            ar_url.append(sc)
            ar_url.append(ts)
            url_db_light = users.find_one({"login": username})['urls_light']
            url_db_light.append(ar_url)
            users.update_one({"login": username}, {"$set": {"urls_light": url_db_light}})
            return render_template('webcheck-light.html')
        except:
            print('Ссылка некорректра')
            return render_template('webcheck-light.html')

    else:
        users.update_one({"login": username}, {"$set": {"urls_light": []}})
        return redirect(url_for('webcheck-light'))


@app.route('/get_data_light', methods=['POST', 'GET'])
def json_ms_lite():
    url = users.find_one({"login": username})['urls_light']
    if request.method == "POST" and url != []:
        return jsonify({'url': url[-1]})
    elif request.method == "GET":
        return render_template('webcheck-light.html')


@app.route('/get_data', methods=['POST', 'GET'])
def json_ms():
    url = users.find_one({"login": username})['urls']
    if request.method == "POST":
        return jsonify({'url': url})
    elif request.method == "GET":
        return render_template('webcheck.html')


@app.route('/webcheck', methods=['POST', 'GET'])
def table_url_send():
    if request.method == "POST":
        url_inp = request.form['url_table']
        inter = request.form['interval']
        if url_inp == '' or inter == '':
            return render_template('webcheck.html')
        ar_url = []
        ar_url.append(url_inp)
        ar_url.append(inter)
        #print(ar_url)
        try:
            response = requests.get(url_inp)
            sc = response.status_code
            ts = response.elapsed.total_seconds()

            if sc == 200 and ts <= 10:
                print(sc, ts)
            else:
                print(sc, ts)
                print('Ссылка НЕ работает')
            url_db = users.find_one({"login": username})['urls']
            ar_url.append(sc)
            ar_url.append(ts)
            url_db.append(ar_url)
            users.update_one({"login": username}, {"$set": {"urls": url_db}})
            return render_template('webcheck.html')
        except:
            print('Ссылка некорректра')
        #    return "<h1>Ссылка некорректна</h1>"

    else:
        return render_template('webcheck.html')


@app.route('/remove_url')
def data_del():
    cont_del = request.args.get('url_del')
    user = users.find_one({"login": username})['urls']
    ar_base = []
    for i in range(len(user)):
        if user[i][0] == cont_del:
            print(user[i])
            print('if')
            users.update_one({"login": username}, {"$set": {"urls": ar_base}})
        else:
            ar_base.append(user[i])
            print(ar_base)
            print('else')
            users.update_one({"login": username}, {"$set": {"urls": ar_base}})
    return render_template('webcheck.html')


#if __name__ == "__main__":
#    app.run(debug=True)
