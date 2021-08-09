import pandas as pd
import src.graph.diagrams as diagrams
import numpy as np


# function to get the experiment name out of the data
def get_name(exp):
    if "7ko" in exp:
        return "7ko"
    elif "7ox" in exp:
        return "7ox"
    elif "8ox" in exp:
        return "8ox"
    else:
        return "wt"


# processing csvs containing tpms, merging of the tables unnecessary for now
# as the one for the transcripts contains all necessary information
def proc(allgenes, name, percent):
    # making the plot for gene
    fig = diagrams.plot(allgenes[allgenes.AGI.str.contains(name)], name)
    return fig


# processing the csv containing occurrences of genes in other datasets
# not entirely correct yet, strands and samples not always applicable
def occ(csv, gene):
    strands = csv.strand.tolist()
    strands = np.unique(strands)
    samples = csv["sample"].tolist()
    samples = np.unique(samples)
    return diagrams.heatmap(csv, strands, samples, gene)
