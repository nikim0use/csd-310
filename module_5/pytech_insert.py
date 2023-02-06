""" 
    Title: pytech_insert.py
    Author: Kristin Bougrine
    Date: January 15, 2023
    Description: Test program for inserting new documents 
     into the students collection 
"""

""" import statements """
from pymongo import MongoClient

# MongoDB connection string 
url = "mongodb+srv://admin:admin@cluster0.k7xyaiu.mongodb.net/?retryWrites=true&w=majority"

# connect to the MongoDB cluster 
client = MongoClient(url)

# connect pytech database
db = client.pytech

""" three student documents"""
# Frances Lowe's data document 
frances = {
    "student_id": "1007",
    "first_name": "Frances",
    "last_name": "Lowe",
    "enrollments": [
        {
            "term": "Fall 2022",
            "gpa": "3.7",
            "start_date": "August 23, 2023",
            "end_date": "December 20, 2022",
            "courses": [
                {
                    "course_id": "CS 345",
                    "description": "Computer Science",
                    "instructor": "Molly Mounds",
                    "grade": "B+"
                },
                {
                    "course_id": "MA 376",
                    "description": "College Algebra",
                    "instructor": "Joy Page",
                    "grade": "A"
                }
            ]
        }
    ]

}

# Sophia Parrish data document 
sophia = {
    "student_id": "1008",
    "first_name": "Sophia",
    "last_name": "Parrish",
    "enrollments": [
        {
            "term": "Fall 2022",
            "gpa": "3.82",
            "start_date": "August 23, 2022",
            "end_date": "December 20, 2022",
            "courses": [
                {
                    "course_id": "CS 447",
                    "description": "Advanced Computer Science",
                    "instructor": "Chris Green",
                    "grade": "A"
                },
                {
                    "course_id": "CS 340",
                    "description": "Programming with C#",
                    "instructor": "Selena Byrd",
                    "grade": "A-"
                }
            ]
        }
    ]
}

# Vera Hunt data document
vera= {
    "student_id": "1009",
    "first_name": "Vera",
    "last_name": "Hunt",
    "enrollments": [
        {
            "term": "Fall 2022",
            "gpa": "3.0",
            "start_date": "August 23, 2022",
            "end_date": "December 20.2022",
            "courses": [
                {
                    "course_id": "CS 310",
                    "description": "Database Security",
                    "instructor": "Zelda Parker",
                    "grade": "B"
                },
                {
                    "course_id": "CS 420",
                    "description": "IT Auditing",
                    "instructor": "Stan Davidson",
                    "grade": "B+"
                }
            ]
        }
    ]
}

# get the students collection 
students = db.students

# insert statements with output 
print("\n  -- INSERT STATEMENTS --")
frances_student_id = students.insert_one(frances).inserted_id
print("  Inserted student record Frances Lowe into the students collection with document_id " + str(frances_student_id))

sophia_student_id = students.insert_one(sophia).inserted_id
print("  Inserted student record Sophia Parrish into the students collection with document_id " + str(sophia_student_id))

vera_student_id = students.insert_one(vera).inserted_id
print("  Inserted student record Vera Hunt into the students collection with document_id " + str(vera_student_id))

input("\n\n  End of program, press any key to exit... ")