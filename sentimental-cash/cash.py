from cs50 import get_float

while True:
    cash = get_float("Change: ")
    if (cash > 0):
        break

count = 0
cash = int(cash * 100)

while cash > 0:
    if (cash - 25 >= 0):
        count += 1
        cash = cash - 25
    elif (cash - 10 >= 0):
        count += 1
        cash = cash - 10
    elif (cash - 5 >= 0):
        count += 1
        cash = cash - 5
    elif (cash - 1 >= 0):
        count += 1
        cash = cash - 1
print(count)
