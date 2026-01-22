class ATM():
    
    def __init__(self):
        
        #encapsulation
        # __variable makes it private and we cannot access it from outside the class
        self.__pin = None
        self.__balance = 0
        self.menu()
        
    def menu(self):
        user_input = int(input("""\n
        ---------MENU-------- : 
        1.Create Accont
        2.Change PIN
        3.Check Balance
        4.Withdraw
        5.Deposit 
        
        Enter choise : """))
        
        if user_input == 1:
            self.create_account()
            
        elif user_input == 2:
            self.change_pin()
            
        elif user_input == 3:
            self.check_balance()
        
        elif user_input == 4:
            self.withdraw()
        
        elif user_input == 5:
            self.deposit()
        
        else : 
            exit()
    
    def alert_msg(self):
        print("\nInsufficient Balance!!")
        self.menu()
         
    def create_account(self):
        user_pin = int(input("Enter PIN : "))
        self.pin = user_pin
        
        user_balance = int(input("Enter balance : "))
        self.balance = user_balance
        self.menu()
        
    def change_pin(self):
        user_pin = int(input("\nEnter your current PIN : "))
        
        if user_pin == self.pin :
            new_pin = int(input("\nEnter new PIN : "))
            self.pin = new_pin
            print("PIN changed successfully")
            self.menu()
        else : 
            print("\nEnter correct PIN!")
        
    def check_balance(self):
        user_pin = int(input("Enter your PIN : "))
        if user_pin == self.pin :
            print(f"Your balance is : {self.balance}")
            self.menu()
        else :
            print("Enter valid PIN!")
            self.menu()
    
    def withdraw(self):
        user_pin = int(input("Enter your PIN : "))
        if user_pin == self.pin :
            amount = int(input("\nEnter amount to withdraw : "))
            if amount > self.balance : 
                print("\nInsufficient balance!!")
                self.menu()
            else : 
                self.balance -= amount
                print(f"{amount} is withdrawn")
                self.menu()
        else :
            print("Enter vald PIN")
            self.menu()
            
    def deposit(self):
        user_pin = int(input("Enter your PIN : "))
        if user_pin == self.pin :
            amt = int(input("\nEnter amount to deposit : "))
            self.balance += amt
            print(f"\n{amt} deosited")
            self.menu()
        else : 
            self.alert_msg()
            
p1 = ATM()