#!/usr/bin/python3

"""
== Лото ==

Правила игры в лото.

Игра ведется с помощью специальных карточек, на которых отмечены числа, 
и фишек (бочонков) с цифрами.

Количество бочонков — 90 штук (с цифрами от 1 до 90).

Каждая карточка содержит 3 строки по 9 клеток. В каждой строке по 5 случайных цифр, 
расположенных по возрастанию. Все цифры в карточке уникальны. Пример карточки:

--------------------------
    9 43 62          74 90
 2    27    75 78    82
   41 56 63     76      86 
--------------------------

В игре 2 игрока: пользователь и компьютер. Каждому в начале выдается 
случайная карточка. 

Каждый ход выбирается один случайный бочонок и выводится на экран.
Также выводятся карточка игрока и карточка компьютера.

Пользователю предлагается зачеркнуть цифру на карточке или продолжить.
Если игрок выбрал "зачеркнуть":
	Если цифра есть на карточке - она зачеркивается и игра продолжается.
	Если цифры на карточке нет - игрок проигрывает и игра завершается.
Если игрок выбрал "продолжить":
	Если цифра есть на карточке - игрок проигрывает и игра завершается.
	Если цифры на карточке нет - игра продолжается.
	
Побеждает тот, кто первый закроет все числа на своей карточке.

Пример одного хода:

Новый бочонок: 70 (осталось 76)
------ Ваша карточка -----
 6  7          49    57 58
   14 26     -    78    85
23 33    38    48    71   
--------------------------
-- Карточка компьютера ---
 7 11     - 14    87      
      16 49    55 77    88    
   15 20     -       76  -
--------------------------
Зачеркнуть цифру? (y/n)

Подсказка: каждый следующий случайный бочонок из мешка удобно получать 
с помощью функции-генератора.

Подсказка: для работы с псевдослучайными числами удобно использовать 
модуль random: http://docs.python.org/3/library/random.html

"""
#класс мешка с бочонками для получения случайного бочонка из мешка
class Bag_of_kegs:
    
    def __init__(self,n_kags = 90):
        self.n_kags = n_kags
        self.__kag_list = list(range(1,self.n_kags + 1))    
  
    #случайно перемешиваем мешок с бочонками и достаем случайный, затем удаляем бочонок из мешка
    def get_keg(self):
        import random
        random.shuffle(self.__kag_list)    
        keg = random.choice(self.__kag_list)
        self.__kag_list.remove(keg)    
        return keg
    #наполняем бочонок
    def fill_bag(self):
        self._kag_list = list(range(1,self.n_kags + 1))

#класс, который описывает свойста и методы карты лото
class Loto_card:
    
    def __init__(self,rows = 3,cols = 9,n_nums = 90):
        self.rows = rows
        self.cols = cols
        self.n_nums = n_nums
        #служебный список для генерации чисел на карте
        self.__num_list = list(range(1,self.n_nums + 1))
        #константа, сколько чисел в строке карты
        self.NUMS_IN_ROW = 5
        self._card = []
        self._win = False
    #служебная функция - генератор чисел для строки карты
    def __fill_row_nums(self):
        import random
        result = {}
        cols = list(range(0,self.cols))        
        
        for num in range(0,self.NUMS_IN_ROW):            
            idx = random.choice(cols)
            value = random.choice(self.__num_list)            
            result[idx] = value
            self.__num_list.remove(value)
            cols.remove(idx)
        
        return result
            
    #метод создает новую карту лото в виде многомерного массива
    def new_card(self):        
        self._card = []
        for row in range(0,self.rows):
            fill_row = []
            fill_row_nums = self.__fill_row_nums()
            
            for col in range(0,self.cols):
                if fill_row_nums.get(col) == None:
                    fill_row.append('_')
                else:
                    fill_row.append(fill_row_nums.get(col))
            
            self._card.append(fill_row)
        
        return self._card
    #доступ к массиву карты лото  
    @property
    def card(self):
        return self._card
    #свойство, проверяющее, зачеркнуты ли все числа и есть ли победа
    @property
    def win(self):
        self._win = True
        for row in self.card:
            for col in row:
                if col != '_' and col != 'X':
                    self._win = False
        return self._win
    #метод, который зачеркивает цифру по бочонку
    def paint_up(self,keg):
        for idx_row,row in enumerate(self.card):
            for idx_col,col in enumerate(row):
                if keg == col:
                    self.card[idx_row][idx_col] = 'X'
        return self.card
    #отрисовка карты лото
    def draw_card(self):
        card_str = '======================\n'
        for row in self.card:
            row_str = ','.join([str(x) for x in row]) + '\n'           
            card_str += row_str
        card_str += '======================\n'
        return card_str
    #метод, который проеряет наличие числа бочонка в карте лото
    def keg_in_card(self,keg):
        keg_in_card = False
        for row in self.card:
            for col in row:
                if col == keg:
                    keg_in_card = True
                    return keg_in_card
        return keg_in_card

#функция, которая очищает выход в консоли. Расскоментировать, если нужно
#def clear_output():
    #import os
   # os.system('cls')
   
#Начинаем игру    
while True:
    game_start = input('Хотите сыграть в лото, \'X/Y\' ')
    
    if game_start == 'X':
        bag_of_kegs = Bag_of_kegs()
        
        player_card = Loto_card()
        computer_card = Loto_card()
        
        player_card.new_card()
        computer_card.new_card()
        
        
        while True:
            #clear_output()
            keg = bag_of_kegs.get_keg()
            print('Новый бочонок: ',keg)
            print('ваша карточка')
            print(player_card.draw_card())
            print('Карточка кмпьютера')
            print(computer_card.draw_card())
            
            action = input('Зачеркнуть число? (y/n) ')
            if action == 'y':
                
                if player_card.keg_in_card(keg) == True:
                    player_card.paint_up(keg)
                    if player_card.win:
                        print('Вы победили')
                        break
                else:
                    print('Вы проиграли')
                    break
                
                if computer_card.keg_in_card(keg) == True:
                    computer_card.paint_up(keg)
                    if computer_card.win:
                        print('Победил компьютер')
                        break
              
            elif action == 'n':
                
                if computer_card.keg_in_card(keg) == True:
                    computer_card.paint_up(keg)
                    if computer_card.win:
                        print('Победил компьютер')
                        break
                else:         
                    continue
            else:
                print('Неизвестная команда, игра будет завершена')
                break
    
    
    else:
        print('Выход...')
        break