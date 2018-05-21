import document
from parser import *

if __name__ == "__main__":
    p = Parser()
    print("Welcome to DB123\n")
    while True:
        cmd = input('>>> ')
        if(cmd.lower() == 'q' or cmd.lower() == 'quit'):
            exit()
        elif(cmd == '\n'):
            continue
        p.parse(cmd)
