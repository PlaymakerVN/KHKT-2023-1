
with open("code.txt", "r", encoding="utf-8") as file:
    code = file.read()

exec(code)