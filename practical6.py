from students import get_students
from ranking import rank_students
from report import display

try:
    n = int(input("Enter number of students: "))

    students = []

    for i in range(n):
        print("\nStudent", i + 1)
        students.append(get_studentsa())

    students = rank_students(students)
    display(students)

except ValueError:
    print("Invalid input")
