n = int(input("Enter value of N: "))

roll = []

print("Enter", n - 1, "roll numbers:")
for i in range(n - 1):
    roll.append(int(input()))

total = n * (n + 1) // 2
missing = total - sum(roll)

print("Missing Roll Number =", missing)