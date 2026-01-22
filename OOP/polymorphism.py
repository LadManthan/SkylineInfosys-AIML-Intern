class Complex:
    def __init__(self,real,img):
        self.real = real
        self.img = img
        
    def show(self):
        print(self.real , 'i + ' , self.img , 'j')
        
    # __add__ is the Dunder Function
    # Dunder func helps us to use func in user defined classes 
    def __add__(self,num2):
        newreal = self.real + num2.real
        newimg = self.img + num2.img
        return Complex(newreal,newimg)
        
c1 = Complex(1,3)
c1.show()

c2 = Complex(4,6)
c2.show()

c3 = c1 + c2
c3.show()
