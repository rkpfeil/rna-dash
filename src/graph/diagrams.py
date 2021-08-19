import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd


# first function try, kept for remembering subplots
def old(x, tpm, sd_tpm):
    fig = make_subplots(rows=1, cols=4, column_widths=[0.25, 0.25, 0.25, 0.25],
                        specs=[[{"type": "scatter"}, {"type": "scatter"}, {"type": "scatter"}, {"type": "scatter"}]])
    fig.add_trace(go.Scatter(
        name="AT1G01010",
        x=x,
        y=tpm,
        error_y=dict(
            type='data',
            array=sd_tpm)
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        name="AT1G01010",
        x=x,
        y=tpm,
        error_y=dict(
            type='data',
            array=sd_tpm)
    ), row=1, col=2)
    fig.add_trace(go.Scatter(
        name="AT1G01010.2",
        x=x,
        y=[1, 2, 3, 4],
        error_y=dict(
            type='data',
            array=sd_tpm)
    ), row=1, col=2)
    fig.add_trace(go.Scatter(
        x=x,
        y=tpm,
        error_y=dict(
            type='data',
            array=sd_tpm)
    ), row=1, col=3)
    fig.add_trace(go.Scatter(
        name="AT1G01010",
        x=x,
        y=tpm,
        error_y=dict(
            type='data',
            array=sd_tpm)
    ), row=1, col=4)
    fig.show()


# plotting a dataframe, making "subplots" according to experiment name
# commented out a try to add lines in the scatter plot, does not work when using subplots
def plot(df, name):
    fig2 = px.scatter(df, x="EXP", y="TPM", color="AGI", error_x="sd_TPM", error_y="sd_TPM", facet_col="exp_name",
                      title=name,
                      category_orders={"exp_name": ["wt", "7ko", "7ox", "8ox"]},
                      template="plotly_white")
    fig2.update_xaxes(matches=None)
    # fig1 = px.line(df, x="EXP", y="TPM", color="AGI", facet_col="exp_name")
    # fig = go.Figure(data=fig1.data + fig2.data)
    return fig2


# plotting the heatmap
# used if there is two values in sample
# keeping the variable names strands and samples
def heatmap(csv, samples, strands, gene):
    data = []
    for sample in samples:
        new = []
        for strand in strands:
            filtered = csv[csv["sample"].str.contains(sample)]
            filtered = filtered[filtered["sample"].str.contains(strand)]
            if filtered[filtered.AGI.str.contains(gene)].empty:
                new.append(0)
            else:
                new.append(1)
            print(new)
        data.append(new)

    fig = px.imshow(data,
                    x=strands,
                    y=samples,
                    color_continuous_scale=["red", "green"])
    return fig


# not in fact a heatmap because that only works if I have two things
def heatmap2(csv, samples, gene):
    data = []
    for sample in samples:
        filtered = csv[csv["sample"].str.contains(sample)]
        if filtered[filtered.AGI.str.contains(gene)].empty:
            data.append(0)
        else:
            data.append(1)
    dic = {"sample": samples, "data": data}
    df = pd.DataFrame(dic)
    fig = px.bar(df, x="sample", y=data)
    return fig
