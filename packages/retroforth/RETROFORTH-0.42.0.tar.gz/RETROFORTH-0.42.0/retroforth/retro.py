#!/usr/bin/env python3

import PyNGA_C

def run():
    Done = False
    while not Done:
        Line = input("\nOk> ")
        if Line == "bye":
            Done = True
        else:
            for Token in Line.split(" "):
                PyNGA_C.rre_evaluate(Token)

if __name__ == "__main__":
    run()
