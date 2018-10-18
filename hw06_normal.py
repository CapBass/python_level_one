# Задание-1:
# Реализуйте описаную ниже задачу, используя парадигмы ООП:
# В школе есть Классы(5А, 7Б и т.д.), в которых учатся Ученики.
# У каждого ученика есть два Родителя(мама и папа).
# Также в школе преподают Учителя. Один учитель может преподавать 
# в неограниченном кол-ве классов свой определенный предмет. 
# Т.е. Учитель Иванов может преподавать математику у 5А и 6Б,
# но больше математику не может преподавать никто другой.

# Выбранная и заполненная данными структура должна решать следующие задачи:
# 1. Получить полный список всех классов школы
# 2. Получить список всех учеников в указанном классе
#  (каждый ученик отображается в формате "Фамилия И.О.")
# 3. Получить список всех предметов указанного ученика 
#  (Ученик --> Класс --> Учителя --> Предметы)
# 4. Узнать ФИО родителей указанного ученика
# 5. Получить список всех Учителей, преподающих в указанном классе

class Teacher:
    
    def __init__(self,name,surname,subject):
        self.name = name
        self.surname = surname
        self.subject = subject
class School:
    
    def __init__(self,name):
        self.name = name
        self.class_rooms = []       

    
    def add_class_room(self,name):
        self.class_rooms.append(Class_room(name,self))
   
    
    def get_class_rooms(self):
        class_rooms = []
        for class_room in self.class_rooms:
            class_rooms.append(class_room.name)
        return class_rooms        

    
    def get_class_room(self,name):
        for class_room in self.class_rooms:
            if class_room.name == name:
                return class_room
    
    def full_student_info(self,name):
        result = {}
        for class_room in self.class_rooms:
            for student in class_room.students:
                if student.name == name[0] and student.surname == name[1]:
                    result['ученик'] = student.name
                    break
            
            if result['ученик']:                
                result['класс'] = class_room.name
                
                teachers = []
                for teacher in class_room.teachers:
                    teachers.append({'ФИО':teacher.name + ' '  + teacher.surname,'Предмет': teacher.subject }) 
                
                result['учителя'] =  teachers
                return result
            
class Class_room:
    
    def __init__(self,name,school):
        self.name = name
        self.school = school
        self.students = []
        self.teachers = []
    
    def add_student(self, name, surname, mother, father):
        self.students.append(Student(name, surname, self, mother, father))
    
    def add_teacher(self, name, surname, subject):
        self.teachers.append(Teacher(name, surname, subject))
    
    def get_students(self):
        students = []
        for student in self.students:
            students.append((student.name,student.surname))
        return students
    
    def get_teachers(self):
        teachers = []
        for teacher in self.teachers:
            teachers.append((teacher.name,teacher.surname))
        return teachers
            
    def get_student(self,name):
        for student in self.students:
            if student.name == name[0] and student.surname == name[1]:
                return student
    
    def get_teacher(self,name):
        for teacher in self.teachers:
            if teacher.name == name[0] and teacher.surname == name[1]:
                return teacher 
class Student:
    
    def __init__(self, name, surname, class_room, mother, father):
        self.name = name
        self.surname = surname
        self.class_room = class_room
        self.mother = mother
        self.father = father
    
    def get_class_room(self):
        for class_room in school.class_rooms:
            for student in class_room:
                if student == self:
                    return class_room.name

#получить все классы школы					
school = School('Школа 1')
school.add_class_room('5A')
school.add_class_room('7B')
print(school.get_class_rooms())

#получить учеников указанного класса
class_5A = school.get_class_room('5A')
class_7B = school.get_class_room('7B')
class_5A.add_student('Вася','Пупкин','Пупкина Мария Викторовна','Пупкин Иван Егорович')
class_7B.add_student('Петр','Сидоров','Сидорова Валерия Ивановна','Сидоров Артем Григорьевич')
class_5A.add_teacher('Алексей','Попов','математика')
class_7B.add_teacher('Валентина','Иванова','Русский язык')
print(class_5A.get_students())
print(class_7B.get_students())

#получить информацию о предметах ученика со списком учителей
print(school.full_student_info(('Вася','Пупкин')))

#получить отца и мать ученика
student = class_5A.get_student(('Вася','Пупкин'))
print('мать:', student.mother,',', 'отец:', student.father)
print('мать:', student.mother,',', 'отец:', student.father)
