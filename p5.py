students = []

n = int(input("Enter number of students: "))

if n != 5:
    print("Error:Only 5 student allowed..")
    exit()

for i in range(n):
    print(f"\nEnter details of Student {i+1}")

    roll = int(input("Roll No: "))
    name = input("Name: ")

    marks = []
    for j in range(5):
        mark = float(input(f"Subject {j+1} Marks: "))
        marks.append(mark)

    total = sum(marks)
    percentage = total / 5

    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 50:
        grade = "D"
    else:
        grade = "F"

    students.append([roll, name, marks, total, percentage, grade])

students.sort(key=lambda x: x[3], reverse=True)

rank = 1

for i in range(len(students)):
    if i > 0 and students[i][3] == students[i-1][3]:
        students[i].append(students[i-1][6])
    else:
        students[i].append(i + 1)

print("\nSTUDENT RESULT")
print("Rank\tRoll\tName\tTotal\tPercentage\tGrade")

for s in students:
    print(f"{s[6]}\t{s[0]}\t{s[1]}\t{s[3]}\t{s[4]:.2f}%\t{s[5]}")