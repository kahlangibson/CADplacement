from Tkinter import *
import Tkinter as tk
from circuit import *
from os import listdir
from os.path import isfile, join
from draw import *

dir = './test_benchmarks/'

def read_infile():
    myapp.delete()
    filename = file.get()
    f = open(dir+filename, "r")
    myCircuit = Circuit(f,myapp)
    f.close()


## main ##
root = Tk()
root.lift()
root.attributes("-topmost", True)

myapp = draw(root)

global runButton
global halfPerimeterText
global v
# v = tk.StringVar()
# runButton = tk.Button(root, text="Run Placement", command=circuit.place)
# halfPerimeterText = tk.Label(root, textvariable=v)

file = tk.StringVar(root)
# initial value
file.set('Choose File')
# filenames = [f for f in listdir('./benchmarks/') if isfile(join('./benchmarks/', f))]
filenames = [f for f in listdir(dir) if isfile(join(dir, f))]
drop = tk.OptionMenu(root, file, *filenames)
drop.pack(side='left', padx=10, pady=10)
go = tk.Button(root, text="Choose File", command=read_infile)
go.pack(side='left', padx=20, pady=10)

root.mainloop()