
""" 
== OpenWeatherMap ==

OpenWeatherMap — онлайн-сервис, который предоставляет бесплатный API
 для доступа к данным о текущей погоде, прогнозам, для web-сервисов
 и мобильных приложений. Архивные данные доступны только на коммерческой основе.
 В качестве источника данных используются официальные метеорологические службы
 данные из метеостанций аэропортов, и данные с частных метеостанций.

Необходимо решить следующие задачи:

== Получение APPID ==
    Чтобы получать данные о погоде необходимо получить бесплатный APPID.
    
    Предлагается 2 варианта (по желанию):
    - получить APPID вручную
    - автоматизировать процесс получения APPID, 
    используя дополнительную библиотеку GRAB (pip install grab)

        Необходимо зарегистрироваться на сайте openweathermap.org:
        https://home.openweathermap.org/users/sign_up

        Войти на сайт по ссылке:
        https://home.openweathermap.org/users/sign_in

        Свой ключ "вытащить" со страницы отсюда:
        https://home.openweathermap.org/api_keys
        
        Ключ имеет смысл сохранить в локальный файл, например, "app.id"

        
== Получение списка городов ==
    Список городов может быть получен по ссылке:
    http://bulk.openweathermap.org/sample/city.list.json.gz
    
    Далее снова есть несколько вариантов (по желанию):
    - скачать и распаковать список вручную
    - автоматизировать скачивание (ulrlib) и распаковку списка 
     (воспользоваться модулем gzip 
      или распаковать внешним архиватором, воспользовавшись модулем subprocess)
    
    Список достаточно большой. Представляет собой JSON-строки:
{"_id":707860,"name":"Hurzuf","country":"UA","coord":{"lon":34.283333,"lat":44.549999}}
{"_id":519188,"name":"Novinki","country":"RU","coord":{"lon":37.666668,"lat":55.683334}}
    
    
== Получение погоды ==
    На основе списка городов можно делать запрос к сервису по id города. И тут как раз понадобится APPID.
        By city ID
        Examples of API calls:
        http://api.openweathermap.org/data/2.5/weather?id=2172797&appid=b1b15e88fa797225412429c1c50c122a

    Для получения температуры по Цельсию:
    http://api.openweathermap.org/data/2.5/weather?id=520068&units=metric&appid=b1b15e88fa797225412429c1c50c122a

    Для запроса по нескольким городам сразу:
    http://api.openweathermap.org/data/2.5/group?id=524901,703448,2643743&units=metric&appid=b1b15e88fa797225412429c1c50c122a


    Данные о погоде выдаются в JSON-формате
    {"coord":{"lon":38.44,"lat":55.87},
    "weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04n"}],
    "base":"cmc stations","main":{"temp":280.03,"pressure":1006,"humidity":83,
    "temp_min":273.15,"temp_max":284.55},"wind":{"speed":3.08,"deg":265,"gust":7.2},
    "rain":{"3h":0.015},"clouds":{"all":76},"dt":1465156452,
    "sys":{"type":3,"id":57233,"message":0.0024,"country":"RU","sunrise":1465087473,
    "sunset":1465149961},"id":520068,"name":"Noginsk","cod":200}    


== Сохранение данных в локальную БД ==    
Программа должна позволять:
1. Создавать файл базы данных SQLite со следующей структурой данных
   (если файла базы данных не существует):

    Погода
        id_города           INTEGER PRIMARY KEY
        Город               VARCHAR(255)
        Дата                DATE
        Температура         INTEGER
        id_погоды           INTEGER                 # weather.id из JSON-данных

2. Выводить список стран из файла и предлагать пользователю выбрать страну 
(ввиду того, что список городов и стран весьма велик
 имеет смысл запрашивать у пользователя имя города или страны
 и искать данные в списке доступных городов/стран (регуляркой))

3. Скачивать JSON (XML) файлы погоды в городах выбранной страны
4. Парсить последовательно каждый из файлов и добавлять данные о погоде в базу
   данных. Если данные для данного города и данного дня есть в базе - обновить
   температуру в существующей записи.


При повторном запуске скрипта:
- используется уже скачанный файл с городами;
- используется созданная база данных, новые данные добавляются и обновляются.


При работе с XML-файлами:

Доступ к данным в XML-файлах происходит через пространство имен:
<forecast ... xmlns="http://weather.yandex.ru/forecast ...>

Чтобы работать с пространствами имен удобно пользоваться такими функциями:

    # Получим пространство имен из первого тега:
    def gen_ns(tag):
        if tag.startswith('{'):
            ns, tag = tag.split('}')
            return ns[1:]
        else:
            return ''

    tree = ET.parse(f)
    root = tree.getroot()

    # Определим словарь с namespace
    namespaces = {'ns': gen_ns(root.tag)}

    # Ищем по дереву тегов
    for day in root.iterfind('ns:day', namespaces=namespaces):
        ...

"""
import json
import os
import requests
import sqlite3 as sql

def get_cities_by_country(country):
    """Функция возвращает данные городов из файла в виде списка"""
    cities = []
    for idx,item in enumerate(parsed_json):
        if item['country'].lower() == country.lower():
            cities.append(parsed_json[idx])
    return cities

def get_city(city):
    """Функция возвращает данные города из файла в виде списка"""
    cities = []
    for idx,item in enumerate(parsed_json):
        if item['name'].lower() == city.lower():
            cities.append(parsed_json[idx])
            return cities

def get_cities_id(city_list):
    """Функция возвращает спиок id городов из списка данных городов"""
    city_list_id = [str(x['id']) for x in city_list]
    city_str_id = ','.join(city_list_id)
    return city_str_id

