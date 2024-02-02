# simple TSV data extraction script
# author: Jackson Datkuliak

# Sample tsv import from Carta
#               0           1           2
# 0  NumPixels     100.000000    pixel(s)
# 1  Sum            10.794709      MJy/SR
# 2  FluxDensity          NaN         NaN
# 3  Mean            0.107947      MJy/SR
# 4  StdDev          0.108665      MJy/SR
# 5  Min            -0.072920      MJy/SR
# 6  Max             0.383152      MJy/SR
# 7  Extrema         0.383152      MJy/SR
# 8  RMS             0.152783      MJy/SR
# 9  SumSq           2.334250  (MJy/SR)^2

import pandas as pd
import os

# File directory to scan for folders containing tsv files
directoryToScan = 'ngc1792' # <-- change me to name of folder to scan for folders containing tsv files
rowOp = 3 # <-- change this to the corresponding row of numbers you want to evaluate. 3 is mean, 4 is StdDev, etc.



statString = "" # don't change this!
for dir in os.scandir(directoryToScan):
    # make sure that this is a directory and not a file
    if (dir.is_dir()):
        # Initializing variables
        tsvArray = []
        means = []
        pixels = []
        finalMean = 0
        totalPixels = 0

        # Scanning the directory
        files = os.scandir(dir.path)
        # looking through every file in the directory
        for entry in files:
            # if the entry is a file and has a .tsv extension
            if(entry.name[len(entry.name)-4:len(entry.name):1] == ".tsv"):
                # read every tsv file with pandas library, then add it to an array
                # sep argument is the data separator argument, \t is the TAB key character (default for CARTA exports)
                # comment argument tells pandas what lines to ignore (what lines are comments)
                # header argument tells it to not read the first line as a header
                currentCsv = pd.read_csv(dir.path + '/' + entry.name, sep='\t', comment="#", header = None)
                # extract the mean value, StdDev, etc
                means.append(currentCsv.iloc[rowOp, 1])
                pixels.append(currentCsv.iloc[0, 1])

        # we have mean values and the amount of pixels they represent, so we will take a weighted average of the dataset
        for i in range(len(pixels)):
            # adding all of the pixel values to get the total
            totalPixels += pixels[i]
        
        for i in range(len(means)):
            # taking the ratio of how many pixels where in the region to the total amount of pixels and adding that regions mean value
            finalMean += (pixels[i] / totalPixels) * (means[i])

        # Append data to a a string to save later
        statString += ("Means " + dir.name +":  " + str(finalMean) + "\n")

        # Print data to terminal
        print(dir.name + "   " + str(finalMean))

# Open a text file in the directory that was scanned and output data
textFile = open(directoryToScan + "/stats.txt", "w")
textFile.write(statString)
textFile.close()