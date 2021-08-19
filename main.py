from argparse import ArgumentParser
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import src.processing.processing as processing

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# def main():
# adding all the arguments, reading the data
arg = ArgumentParser()
arg.add_argument("-g", "--gene", dest="gene", nargs="?", required=True)
arg.add_argument("-t", "--transcript", dest="trans", nargs="?", required=True)
arg.add_argument("-d", "--description", dest="desc", nargs="?", required=True)
arg.add_argument("-o", "--occurrence", dest="occ", nargs="?", required=True)
args = arg.parse_args()

gene_csv = pd.read_csv(args.gene, sep="\t")
trans_csv = pd.read_csv(args.trans, sep="\t")
desc_csv = pd.read_csv(args.desc, sep="\t", header=None, names=['gene', 'name', 'description'])
occ_csv = pd.read_csv(args.occ, sep="\t")

# getting a list of all genes by only using rows containing a single timestamp
genes = gene_csv[gene_csv["EXP"].str.contains("7ko_LL18")].AGI

# renaming the isoform column to AGI to be able to merge the tables
trans_csv.rename(columns={"isoform": "AGI"}, inplace=True)

# adding a new column with the experiment for the subplots
trans_csv["exp_name"] = trans_csv["EXP"].apply(processing.get_name)


# extracting data about other experiments
# if there is two conditions splitting the sample part
occ_csv.sample = occ_csv["sample"].str.split(" ", 1)
val1 = []
val2 = []
if len(occ_csv.sample[0]) > 1:
    occ_csv["val1"] = occ_csv.sample.apply(lambda x: x[0])
    occ_csv["val2"] = occ_csv.sample.apply(lambda x: x[1])
    val1 = occ_csv.val1.tolist()
    val1 = np.unique(val1)
    val2 = occ_csv.val2.tolist()
    val2 = np.unique(val2)
else:
    occ_csv["val1"] = occ_csv.sample.apply(lambda x: x[0])
    val1 = occ_csv.val1.tolist()
    val1 = np.unique(val1)

print(len(val2))

# two parts of the dash, cleaning up the layout
dropdown = dbc.Card(
    [
        dcc.Dropdown(
                    id='gene',
                    options=[{"label": gene, "value": gene} for gene in genes.tolist()
                             ],
                    value="AT1G01060"
        )
    ]
)

fil = dbc.Card(
    [
        dcc.Dropdown(
            id='percent',
            options=[{"label": "10%", "value": 0.1}, {"label": "20%", "value": 0.2}, {"label": "5%", "value": 0.05},
                     {"label": "all", "value": 0}],
            value=0
        )
    ]
)

# app layout deciding how the dashboard looks
app.layout = dbc.Container(
    [
        html.H1(children='RNA-seq transcript expression Dashboard'),

        html.Div(children='''
            Expression profiles of Col2 (WT), grp7-1 8i, AtGRP7-ox and AtGRP8-ox RNA-seq samples
        '''),

        dropdown,

        fil,

        #dbc.Row(
        #    [
        #        dbc.Col(dropdown, md=8),
        #        dbc.Col(fil, md=4)
        #    ]
        #),

        dbc.Row(
            [dcc.Graph(
                id='exp-graph')]
        ),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Toast(
                        [html.P(id='desc')],
                        id='name'
                    ), md=2
                ),
                dbc.Col(
                    dcc.Graph(
                        id="heatmap"
                    ), md=8
                )
            ]
        )
    ]
)

# updating every part according to the dropdowns
@app.callback(
    Output('exp-graph', 'figure'),
    Input('gene', 'value'),
    Input('percent', 'value'))
def exp_graph(gene, percent):
    return processing.proc(trans_csv, gene, percent)


@app.callback(
    Output('name', 'header'),
    Output('desc', 'children'),
    Input('gene', 'value'))
def description(gene):
    name = desc_csv[desc_csv.gene.str.contains(gene)].name
    desc = desc_csv[desc_csv.gene.str.contains(gene)].description
    return name, desc


@app.callback(
    Output('heatmap', 'figure'),
    Input('gene', 'value'))
def heatmap(gene):
    return processing.occ(occ_csv, val1, val2, gene)


# main()
app.run_server(debug=False, host="0.0.0.0")