def get_request_str(id_str, app_id,type_req = 'full'):
    """функция формирует строку гет-запроса к API"""
    if type_req == 'full':
        request_str = 'http://api.openweathermap.org/data/2.5/group?id=' + id_str + '&units=metric&appid=' + app_id
    elif type_req == 'weather':
        request_str = 'http://api.openweathermap.org/data/2.5/weather?id=' + id_str + '&units=metric&appid=' + app_id
    return request_str

def get_data_weather(id_str, app_id,type_req = 'full'):
    """функция получает данные через запрос к API в формате JSON"""
    request = get_request_str(id_str, app_id, type_req)
    res = requests.get(request)
    data = res.json()
    return data

def get_full_data(city_list):
    """Функция получает все данные по погоде городов.
    Сервер API не может принять все id в одном запросе, поэтому отправляем порции запросов"""
    data = []
    i = 0
    idx = 0
    while i < len(city_list)//LIMIT_ID + 1:
        cities = get_cities_id(city_list[idx:idx + LIMIT_ID])   
        result = get_data_weather(cities,APP_ID)
        data.append(result)
        idx += LIMIT_ID
        i += 1
    return data

def write_to_db(data_weather, con, table_name):
    """Функция записывает и обновляет данные в БД, полученные от API"""
    cursor_db = con.cursor()
    #если несколько городов в списке
    if type(data_weather) == list:
        for part in data_weather:
            #API может вернуть пустые данные
            try:
                for item in part['list']:           
                    #пытаемся записать данные в БД
                    try:
                        row = [item['id'],item['name'],item['dt'],item['main']['temp'],item['weather'][0]['id']] 
                        cursor_db.execute('INSERT INTO ' + table_name + ' VALUES(?,?,?,?,?)',row)
                    #если id_города существует, то обновляем данные    
                    except:
                        sql = """UPDATE """ + table_name + """
                                 SET Температура = ?,
                                     Дата = ?
                                WHERE id_города = ?
                                """
                        row = [item['main']['temp'],item['dt'],item['id']]                   
                        cursor_db.execute(sql,row)
                        

            #выводим сообщение, по какому id города нет данных
            except KeyError:
                    print(part)
                    continue
                    
    #если данные только по одному городу                
    elif type(data_weather) == dict:
        try:
            row = [data_weather['id'],data_weather['name'],data_weather['dt'],data_weather['main']['temp'],data_weather['weather'][0]['id']] 
            cursor_db.execute('INSERT INTO ' + table_name + ' VALUES(?,?,?,?,?)',row)
            
        except:
            sql = """UPDATE """ + table_name + """
                    SET Температура = ?,
                    Дата = ?
                    WHERE id_города = ?
                     """
            row = [data_weather['main']['temp'],data_weather['dt'],data_weather['id']]                   
            cursor_db.execute(sql,row)
    con.commit()
    cursor_db.close()
    con.close()

def start():
    """Функция описывает интерфейс пользователя и выполняет команды"""
    while True:
        con = sql.connect(os.path.join(DIR,'openweather'))
        cur = con.cursor()
        
        print("""Для получения данных о погоде города нажмите 1; 
             для получения данных о погороде по городам страны нажмите 2; 
             чтобы выйти нажмите 3""")
        start = input('Введите команду ')
        if start == '1':
            city_name = input('Введите название города ')
            city = get_city(city_name)
            if city == []:
                print('такого города не существует')
            else:
                city = get_cities_id(city)
                data = get_data_weather(city, APP_ID,'weather')                
                write_to_db(data, con, 'weather')
                print('Данные в БД по городу {} сохранены'.format(city_name))
        if start == '2':
            country_name = input('Введите название страны ')            
            country = get_cities_by_country(country_name)         
            if country == []:
                print('Неправильна указана страна')
            else:                
                data = get_full_data(country)
                write_to_db(data, con, 'weather')
                print('Данные в БД по коду страны {} сохранены'.format(country_name))
                API_file = open(os.path.join(DIR,'weather_api.json'), 'w',encoding = 'UTF-8')
                json.dump(data,API_file, indent = 2)
        if start == '3':
            break
        else:
            continue
            
    con.commit()
    cur.close()
    con.close()

    
# Устанавливаем константы
DIR = os.getcwd()
f_name = 'city.list.json'
APP_ID = ''.join(open(os.path.join(DIR,'app.id'),'r',encoding = 'UTF-8').readlines())
# максимальное количество id городов в одном запросе к API
LIMIT_ID = 20

# Получаем данные о городах 
json_f =  open(os.path.join(DIR,f_name),'r',encoding = 'UTF-8').readlines()
json_str = ''.join(json_f)

parsed_json = json.loads(json_str)

#Создаем таблицу БД, если она не создана
con = sql.connect(os.path.join(DIR,'openweather'))
cur = con.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS weather(id_города INTEGER PRIMARY KEY,'
                                           'Город VARCHAR(255),'
                                            'Дата DATE,'
                                            'Температура INTEGER,'
                                            'id_погоды INTEGER)')
con.commit()
cur.close()
con.close()

# Погружаем последний скачанный файл данных по коду страны из API
try:
    last_api_file =  open(os.path.join(DIR,'weather_api.json'),'r',encoding = 'UTF-8').readlines()
    json_api_str = ''.join(last_api_file)
    data = json.loads(json_api_str)
    file_date = os.path.getctime(os.path.join(DIR,'weather_api.json'))
except:
    data = None

# запускаем интерфейс пользователя	
if data != None:
    print('Загружен последний файл от {}. Хотетите получить или обновить новые данные (Y/N)'.format(file_date))
    command = input('(Y/N) ')
    if command  == 'Y':
        start()
else:
    start()