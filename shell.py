import src

while True:
    command = input("basic> ")

    if command == "exit":
        break

    res, error = src.run(command, "<stdin>")

    if error:
        print(error.as_string())
    if res:
        print(res)
