import sys
import toolbox
import os

def run(project):
    directory = toolbox.prefix_dataset + project + "/"
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            with open(directory + file, "r") as content:
                if not content.read():
                    print file

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print "usage python checker.py <project> "
    else:
        run(sys.argv[1])
