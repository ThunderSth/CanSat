def write_data(message):
    with open("/data.csv", "a") as file:
        file.write(message)
        file.write("\n")

while True:
    message = input("Messaage? ")
    write_data(message)