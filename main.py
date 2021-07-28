from argparse import ArgumentParser
import pandas as pd
import src.graph.diagrams as diagrams


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


def main():

    # adding all the arguments, reading the data
    arg = ArgumentParser()
    arg.add_argument("-g", "--gene", dest="gene", nargs="?", required=True)
    arg.add_argument("-t", "--transcript", dest="trans", nargs="?", required=True)
    arg.add_argument("-d", "--description", dest="desc", nargs="?", required=True)
    arg.add_argument("-o", "--occurrence", dest="occ", nargs="?", required=True)
    args = arg.parse_args()

    gene_csv = pd.read_csv(args.gene, sep=" ")
    trans_csv = pd.read_csv(args.trans, sep=" ")
    desc_csv = pd.read_csv(args.desc, sep="\t")
    occ_csv = pd.read_csv(args.occ, sep=" ")

    # renaming the isoform column to AGI to be able to merge the tables
    trans_csv.rename(columns={"isoform":"AGI"}, inplace=True)
    dfs = [gene_csv, trans_csv]
    allgenes = pd.concat(dfs)

    # adding a new column with the experiment for the subplots
    allgenes["exp_name"] = allgenes.EXP.apply(get_name)

    # making the plot for gene AT1G01020
    diagrams.plot(allgenes[allgenes.AGI.str.contains("AT1G01020")])


main()
