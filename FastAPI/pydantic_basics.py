from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Optional, Dict, Annotated


class Address(BaseModel):
    street:str
    city:str
    state:str
    zip_code:str = Field(pattern=r"^\d{6}$")  #6 digit zip code only


class Student(BaseModel):
    name:Annotated[str, Field(max_length=20, title="Students Name", description="Please enter students name in less than 20 characters.")]
    enrollment_no:str
    age:int = Field(gt=18, lt=30)  #18<age<30
    address:Address  #nested model
    email:EmailStr  #email
    intrests:List[str] = Field(max_length=5)  #max 5 intrests only
    contact:Dict[str,str]  #dictionary where key,values are str
    github:AnyUrl = None  #if we dont pass then default value is None
    married:Optional[str] = False #optional field, dont pass:False, pass:str

    
    #field validation
    @field_validator('email')
    @classmethod
    def validate_email(cls, email):
        valid_domain = 'scet.ac.in'
        domain = email.split('@')[-1]  # -1 coz it will return 2 parts, before and after @
        
        if domain != valid_domain:
            raise ValueError("Not valid email!!")
        return email
    
    
def add_student(student : Student):
    print('-'*40)
    print(f"Name : {student.name}")
    print(f"Enrollment no. : {student.enrollment_no}")
    print(f"Age : {student.age}")
    print(f"Address : {student.address}")
    print(f"Email : {student.email}")
    print(f"Intrests : {student.intrests}")
    print(f"Contact : {student.contact}")
    print(f"Github : {student.github}")
    print(f"Married : {student.married}")
     

address_dict = {'street':'Pal','city':'SUrat','state':'Gujarat','zip_code':'123456'}
address1 = Address(**address_dict)
student1 = {
    'name':'Manthan',
    'enrollment_no':'C001',
    'age':22,
    'address':address1,
    'email':'manthan@scet.ac.in',
    'intrests':['AI/ML','Drawing'],
    'contact':{'phone':'1111111111','tel phone':'1234'},
    'github':'https://github.com/ManthanLad'
    }

address_dict = {'street':'Vesu','city':'SUrat','state':'Gujarat','zip_code':'654321'}
address2 = Address(**address_dict)
student2 = {
    'name':'Manendra',
    'enrollment_no':'C002',
    'age':23,
    'address':address2,
    'email':'manendra@scet.ac.in',
    'intrests':['AI/ML','Gaming'],
    'contact':{'phone':'2222222222','tel phone':'4321'},
    'married':'maybe'
    }


student = Student(**student1)  #pass the student_info dict as a argument
add_student(student)

student = Student(**student2)  
add_student(student)
print(type(student))  #pydantic object

temp = student.model_dump()
print(temp)
print(type(temp))  #python dictionary