# exception example
#import sys
from sys import exit
from time import sleep

try:
    print("a")
    #sleep(10)
    122/0
    exit(1)
    print("b")
except (SystemExit, KeyboardInterrupt):
    print("c")