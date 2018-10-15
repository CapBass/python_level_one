# Задача-1:
# Напишите небольшую консольную утилиту,
# позволяющую работать с папками текущей директории.
# Утилита должна иметь меню выбора действия, в котором будут пункты:
# 1. Перейти в папку
# 2. Просмотреть содержимое текущей папки
# 3. Удалить папку
# 4. Создать папку
# При выборе пунктов 1, 3, 4 программа запрашивает название папки
# и выводит результат действия: "Успешно создано/удалено/перешел",
# "Невозможно создать/удалить/перейти"

# Для решения данной задачи используйте алгоритмы из задания easy,
# оформленные в виде соответствующих функций,
# и импортированные в данный файл из easy.py
import os
import hw05_easy as easy

def move_to_directory(dir_name):   
    path = os.path.join(os.getcwd(),dir_name)
	try:
		os.chdir(path)
		print('Вы успешно перешли в директорию ',path)
	except FileExistsError:
		print('Не удалось перейти в директорию')

def show_commands():
	commands = [
		'1: Перейти в директорию',
		'2: Посмотреть содержимое директории',
		'3: Удалить папку',
		'4: Создать папку',
		'0 выход'
	]
	for command in commands:
		print(command)

while True:
	
	show_commands()
	
	command = input('Введите комманду ')
	
	if command == '1':
		dir_name = input('Укажите директорию для перемещения')
		move_to_directory(dir_name)
	elif command == '2':
		easy.show_listdir()
	elif command == '3':
		dir_name = input('Укажите директорию для удаления')
		easy.delete_directory(dir_name)
	elif command == '4':
		dir_name = input('Укажите директорию для создания')
		easy.create_directory(dir_name)
	elif command == '0':
		break
	else:
		print('Недопустимая команда')

		