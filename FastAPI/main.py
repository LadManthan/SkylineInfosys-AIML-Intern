from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, Field, field_validator, EmailStr
from fastapi.responses import JSONResponse
from typing import List,Dict,Optional,Annotated
import uvicorn
import json

app = FastAPI()


class Student(BaseModel):
    id : Annotated[str, Field(..., description='ID of the student', examples=['S001'])]
    enrollment_no : Annotated[str, Field(..., description='students enrollment number')]
    name:Annotated[str, Field(..., description='name ofthe student')]
    year : Annotated[int, Field(..., description='year in which student is studing')]
    email : Annotated[EmailStr, Field(..., description='students email')]
    phone : Annotated[str, Field(..., description='students phone')]
    cgpa : Annotated[float, Field(..., description='Students latest cgpa')]


class StudentUpdate(BaseModel):
    enrollment_no : Annotated[Optional[str], Field(None, description='students enrollment number')]
    name : Annotated[Optional[str], Field(None, description='name ofthe student')]
    year : Annotated[Optional[int], Field(None, description='year in which student is')]
    email : Annotated[Optional[EmailStr], Field(None, description='students email')]
    phone : Annotated[Optional[str], Field(None, description='students phone')]
    cgpa : Annotated[Optional[float], Field(None, description='Students latest cgpa')]


#function to load data
def load_data():
    with open("students.json","r") as f:
        data = json.load(f)
        return data

#function to save data
def save_data(data):
    with open("students.json", "w") as f:
        json.dump(data,f) 


@app.get("/")
def home():
    return {"message": "Welcome to the Student API!"}


@app.get("/about")
def about():
    return {"message":"This is API example to manage students data"}


@app.get("/view_students")
def view_students():
    data = load_data()
    return data


@app.get("/search_students/{student_id}")
def search_students(student_id : str = Path(..., description="ID of student to search", examples=["S001"])):
    data = load_data()
    
    if student_id in data:
        return data[student_id]
    else:
        #return {"message":"Student not found."} --> this will show HTTP 200 status code even if data not found. it should show 404
        raise HTTPException(status_code=404, detail="Student not found!!")


@app.get("/sort_students")
def sort_students(sort_by : str = Query(..., description="Sort students by year or CGPA"), order : str = Query("asc", description='Sort in ascending or descding order')):
    data = load_data()
    
    valid_sort_by = ["year","cgpa"]
    
    if sort_by not in valid_sort_by:
        raise HTTPException(status_code=400, detail=f"Invalid sort by field!!\n Select from {valid_sort_by}")
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400, detail="Invalid order!!\n Oder by ascending or descending only!!")
    reverse = True if order == 'desc' else False
    
    
    sorted_students = sorted(data.items(), key=lambda x : x[1][sort_by], reverse = reverse)
    return sorted_students


@app.post("/create_student")
def create_student(student : Student):
    data = load_data()

    #if student already exist raise error
    if student.id in data:
        raise HTTPException(status_code=400, detail="Student already exists!!")

    #convert pydantic object into dictionary and then add to data
    data[student.id] = student.model_dump(exclude=['id'])
    save_data(data)
    
    return JSONResponse(status_code=201, content={'message':'Student info added successfully!!'})

@app.put("/update_student/{student_id}")
def update_student(student_id : str, student_update : StudentUpdate):
    data = load_data()
    
    if student_id not in data :
        raise HTTPException(status_code=404, detail="Student not found!!")
    
    existing_student_info = data[student_id]
    updated_student_info = student_update.model_dump(exclude_unset=True)  #this will return only those fields which are provided in request body and ignore the rest of the fields
    
    for key,value in updated_student_info.items():
        existing_student_info[key] = value
    
    #add new data to existing student id
    data[student_id] = existing_student_info
    save_data(data)
    
    return JSONResponse(status_code=201, content={'message':'Student info updated successfully!!'})
    
    
@app.delete("/delete_student/{student_id}")    
def delete_student(student_id : str):
    data = load_data()
    
    if student_id not in data:
        raise HTTPException(status_code=404, detail="Student not found!!")
    
    del data[student_id]
    save_data(data)
    
    return JSONResponse(status_code=201, content={'message':'Student info deleted successfully!!'})
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    