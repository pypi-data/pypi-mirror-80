def verb(func):
    def wrapper():
        print("verb wrap")
        func()
        print("end verb wrap")