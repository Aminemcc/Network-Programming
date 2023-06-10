def make_list(number):
    names = []
    for item in number :
        names.append(input("Enter your name with a capital letter."))
    return names

number =int(input("How many names need to be entered?"))
names = make_list([i for i in range(number)])
for name in names :
    if name [0] == "A":
        print("Name", name, " starts with A")