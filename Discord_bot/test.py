import random
import sys
import os

def get_dota_joke():
    with open("mars.txt", "r") as f:
        return(random.choice(f.readlines()))

if __name__ == "__main__":

    with open("mars.txt", "r") as f:
        print(random.choice(f.readlines()))

    exit()
    joke = get_dota_joke().strip()
    print(joke)
    



