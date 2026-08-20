def display(students):
    print("Rank\tRoll No\tName\tTotal\tPercentage\tGrade")

    for s in students:
        print(s[5], "\t", s[0], "\t", s[1], "\t", s[2], "\t", s[3], "\t\t", s[4])