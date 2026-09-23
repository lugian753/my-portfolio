from position import *


def view_pos():
    print("+"+"----+"+("----+"*6)+"----+")
    index=0
    while index!=64:
        print("|",end="")
        for i in range(8):
            print(" "+board[index]+"  ",end="|")
            index+=1
        print()
        print("+"+"----+"+("----+"*6)+"----+")

def main():
    insert_position(starting_pos)
    view_pos()

main()