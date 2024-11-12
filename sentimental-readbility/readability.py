from cs50 import get_string

text = get_string("Text: ")

words = 1
sentences = 0
letters = 0

for i in range(len(text)):
    if (text[i].isalpha()):
        letters += 1
    if (text[i].isspace()):
        words += 1

sentences = sentences + text.count('.')
sentences = sentences + text.count('!')
sentences = sentences + text.count('?')

index = round(0.0588 * ((letters / words) * 100) - 0.296 * ((sentences / words) * 100) - 15.8)

if (index < 1):
    print("Before Grade 1")
elif (index < 16):
    print("Grade ", index)
else:
    print("Grade 16+")
