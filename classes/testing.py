import document
from parser import *

if __name__ == "__main__":
    p = Parser()
    print("Welcome to DB123\n")
    while True:
        cmd = input('>>> ')
        if(cmd == 'q'):
            exit()
        p.parse(cmd)
