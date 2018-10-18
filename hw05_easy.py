# Задача-1:
# Напишите скрипт, создающий директории dir_1 - dir_9 в папке,
# из которой запущен данный скрипт.
# И второй скрипт, удаляющий эти папки.
import os

def create_directory(f_name):
    dir_path = os.path.join(os.getcwd(),f_name)
    try:
        os.mkdir(dir_path)
        print('Директория успешно создана')
    except FileExistsError:
        print('Такая директория уже существует')

def delete_directory(f_name):
    dir_path = os.path.join(os.getcwd(),f_name)
    try:
        os.rmdir(dir_path)
        print('Директория успешно удвлена')
    except FileExistsError:
        print('Директория уже удалена')

def create_dir_9():
    i = 1
    while i <= 9:
        f_name = 'dir_' + str(i)
        create_directory(f_name)
        i += 1
        
def delete_dir_9():
    i = 1
    while i <= 9:
        f_name = 'dir_' + str(i)
        delete_directory(f_name)
        i += 1

# Задача-2:
# Напишите скрипт, отображающий папки текущей директории.


def show_listdir():
    directories = os.listdir(os.getcwd())
    for dir in directories:
        dir_path = os.path.join(os.getcwd(),dir)
        if os.path.isdir(dir_path):
            print(dir)


# Задача-3:
# Напишите скрипт, создающий копию файла, из которого запущен данный скрипт.


def copy_file():
    file_name = os.path.basename(__file__)

    with open(os.path.join(os.getcwd(),file_name),'r',encoding='UTF-8') as current_f:
        with open(os.path.join(os.getcwd(), 'copy_file.py'), 'w', encoding='UTF-8') as copy_f:
            copy_f.write(current_f.read())