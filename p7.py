from datetime import datetime


class Course:
    def __init__(self, code, day, start_time, end_time):
        self.code = code
        self.day = day
        self.start_time = start_time
        self.end_time = end_time

        
        self.start = datetime.strptime(start_time, "%H:%M")
        self.end = datetime.strptime(end_time, "%H:%M")

        if self.start >= self.end:
            raise ValueError("End time must be after start time.")

    def __str__(self):
        return (f"Course: {self.code}, Day: {self.day}, "
                f"Time: {self.start_time}-{self.end_time}")


class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.courses = []

    def register_course(self, course):
        self.courses.append(course)

    def check_conflicts(self):
        conflicts = []

        for i in range(len(self.courses)):
            for j in range(i + 1, len(self.courses)):
                c1 = self.courses[i]
                c2 = self.courses[j]

                if (c1.day.lower() == c2.day.lower()
                        and c1.start < c2.end
                        and c2.start < c1.end):
                    conflicts.append((c1, c2))

        return conflicts

    def __str__(self):
        return (f"\nStudent ID: {self.student_id}\n"
                f"Student Name: {self.name}\n"
                f"Total Registered Courses: {len(self.courses)}")


try:
    n = int(input("Enter number of students: "))

    if n <= 0:
        raise ValueError("Number of students must be positive.")

    for i in range(n):
        print(f"\n--- Student {i + 1} ---")

        sid = input("Enter Student ID: ")
        name = input("Enter Student Name: ")
        student = Student(sid, name)

        count = int(input("Enter number of courses: "))

        if count <= 0:
            raise ValueError("Number of courses must be positive.")

        for j in range(count):
            print(f"\nCourse {j + 1}")

            code = input("Enter Course Code: ")
            day = input("Enter Day (Monday-Sunday): ").strip()

            if day.lower() not in [
                "monday", "tuesday", "wednesday", "thursday",
                "friday", "saturday", "sunday"
            ]:
                raise ValueError("Invalid day entered.")

            start = input("Enter Start Time (HH:MM): ")
            end = input("Enter End Time (HH:MM): ")

            course = Course(code, day, start, end)
            student.register_course(course)

        
        print("\nStudent Details")
        print(student)

        
        conflicts = student.check_conflicts()

        if conflicts:
            print("\nConflicting Course Pairs:")
            for c1, c2 in conflicts:
                print(f"{c1.code} conflicts with {c2.code}")
        else:
            print("\nNo course conflicts found.")

        
        print("\nStudent Timetable:")
        for course in student.courses:
            print(course)

except ValueError as e:
    print("Invalid Input:", e)

except Exception as e:
    print("An error occurred:", e)