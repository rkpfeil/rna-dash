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
# if a filter is selected, filtering the data
def proc(allgenes, name, percent):
    # making the plot for gene
    if percent == 0:
        fig = diagrams.plot(allgenes[allgenes.AGI.str.contains(name)], name)
    else:
        filtered = allgenes[allgenes.AGI.str.contains(name)]
        gene = filtered[filtered.AGI == name]
        gene = gene.set_index(pd.Index(range(16)))
        # print(gene)
        # print((filtered.TPM > 0).all())
        transcripts = filtered.AGI.tolist()
        transcripts = np.unique(transcripts)
        # print(percent * gene.TPM)
        keep = []
        for transcript in transcripts:
            df = filtered[filtered.AGI == transcript]
            df = df.set_index(pd.Index(range(16)))
            # print(df)
            # print(df.TPM.gt(percent*gene.TPM))
            if (df.TPM.gt(percent * gene.TPM)).any():
                keep.append(transcript)
                # print(transcript)
        filtered = filtered[filtered.AGI.isin(keep)]
        # print(filtered)
        fig = diagrams.plot(filtered, name)
    return fig


# processing the csv containing occurrences of genes in other datasets
# not entirely correct yet, strands and samples not always applicable
def occ(csv, val1, val2, gene):
    if len(val2) > 1:
        return diagrams.heatmap(csv, val1, val2, gene)
    else:
        return diagrams.heatmap2(csv, val1, gene)
