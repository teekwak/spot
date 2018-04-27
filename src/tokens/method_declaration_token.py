class MethodDeclarationToken:

    @staticmethod
    def parse(reader):
        char = next(reader)

        # move generator up until not a whitespace
        while char.isspace():
            char = next(reader)

        name = ''
        # get name of method
        while char != '(':
            name += char
            char = next(reader)

        return name.strip()

        # # get arguments
        # while char != ')':
        #     current_token += char
        #     char = next(reader)
        # current_token += char

        # # remove rest of whitespace
        # while char != ':':
        #     char = next(reader)
