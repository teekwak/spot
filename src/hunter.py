# tokenize each python file
# need to keep track of methods that are found, but not declared
# need to keep track of methods that are declared, but not found
# keeping track of every method can get large, maybe we remove from global data structure if we find declaration + usage?
# let's stick to just finding methods being used
# let's also stick to a single file

# objective: get all methods in a file (declared and used)
# need a file for reserved words to ignore

from tokens.ClassToken import ClassToken
from tokens.MethodDeclarationToken import MethodDeclarationToken


class Hunter:

    def __init__(self):
        # i'm not even sure if we need this
        # self.reserved_words = frozenset([
        #     'and', 'as', 'assert',
        #     'break', 'class', 'continue',
        #     'def', 'del', 'elif',
        #     'else', 'except', 'False',
        #     'finally', 'for', 'from',
        #     'global', 'if', 'import',
        #     'in', 'is', 'lambda',
        #     'None', 'nonlocal', 'not',
        #     'or', 'pass', 'raise',
        #     'return', 'True', 'try',
        #     'while', 'with', 'yield',
        # ])
        self.class_names = {} # name to 'called' boolean
        self.method_names = {} # name to 'called' boolean

    def file_character_generator(self, file_path):
        with open(file_path, 'r') as file:
            while True:
                char = file.read(1)
                if len(char) == 1:
                    yield char
                else:
                    return

    # this is under the assumption that the code is correct
    def hunt(self, file_path):
        in_string = False
        current_token = ''

        character_reader = self.file_character_generator(file_path)
        for char in character_reader:
            # what if we hit a parentheses?
            # does that mean we are in a function?
            # what if we are in a generator?

            # parse strings
            # if char == '\'' or char == '\"':
            #     if in_string:
            #         if current_token[-1] == '\\':
            #             current_token += char
            #         else:
            #             in_string = False
            #             current_token += char
            #     else:
            #         in_string = True
            #         current_token += char

            # method invocation
            if char == '(':
                if current_token != '':
                    if '.' in current_token:
                        current_token = current_token.split('.')[-1]

                    if current_token in self.method_names:
                        # self.method_names[current_token] = True
                        self.method_names.pop(current_token, None)
                    else:
                        # we called a method not declared here
                        # do nothing for now
                        print(f"\"{current_token}\" was called, but not declared")

                # fastforward to ), skip arguments for now
                while char != ')':
                    char = next(character_reader)

            elif char.isspace():
                # TODO: ignore __xxx__ methods from being invoked
                # TODO: parse generators?
                # TODO: parse if statements
                # TODO: import statements

                if in_string:
                    current_token += char
                elif current_token == 'class':
                    # if the class name already exists, this could be okay
                    # if only there was a way to get the full class name

                    class_name = ClassToken.parse(character_reader)
                    self.class_names[class_name] = False
                elif current_token == 'def':
                    method_name = MethodDeclarationToken.parse(character_reader)
                    self.method_names[method_name] = False
                else:
                    # if len(current_token) > 0:
                    #     print(current_token)
                    pass

                current_token = ''
            else:
                current_token += char

        print(self.class_names)
        print(self.method_names)

if __name__ == '__main__':
    Hunter().hunt('../test/test.py')
