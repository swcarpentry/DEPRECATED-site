import sys

def key(x):
    return x.split(' ')[1].split('/')[-1]

with open(sys.argv[1], 'r') as reader:
    lines = [x.strip() for x in reader.readlines()]

lines = [(key(x), x) for x in lines]
lines.sort()

with open(sys.argv[1], 'w') as writer:
    for (key, line) in lines:
        print >> writer, line
