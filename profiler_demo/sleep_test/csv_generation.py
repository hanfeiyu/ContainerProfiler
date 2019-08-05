import random
import json
import os, sys
import pandas as pd
import subprocess
import matplotlib.pyplot as plt
import numpy as np

# vm_container dictionary to store the virtual machine and container data. Key is the filename and value is the virtual machine and container data.
vm_container = {}
# Path from where the json files to be converted to a csv file
path = sys.argv[1]
dirs = os.listdir( path )
# processes dictionary to store process level data
processes = dict()

for file in dirs:
    with open(path+file) as f:
        # Deserialize into python object
        y = json.load(f)
        # A dictionary which contains the value of vm_container dictionary
        r = {}

        # Check for any list or dictionary in y
        for k in y:
            if k != "pProcesses" and k != "cProcessorStats":
                r[k] = y[k]

        if "cProcessorStats" in y and "cNumProcessors" in y:
            for k in y["cProcessorStats"]:
                if k != "cNumProcessors":
                    r[k] = y["cProcessorStats"][k]

        #totalProcesses = y["cNumProcesses"]
        totalProcesses = len(y["pProcesses"]) - 1

        # Loop through the process level data
        for i in xrange(totalProcesses):
            # A dictinary containing process level data
            s = {"filename": file}

            for k in y["pProcesses"][i]:
                s[k] = y["pProcesses"][i][k]

            # If the process id is already in the processes, append to the list of processes
            pids = []
            if y["pProcesses"][i]["pId"] in processes:
                pids = processes[y["pProcesses"][i]["pId"]]
            pids.append( s )
            processes[y["pProcesses"][i]["pId"]] = pids
        vm_container[file] = r

# Create a separate CSV files for each of the processes
for key, value in processes.iteritems():
    df1 = pd.DataFrame(value)
    df1.to_csv(str(key)+".csv")

# Dump dictionary to a JSON file
with open("vm_container.json","w") as f:
    f.write(json.dumps(vm_container))

# Convert JSON to dataframe and convert it to CSV
df = pd.read_json("vm_container.json").T
df.to_csv("vm_container.csv", sep=',')
