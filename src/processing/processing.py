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
def proc(gene, trans):
    # renaming the isoform column to AGI to be able to merge the tables
    trans.rename(columns={"isoform": "AGI"}, inplace=True)
    dfs = [gene, trans]
    allgenes = pd.concat(dfs)
    allgenes = trans

    # adding a new column with the experiment for the subplots
    allgenes["exp_name"] = allgenes.EXP.apply(get_name)

    # making the plot for gene AT1G01020
    fig = diagrams.plot(allgenes[allgenes.AGI.str.contains("AT1G01060")], "AT1G01060")
    return fig


# processing the csv containing occurrences of genes in other datasets
# not entirely correct yet, strands and samples not always applicable
def occ(csv):
    strands = csv.strand.tolist()
    strands = np.unique(strands)
    samples = csv["sample"].tolist()
    samples = np.unique(samples)
    return diagrams.heatmap(csv, strands, samples)
