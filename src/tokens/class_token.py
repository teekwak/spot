class ClassToken:

    @staticmethod
    def parse(reader):
        char = next(reader)

        while char.isspace():
            char = next(reader)

        name = ''
        while char != ':':
            name += char
            char = next(reader)

        return name.strip()
