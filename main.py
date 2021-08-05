from argparse import ArgumentParser
import pandas as pd
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

gene_csv = pd.read_csv(args.gene, sep=" ")
trans_csv = pd.read_csv(args.trans, sep=" ")
desc_csv = pd.read_csv(args.desc, sep="\t", header=None, names=['gene', 'name', 'description'])
occ_csv = pd.read_csv(args.occ, sep="\t")

# getting a list of all genes by only using rows containing a single timestamp
genes = gene_csv[gene_csv.EXP.str.contains("7ko_LL18")].AGI

# both of the figures, will be unnecessary once app.callback is implemented
fig = processing.proc(gene_csv, trans_csv)

heatmap = processing.occ(occ_csv)

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
        dcc.Input(
            id='filter',
            placeholder='Filter the output'
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
                id='exp-graph',
                figure=fig)]
        ),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Toast(
                        [html.P(desc_csv[desc_csv.gene.str.contains("AT1G01060")].description)],
                        header=desc_csv[desc_csv.gene.str.contains("AT1G01060")].name
                    ), md=2
                ),
                dbc.Col(
                    dcc.Graph(
                        id="heatmap",
                        figure=heatmap
                    ), md=8
                )
            ]
        )
    ]
)

# main()
app.run_server(debug=True)
