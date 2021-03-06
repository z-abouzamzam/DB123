import document
import readline
from parser import *

if __name__ == "__main__":
    # Initialize a parser for handling user input
    p = Parser()
    print("Welcome to DB123\n")

    # Run the database until 'q' or 'quit' is issued as a command
    while True:
        cmd = input('>>> ')
        if(cmd.lower() == 'q' or cmd.lower() == 'quit'):
            exit()
        elif(cmd == '\n'):
            continue
        p.parse(cmd)
