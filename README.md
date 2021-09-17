# rna-dash

### usage

Parameters:

-t: TPM Data, tab separated, containing isoform, EXP, TPM, sd_TPM\
isoform: gene AGI or name of the isoform\
EXP: Experiment name and timestamp, seperated by an underscore. Needs to contain wildtype (wt_)\
TPM: TPM data\
sd_TPM: standard derivation of the TPM data

![Picture of a table containing example data](/pictures/transcript1.png)

-d: gene annotation data, tab separated, containing AGI, gene name and gene description, columns don't have names

-o: occurrence of genes in other experiments, tab separated, containing AGI and sample\
sample can contain either one or two conditions, separated by a space

![Picture of a table containing example data](/pictures/datasets.png)

-p: port, default is 8050

-b: run as debug True or False, default is False

-i: title, default is empty. If the title contains more than one word, it has to be enclosed by ""

### features

#### dashboard

The dashboard contains a graph showing the expression of a gene. This gene is chosen via a dropdown menu containing all available genes with their name and descriptions. This is cut off after 70 characters. If a gene has a name an/or description but there is no expression data, a blank graph is shown. The shown expression data can be filtered with a second dropdown menu. With this dropdown menu a percentage is selected. Transcripts with an expression under said percentage of the gene expression will be excluded from the graph.

![Picture of the upper part of the dashboard, containing title, filter options and the graph](/pictures/dashboard_top.png)

Under the graph are a card containing the chosen genes name and description and information aout other datasets where the gene was found. Depending on if the datasets contain one or two conditions this will be shown as a heatmap for two conditions or a histogram for a single condition

![Picture of the lower part of the dashboard containing information about the selected gene and a heatmap showing in what other datasets the gene was expressed](/pictures/dashboard_bottom.png)

#### filters

![Picture of the dropdown menu for choosing a gene](/pictures/gene_selection.png)

As mentioned in the section above, a filter has been implemented to choose a percentage. Transcripts that are expressed with a rate lower than that percentage of the gene expression are not shown. Below are images of the graph for example gene 2. In the first image, all transcripts are shown, in the second picture they are filtered with 10%.

![Picture of the graph for example gene 2 unfiltered](/pictures/unfiltered.png)
![Picture of the graph for example gene 2 filtered with 10%, two of the transcripts are no longer shown](/pictures/filtered_10.png)
