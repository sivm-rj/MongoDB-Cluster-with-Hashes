import random
import csv

random.seed(123)
def generate_student_data(num_students):
    # Define possible majors
    majors = ['Computer Science', 'Mechanical Engineering', 'English', 'Biology', 'Psychology', 'History']
    
    # Define column headers
    headers = ['Name', 'Age', 'Major', 'GPA']
    
    # Initialize list to store student data
    student_data = []
    
    # Generate unique names for students
    names = set()
    x = 0
    while len(names) < num_students:
        name = 'Student{}'.format(x)
        names.add(name)
        x = x + 1
    
    # Generate student data
    for name in names:
        age = random.randint(18, 24)
        major = random.choice(majors)
        gpa = round(random.uniform(2.5, 4.0), 2)
        student_data.append([name, age, major, gpa])
    
    # Write data to CSV file
    with open('students.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(student_data)


generate_student_data(10000)

