import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"

st.title("Student Management System")

menu = st.sidebar.selectbox(
    "Menu",    
    [
        "View Students",
        "Search Student",
        "Create Student",
        "Update Student",
        "Delete Student",
        "Sort Students"
    ]
)


# ---------------- VIEW STUDENTS ----------------
if menu=='View Students':
    if st.button("Load Students"):
        response = requests.get(f"{BASE_URL}/view_students")

        if response.status_code == 200:
            data = response.json()

            df = pd.DataFrame.from_dict(data, orient="index")
            df.reset_index(inplace=True)
            df.rename(columns={"index": "student_id"}, inplace=True)

            st.dataframe(df)
        else:
            st.error("Error loading data!!")


# ---------------- SEARCH STUDENT ----------------
elif menu=='Search Student':
    student_id = st.text_input("Enter id of student to search :")

    if st.button("Search"):
        response = requests.get(f"{BASE_URL}/search_students/{student_id}")

        if response.status_code == 200:
            data = response.json()

            df = pd.DataFrame([data])
            df.insert(0, "student_id", student_id)

            st.dataframe(df)

        else:
            st.error(f"{response.status_code} - {response.json()['detail']}")


# ---------------- CREATE STUDENT ----------------
elif menu=='Create Student':
    st.subheader("Create new student")

    student_id = st.text_input("Student ID")
    enrollment_no = st.text_input("Enrollment No.")
    name = st.text_input("Name")
    year = st.number_input("Year",min_value=0, max_value=5, step=1)
    email = st.text_input("Email")
    phone = st.text_input("Phone No.")
    cgpa = st.number_input("CGPA")

    if st.button("Create Student"):

        payload = {
            "id": student_id,
            "enrollment_no": enrollment_no,
            "name": name,
            "year": year,
            "email": email,
            "phone": phone,
            "cgpa": cgpa
        }

        response = requests.post(f"{BASE_URL}/create_student",json=payload)

        if response.status_code == 201:
            st.success("Student created successfully!")
        else: 
            st.error(response.json()['detail'])


# ---------------- UPDATE STUDENT ----------------
elif menu == "Update Student":

    st.subheader("Update Student")

    student_id = st.text_input("Student ID")

    enrollment_no = st.text_input("Enrollment Number")
    name = st.text_input("Name")
    year = st.number_input("Year", min_value=1, max_value=4)
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0)

    if st.button("Update Student"):

        payload = {}

        if enrollment_no:
            payload["enrollment_no"] = enrollment_no
        if name:
            payload["name"] = name
        if year:
            payload["year"] = year
        if email:
            payload["email"] = email
        if phone:
            payload["phone"] = phone
        if cgpa:
            payload["cgpa"] = cgpa

        response = requests.put(
            f"{BASE_URL}/update_student/{student_id}",
            json=payload
        )

        if response.status_code == 201:
            st.success("Student updated successfully")
        else:
            st.error(response.json()["detail"])


# ---------------- DELETE STUDENT ----------------
elif menu == "Delete Student":

    student_id = st.text_input("Student ID")

    if st.button("Delete"):

        response = requests.delete(
            f"{BASE_URL}/delete_student/{student_id}"
        )

        if response.status_code == 201:
            st.success("Student deleted successfully")
        else:
            st.error(response.json()["detail"])


# ---------------- SORT STUDENTS ----------------
elif menu == "Sort Students":

    sort_by = st.selectbox("Sort By", ["year", "cgpa"])
    order = st.selectbox("Order", ["asc", "desc"])

    if st.button("Sort"):

        response = requests.get(
            f"{BASE_URL}/sort_students",
            params={"sort_by": sort_by, "order": order}
        )

        if response.status_code == 200:

            data = response.json()

            rows = []
            for student_id, info in data:
                info["student_id"] = student_id
                rows.append(info)

            df = pd.DataFrame(rows)

            st.dataframe(df)

        else:
            st.error(response.json()["detail"])