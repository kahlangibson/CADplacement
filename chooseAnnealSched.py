from os import listdir
from os.path import isfile, join
from simAnneal import simAnneal
import numpy

dir = './benchmarks/'

filenames = [str(f) for f in listdir(dir) if isfile(join(dir, f))]
# filenames = ['apex1.txt']

# annealSched = {"startT":0, "n":0, "beta":0, "exitRate":0, "runWith0":0}
# sizeDict = {"x":0,"y":0}
costs = {}
bestAcceptRates = {}
scheds = {}
sizes = {}
numCells = {}
all_schedules = {}
acceptRates = {}

for f in filenames:
    sizes[f] = {}
    scheds[f] = {}
    bestAcceptRates[f] = {}
    all_schedules[f] = {}
    acceptRates[f] = {}

list1 = [80.]
list3 = [0.25]

""" This function iterates through annealing schedules 
    and prints results based on benchmark circuits
"""

for startT in list1:
    for beta in [0.6]:
        for exitRate in list3:
            for runWith0 in [True]:
                for i,filename in enumerate(filenames):
                    print filename + " " + str(i+1) + "/" + str(len(filenames)) + ": startT " \
                          + str(startT) + " beta " + str(beta) + " exitRate " + str(exitRate)
                    f = open(dir+filename, "r")  # gets closed inside simAnneal object
                    myCircuit = simAnneal(startT, beta, exitRate, runWith0, f)
                    if filename not in costs: # only need to collect these once/initialize
                        costs[filename] = myCircuit.cost
                        sizes[filename] = {"x": myCircuit.nx, "y": myCircuit.ny}
                        numCells[filename] = myCircuit.numCells
                    myCircuit.runSimAnneal()
                    if myCircuit.cost <= costs[filename]:
                        costs[filename] = myCircuit.cost
                        del scheds[filename]
                        del bestAcceptRates[filename]
                        scheds[filename] = \
                            {"startT": startT, "beta": beta,
                             "exitRate": exitRate, "runWith0": runWith0}
                        bestAcceptRates[filename] = myCircuit.acceptanceRates
                    all_schedules[filename][myCircuit.cost] = \
                        {"startT": startT, "beta": beta,
                         "exitRate": exitRate, "runWith0": runWith0}
                    acceptRates[filename][myCircuit.cost] = myCircuit.acceptanceRates


output = open("results.txt", "w")

for f in filenames:
    ratef = open("rate_"+f, "w")
    for rate in bestAcceptRates[f]:
        ratef.write(str(rate[1])+"\n")
    ratef.close()
    output.write(f + "\n")
    output.write("Size: " + str(sizes[f]["x"]) + ", " + str(sizes[f]["y"]) + "\n")
    output.write("Num Cells: " + str(numCells[f]) + "\n")
    output.write("Minimum Cost: " + str(costs[f]) + "\n")
    for param in scheds[f]:
        output.write("   " + param + " : " + str(scheds[f][param]) + "\n")

output.close()

for f in filenames:
    output = open("top5_"+f, "w")
    output.write(f + "\n")
    costs = [s for s in all_schedules[f]]
    print costs
    for _ in range(min(len(costs),5)):
        c = costs[0]
        i = 0
        for idx, cost in enumerate(costs):
            if cost < c:
                c = cost
                i = idx
        output.write("Cost: " + str(c) + "\n")
        for param in all_schedules[f][c]:
            output.write("   " + param + " : " + str(all_schedules[f][c][param]) + "\n")
        for tuple in acceptRates[f][c]:
            output.write("   " + str(tuple[0]) + " : " + str(tuple[1]) + "\n")
        output.write("\n")
        costs.pop(i)

    output.close()

print "done"


