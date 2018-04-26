import argparse


class CommandLineArgParser:

    # TODO: check that file_path is a real file
    # TODO: check that file_path is a python file
    def __init__(self):
        parser = argparse.ArgumentParser(description='Recursively find unused classes and methods from a starting file.')
        parser.add_argument('file_path', type=str, help='relative file path to start scanning')
        args = parser.parse_args()
        self.file_path = args.file_path
