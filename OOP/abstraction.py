from abc import ABC, abstractmethod

class Person(ABC):
    
    @abstractmethod
    def role(self):
        pass
    
    @abstractmethod
    def salary(self):
        pass
    
class Teacher(Person):
    
    def role(self):
        print("You are a Teacher.")
        
    def salary(self):
        print("Your salary is 25000")
        
class Student(Person):
    def role(Self):
        print("You are a student.")
        
    #if you dont write the salary method then it will generate an error
    def salary(self):
        print("Students dont get salary, they hae to pay fees")

'''
p = Person()
p.role() 
this will generate an error :
"Can't instantiate abstract class Person with abstract method role"
you need to implemet the abstract method in subclass '''

t = Teacher()
t.role()

s = Student()
s.role()
