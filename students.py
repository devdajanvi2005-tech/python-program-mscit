def get_students():
    roll = int(input("Enter roll no: "))
    name = input("Enter name: ")

    m1 = int(input("Enter sub1 marks: "))
    m2 = int(input("Enter sub2 marks: "))
    m3 = int(input("Enter sub3 marks: "))
    m4 = int(input("Enter sub4 marks: "))
    m5 = int(input("Enter sub5 marks: "))

    total = m1 + m2 + m3 + m4 + m5
    per = total / 5

    if per >= 90:
        grade = "A"
    elif per >= 80:
        grade = "B"
    elif per >= 70:
        grade = "C"
    elif per >= 60:
        grade = "D"
    else:
        grade = "E"

    return [roll, name, total, per, grade]