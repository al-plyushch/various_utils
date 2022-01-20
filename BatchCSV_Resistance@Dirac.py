import numpy as np
import os
import tkinter
from tkinter import filedialog
import matplotlib.pyplot as plt


tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing
path = filedialog.askdirectory()
print(path)

filelist = os.listdir(path)
print(filelist)
for count, file in enumerate(filelist):
    if ".txt" in file:
        filelist.pop(count)
print(filelist)


#for count, value in enumerate(values):
#...     print(count, value)
Resistances = {}


for file in filelist:
# This specifically written to handle data files from probe station
    V, I, Vg, = [],[],[]
    try:
        Sample = file.split("_")[0]+ file.split("_")[1]
        Device = file.split("_")[3]
        print(Sample, Device)
    except:
        print("Incorrect File format " + file + " Checking next file...")
        continue

    with open(path + "/{}".format(file), "r") as reader:

####Get the current and voltage amplification factor from file header
        line = reader.readline()
        header = line.split()
        print(header)
        f_I = 10**int(header[7].split("^")[1].split(")")[0])
        f_V = int(header[5].replace("(", "").replace(")", "").replace("x", ""))
        print("voltage factor", f_V)
        print("current factor", f_I)
        line = reader.readline()
#Get voltage and current values


        while line != '':

            try:

                V.append(float(line.split()[3].replace(",", ".")))
                Vg.append(float(line.split()[2].replace(",", ".")))
                I.append(float(line.split()[4].replace(",", ".")))
                line = reader.readline()
            except:
                print(file + "Invalid file format")



        V = np.asarray(V, dtype=float)/f_V
        I = np.asarray(I, dtype=float)/f_I




    reader.close()
    R = V/I
    maxR = np.max(R)
    Resistances[file] = maxR
    print(maxR)

results = open(path+"/Results of {}.dat".format(Sample +" "+ Device), "w")

for device in Resistances:
    results.write(device + " " + str(Resistances[device])  +"\n")

results.close()

print ("Done!")





