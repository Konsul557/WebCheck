import requests
url = input('Введите запрос ')
try:
    response = requests.get(url)
    sc = response.status_code
    ts = response.elapsed.total_seconds()

    if sc == 200 and ts <= 10:
        print ('Ссылка работает')
        print(sc, ts)
    else :
        print ('Ссылка НЕ работает')
except:
    print ('Ссылка некорректра')