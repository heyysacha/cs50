from cs50 import get_int

while True:
    height = get_int("Height: ")
    if (8 >= height >= 1):
        break


for i in range(height):
    for j in range(height):
        if (height > i + j + 1):
            print(" ", end="")
        else:
            print("#", end="")
    print()
