import sys
import csv
import numpy as np
from matplotlib import pyplot as plt

countries = []
populations = []
attendees = []
instructors = []
with open(sys.argv[1], 'r') as raw:
    cooked = csv.reader(raw)
    for (c, p, a, i) in cooked:
        countries.append(c)
        populations.append(float(p))
        attendees.append(float(a))
        instructors.append(float(i))

populations = np.array(populations) / 1e6
attendees = np.array(attendees) / populations
instructors = np.array(instructors) / populations

plt.scatter(attendees, instructors)
plt.xlabel('Attendees per million pop')
plt.ylabel('Instructors per million pop')

for (label, x, y) in zip(countries, attendees, instructors):
    plt.annotate(label, xy = (x, y))

plt.show()
