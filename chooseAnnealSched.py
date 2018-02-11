from os import listdir
from os.path import isfile, join
from simAnneal import simAnneal
import numpy
from time import gmtime, strftime

dir = './benchmarks/'

filenames = [str(f) for f in listdir(dir) if isfile(join(dir, f))]
# filenames = ["alu2.txt"]

# annealSched = {"startT":0, "n":0, "deltaT":0, "exitT":0, "runWith0":0}
# sizeDict = {"x":0,"y":0}
costs = {}
scheds = {}
sizes = {}
all_schedules = {}
for f in filenames:
    costs[f] = 0
    sizes[f] = {}
    scheds[f] = {}
    all_schedules[f] = {}

list1 = [10., 100., 1000.]
list2 = [10,50]

""" This function iterates through annealing schedules and prints results based on benchmark circuits
"""

for startT in list1:
    for n in list2:
        for deltaT in numpy.arange(1., startT/4., 2.):
            for exitT in numpy.arange(1., 10., 1.):
                for runWith0 in [True,False]:
                    for i,filename in enumerate(filenames):
                        print filename + " " + str(i+1) + "/" + str(len(filenames)) + ": startT " + str(startT) + " deltaT " + str(deltaT) + " exitT " + str(exitT)
                        f = open(dir+filename, "r")
                        myCircuit = simAnneal(startT, n, deltaT, exitT, runWith0, f, None)
                        f.close()
                        if sizes[filename] == {}:
                            sizes[filename] = {"x":myCircuit.nx,"y":myCircuit.ny}
                            costs[filename] = myCircuit.cost
                        myCircuit.runSimAnneal()
                        if myCircuit.cost <= costs[filename]:
                            costs[filename] = myCircuit.cost
                            del scheds[filename]
                            scheds[filename] = \
                                {"startT":startT, "n":n, "deltaT":deltaT,
                                 "exitT":exitT, "runWith0":runWith0}
                        all_schedules[filename][myCircuit.cost] = \
                            {"startT":startT, "n":n, "deltaT":deltaT,
                                 "exitT":exitT, "runWith0":runWith0}


output = open("results.txt", "w")
for f in filenames:
    output.write(f + "\n")
    output.write("Minimum Cost: " + str(costs[f]) + "\n")
    for param in scheds[f]:
        output.write("   " + param + " : " + str(scheds[f][param]) + "\n")

output.close()

output = open("top5.txt", "w")
for f in filenames:
    output.write(f + "\n")
    costs = [s for s in all_schedules[f]]
    print costs
    for _ in range(5):
        c = costs[0]
        i = 0
        for idx,cost in enumerate(costs):
            if cost < c:
                c = cost
                i = idx
        output.write("Cost: " + str(c) + "\n")
        for param in all_schedules[f][c]:
            output.write("   " + param + " : " + str(all_schedules[f][c][param]) + "\n")
        costs.pop(i)

output.close()

print "done"


