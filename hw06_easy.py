# Задача-1: Написать класс для фигуры-треугольника, заданного координатами трех точек.
# Определить методы, позволяющие вычислить: площадь, высоту и периметр фигуры.
class Triangle:
    def __init__(self,A,B,C):
        self.A = A
        self.B = B
        self.C = C
        self.AC = ((self.C[0] - self.A[0])**2 + (self.C[1] - self.A[1])**2)**0.5
        self.AB = ((self.B[0] - self.A[0])**2 + (self.B[1] - self.A[1])**2)**0.5
        self.BC = ((self.C[0] - self.B[0])**2 + (self.C[1] - self.B[1])**2)**0.5

    def get_square (self): 
        return 0.5 * abs((self.A[0] - self.C[0]) * (self.B[1] - self.C[1]) - (self.B[0] - self.C[0]) * (self.A[1] - self.C[1]))
    
    def get_height(self):        
        return 2 * self.get_square()/self.AC
    
    def get_perimeter(self):
        return self.AC + self.AB + self.BC

# Задача-2: Написать Класс "Равнобочная трапеция", заданной координатами 4-х точек.
# Предусмотреть в классе методы:
# проверка, является ли фигура равнобочной трапецией;
# вычисления: длины сторон, периметр, площадь.

class Trapezium:
    def __init__(self, A,B,C,D):
        self.A = A
        self.B = B
        self.C = C
        self.D = D
    
    def get_length(self, O1,O2):
        return ((O2[0] - O1[0])**2 + (O2[1] - O1[1])**2)**0.5  
        
    
    def get_square(self):
        BC = self.get_length(self.B,self.C)        
        AD = self.get_length(self.D,self.A)
        h = abs(AD - self.A[0])        
        return (BC + AD)/2 * h
    
    def is_equi_trapezium(self):
        AB = self.get_length(self.B,self.A)
        CD = self.get_length(self.D,self.C)        
        if AB == CD:
            return True
        else:
            return False
    
    def get_perimeter(self):
        AB = self.get_length(self.B,self.A)
        BC = self.get_length(self.B,self.C)
        CD = self.get_length(self.D,self.C)
        AD = self.get_length(self.D,self.A)
        return AB + BC + CD + AD
