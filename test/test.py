class Something:

    def __init__(self):
        pass

    def do_something(self):
        print("class asdf")

    def do_something_else(self):
        self.do_something()


if __name__ == '__main__':
    x = (1, 2)
    y = Something()
