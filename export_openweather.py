
""" OpenWeatherMap (экспорт)

Сделать скрипт, экспортирующий данные из базы данных погоды, 
созданной скриптом openweather.py. Экспорт происходит в формате CSV или JSON.

Скрипт запускается из командной строки и получает на входе:
    export_openweather.py --csv filename [<город>]
    export_openweather.py --json filename [<город>]
    export_openweather.py --html filename [<город>]
    
При выгрузке в html можно по коду погоды (weather.id) подтянуть 
соответствующие картинки отсюда:  http://openweathermap.org/weather-conditions

Экспорт происходит в файл filename.

Опционально можно задать в командной строке город. В этом случае 
экспортируются только данные по указанному городу. Если города нет в базе -
выводится соответствующее сообщение.

"""

import csv
import json
import os
import sqlite3 as sql

def get_db_data_by_city(name,con,table_name):
    """Функция получает данные из БД по имени города"""
    cur = con.cursor()
    sql = 'SELECT * FROM ' + table_name + ' WHERE Город = ?'
    row = [name]
    result = cur.execute(sql,row).fetchone()
    con.commit()
    cur.close()
    return result  

def get_db_all_data(con,table_name):
    """Функция получает данные из БД по всем городам"""
    cur = con.cursor()
    sql = 'SELECT * FROM ' + table_name 
    result = cur.execute(sql).fetchall()
    con.commit()
    cur.close()
    return result

def export_to_csv(data, DIR, filename):
    """Функция эеспортирует данные из БД в csv"""
    with open(os.path.join(DIR,filename + '.csv'),'w',encoding = 'UTF-8', newline='') as file:
        headers = ('id_города','Город','Дата','Температура','id_погоды')
        csv.writer(file).writerow(headers)
        if type(data) == list:
            for row in data:        
                try:
                    csv.writer(file).writerow(row)
                except:
                    continue
        else:
                try:
                    csv.writer(file).writerow(data)
                except:
                    print('Объект типа None')

def export_to_html(data,DIR,filename):
    """Функция экспортирует данные из БД в html в виде таблицы"""
    with open(os.path.join(DIR,filename + '.html'),'w',encoding = 'UTF-8', newline='') as file:
        file.write("""<h1>Auto Mode Logs</h1>
                            <table>

                            <tr>
                            <th>id_города</th>
                            <th>Город</th>
                            <th>Дата</th>
                            <th>Температура, c</th>
                            <th>id_погоды</th>
                            </tr>""")
        if type(data) == list:
            for row in data:
                file.write('<tr>')
                try:
                    for param in row:
                        file.write('<td> {} </td>'.format(param))                
                except:
                    file.write('</tr>')
                    continue
                file.write('</tr>')

        else:
            file.write('<tr>')
            try:
                for param in data:
                    file.write('<td> {} </td>'.format(param))
            except:
                print('Объект типа None')
                file.write('</tr>')
            file.write('</tr>')

def export_to_json(data,DIR,filename):
    """Функция эеспортирует данные из БД в JSON без заголовков"""
    file = open(os.path.join(DIR,filename + '.json'), 'w',encoding = 'UTF-8')
    json.dump(data,file, indent = 2)

DIR = os.getcwd()
table_name = 'weather'
con = sql.connect(os.path.join(DIR,'openweather'))

input_info = input('Введите запрос разделяя слова пробелами. Название города вводить с большой буквы и на латинице ').split(' ')
filetype = input_info[0]
filename = input_info[1]
cityname = False
if len(input_info) == 3:
    cityname = input_info[2]

if cityname:
    data = get_db_data_by_city(cityname,con,table_name)
else:
    data = get_db_all_data(con,table_name)

if data != None:
    if filetype.lower() == 'csv':
        export_to_csv(data, DIR, filename)
        print('Данные выгружены в csv')
    elif filetype.lower() == 'json':
        export_to_json(data,DIR,filename)
        print('Данные выгружены в json')
    elif filetype.lower() == 'html':
        export_to_html(data,DIR,filename)
        print('Данные выгружены в html')
    else:
        print('Некорректный тип файла')
else:
    print('Указанного города {} не существует'.format(cityname))
