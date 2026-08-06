n = int(input("Enter number of elements: "))

arr = []

print("Enter elements:")
for i in range(n):
    arr.append(int(input()))

print("Consecutive duplicate numbers are:")

for i in range(n - 1):
    if arr[i] == arr[i + 1]:
        if i == 0 or arr[i] != arr[i - 1]:
            print(arr[i]) 