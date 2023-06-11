with open("test.html", 'rb') as f:
    page = f.read()
page = page.decode("utf-8")

# Replace the first occurrence of "12345abc" with a new string
new_string = page.replace("12345abc", "aaaaaaaaaaaaaaaaaa")

# Use the updated new_string for the subsequent replacement
new_string = new_string.replace("Hello", "Hi")

new_string = new_string.encode("utf-8")
print(new_string)
