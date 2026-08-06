p = input("Enter Password: ")

if not any(i.isupper() for i in p):
    print("Uppercase missing")

if not any(i.islower() for i in p):
    print("Lowercase missing")

if not any(i.isdigit() for i in p):
    print("Digit missing")

if not any(i in "@#$%^&*!?" for i in p):
    print("Special character missing")

for i in range(len(p)-1):
    if p[i] == p[i+1]:
        print("Repeated consecutive characters")
        break