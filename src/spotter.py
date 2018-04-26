# tokenize each python file
# need to keep track of methods that are found, but not declared
# need to keep track of methods that are declared, but not found
# keeping track of every method can get large, maybe we remove from global data structure if we find declaration + usage?
# let's stick to just finding methods being used
# let's also stick to a single file

# objective: get all methods in a file (declared and used)
# need a file for reserved words to ignore

# TODO: maybe topological sort functions (dependency graph)
# even if a method calls another method in a class,
# if that method is not called, then those other functions are
# not called
# or running hunter multiple times will catch all of them

from command_line_arg_parser import CommandLineArgParser
from tokens.class_token import ClassToken
from tokens.method_declaration_token import MethodDeclarationToken


class Spotter:

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
        self.undeclared_method_names = []

    def file_character_generator(self, file_path):
        with open(file_path, 'r') as file:
            while True:
                char = file.read(1)
                if len(char) == 1:
                    yield char
                else:
                    return

    # this is under the assumption that the code is correct
    def spot(self, file_path):
        in_string = False
        current_token = ''

        character_reader = self.file_character_generator(file_path)
        for char in character_reader:
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

            # constructor/method invokation
            if char == '(':
                # if current_token == '', then we were at a tuple/generator
                if current_token != '':
                    if '.' in current_token:
                        current_token = current_token.split('.')[-1]

                    if current_token in self.method_names:
                        self.method_names[current_token] = True
                    elif current_token in self.class_names:
                        self.class_names[current_token] = True
                    else:
                        # we called a method not declared here
                        # do nothing for now
                        self.undeclared_method_names.append(current_token)

                # fastforward to ), skip arguments for now
                while char != ')':
                    char = next(character_reader)
            # ignore commented lines
            # TODO: what if there is a # in a string?
            # TODO: add support for ''' and """
            # elif char == '#':
            #     current_token = ''
            #     while char != '\n':
            #         char = next(character_reader)
            elif char.isspace():
                if in_string:
                    current_token += char
                elif current_token == 'class':
                    # if only there was a way to get the full class name
                    # to differentiate between different modules
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

        print(f'Uncalled Classes: {[name for name in self.class_names.keys() if not self.class_names[name]]}')
        print(f'Uncalled Methods: {[name for name in self.method_names.keys() if not self.method_names[name]]}')
        print(f'Undeclared Methods: {self.undeclared_method_names}')

if __name__ == '__main__':
    argParser = CommandLineArgParser()
    Spotter().spot(argParser.file_path)
