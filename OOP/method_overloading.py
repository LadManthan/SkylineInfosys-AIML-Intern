#Python does not support method overloading by default. 
#If you define multiple methods with the same name, only the latest definition will be used.

class shape:
    def area(self,r) :
        return 3.14*r*r
    
    def area(self,l,b):
        return l*b

a = shape()
#print(a.area(2))  #this wont execute and generate error
print(a.area(2,3))

class Shape:
    def area(self,a,b=0):
        if b==0:
            return 3.14*a*a
        else :
            return a*b
        
b = Shape()
print(b.area(2,0))
print(b.area(2,3))