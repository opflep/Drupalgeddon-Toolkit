import os
import sys
from sys import argv
import ntpath

file_path = sys.argv[1]
number = sys.argv[2]


def split_file(filepath, lines_per_file):
    lpf = lines_per_file
    path, filename = os.path.split(filepath)
    n = 1
    with open(filepath, 'r') as r:
        name, ext = os.path.splitext(filename)
        try:
            w = open(os.path.join(path, '{}_{}{}'.format(name, 0, ext)), 'w')
            for i, line in enumerate(r):
                if not i % lpf:
                    w.close()
                    filename = "input_"+str(n)+".txt"
                    w = open(filename, 'w')
                    n += 1
                w.write(line)
        finally:
            w.close()


if __name__ == "__main__":
    split_file(file_path, int(number))
