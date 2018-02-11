from os import listdir
from os.path import isfile, join
from simAnneal import simAnneal

dir = './test_benchmarks/'

filenames = [str(f) for f in listdir(dir) if isfile(join(dir, f))]


""" This function iterates through annealing schedules and prints results based on benchmark circuits
"""
for startT in [5,10,50,100,500,1000,5000]:
    for n in [5,10,50,100]:
        for deltaT in range(1,startT,startT/5):
            for exitprob in range(0.01,0.05,0.01):
                for runWith0 in [True,False]:

                    for filename in filenames:
                        f = open(dir+filename, "r")
                        myCircuit = simAnneal(startT, n, deltaT, exitprob, runWith0, f, None)

