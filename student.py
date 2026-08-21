def rank_students(students):

    students.sort(key=lambda x: x[2], reverse=True)

    for i in range(len(students)):

        if i == 0:
            rank = 1

        elif students[i][2] == students[i-1][2]:
            rank = students[i-1][5]

        else:
            rank = i + 1

        students[i].append(rank)

    return students
