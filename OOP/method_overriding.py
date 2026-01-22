class A:
    def print_msg(self):
        print("This is class A")
        
class B(A):
    
    #same function as of class A
    #the method 'print_msg' is overriden
    def print_msg(self):
        print("This is Class B")
    
a = A()
b = B()

a.print_msg()
b.print_msg()