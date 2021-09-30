#!/usr/bin/python
# coding: utf-8
# Author: LE YUAN
# Date: 2021-09-30

# This python script is to compare the conservation score of essential and non-essential gene comparison across five yeast species
# Input : (i) Essential gene data (ii) Conservation score data
# Output : (i) processed file (ii) A boxplot


import json
import csv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# This function is to process the conservation score data
def process_data() :
    with open("./test_data/conservation_score.txt", "r") as infile :
        conservation_data = infile.readlines()

        conservation = dict()
        for line in conservation_data :
            ortholog = line.strip().split(" ")[2][1:-1]
            conservation_score = line.strip().split(" ")[3]
            conservation[ortholog] = float(conservation_score)

        # This organisms list is five yeast species that I am working
        organisms = ["S_cerevisiae", "S_pombe",  "C_albicans", "Y_lipolytica", "P_pastoris"]
        essential_status = {'E':'Essential', 'NE':'Non-essential'}

        # Open a output csv file and write the content using the csv package
        outfile = open("./output/conservation_score.csv", "w")
        csv_writer = csv.writer(outfile)
        csv_writer.writerow(["type", "organism", "conservation_score"])

        # Process the json file using the json package
        i = 0
        for organism in organisms :
            print("This yeast species is: %s" % organism.replace("_", ". "))
            with open("./test_data/%s.json" % organism, "r") as f :
                data = json.load(f)

            for essential in data :
                ortholog = essential['ortholog']
                try : 
                    csv_writer.writerow([essential_status[list(essential.values())[0]], organism.split('_')[0][0]+'. '+organism.split('_')[1], conservation[ortholog]])
                except :
                    i +=1
                    # print(i)
        outfile.close()

        print("\n" + "-------"*5)
        print("Great! I have generated the processed data file!")

# This function is to output a boxplot to viualize the result
def main() :
    # Read the processed data using the pandas package
    alldata = pd.read_csv("./output/conservation_score.csv")

    plt.figure(figsize=(3.,2.4))
    palette = {"Essential": '#ed7e17', "Non-essential": '#1ba055'}
    # Using the seaborn package to generate a boxplot
    for ind in alldata.index:
        alldata.loc[ind,'organism'] = '${0}$'.format(alldata.loc[ind,'organism'])
    ax = sns.boxplot(data=alldata, x="organism", y="conservation_score", hue="type",
            palette=palette, showfliers=False, linewidth=1)
    ax.set(xlabel=None)

    # Set the ticks and labels for x and y
    plt.xticks(rotation=30,ha='right')
    plt.xticks(fontname = "Arial") 
    plt.yticks([0,0.2,0.4,0.6,0.8,1.0,1.2,1.4])
    plt.ylabel("Conservation score", fontname='Arial')

    handles,labels = ax.get_legend_handles_labels()
    # # specify one legend
    l = plt.legend(handles[0:2], labels[0:2], loc=2, frameon=False, prop={'family':'Arial'})
    plt.savefig("./output/boxplot_result.pdf", dpi=400, bbox_inches = 'tight')

    print("\n" + "-------"*5)
    print("Great! I have generated the boxplot for visualization!")


# Run two functions above
if __name__ == "__main__" :
    process_data()
    main()
