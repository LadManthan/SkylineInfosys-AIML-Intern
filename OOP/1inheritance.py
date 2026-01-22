print("\nSuper keyword for Constructer : \n")
class Phone():
    def __init__(self, price, brand, camera):
        print("Inside Phone class")
        self.price = price
        self.brand = brand
        self.camera = camera
        
class SmartPhone(Phone):
    def __init__(self, price, brand, camera, os, battery):
        print("Inside Smart Phone class")
        
        #using super() to access Phone class
        super().__init__(price, brand, camera)  #the paramters are passed to Phone class <-------|
        self.os = os    #                                                                        |
        self.battery = battery  #                                                                |
        print("Inside Smart Phone class")  #                                                     |
#here we are creating object of Phone class only                                                 |
p = Phone(20000, 'Samsug', '48 MP')  #                                                           |
#                                                                                                |
#here we are creating object of SmartPhone class and passing parameters of phone class as well---|
s = SmartPhone(20000, 'Samsug', '48 MP', "Android", "5000 mAh")


print("\n\nSuper keyword for methods\ : n")
class A:
    def __init__(self,n1,n2):
        self.x=n1
        self.y=n2

    def add(self):
        print("Inside class A")
        print(self.x+self.y)

class B(A) :
    def __init__(self, n1, n2):
        self.x=n1
        self.y=n2

    def add(self):
        print("inside classs B")
        
        #super keyword is used to access methods of parent class
        super().add()
        
a = A(5,5)
a.add()

b = B(15,5)
b.add()
