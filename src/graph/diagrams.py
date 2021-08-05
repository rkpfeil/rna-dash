import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px


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
                      title=name)
    fig2.update_xaxes(matches=None)
    # fig1 = px.line(df, x="EXP", y="TPM", color="AGI", facet_col="exp_name")
    # fig = go.Figure(data=fig1.data + fig2.data)
    return fig2


# plotting the heatmap
# again not correct yet because of the use of strands and samples
def heatmap(csv, strands, samples):
    data = []
    for sample in samples:
        new = []
        for strand in strands:
            filtered = csv[csv["sample"].str.contains(sample)]
            filtered = filtered[filtered.strand.str.contains(strand)]
            if filtered[filtered.AGI.str.contains("AT1G01080")].empty:
                new.append(0)
            else:
                new.append(1)
        data.append(new)

    fig = px.imshow(data,
                    x=strands,
                    y=samples)
    return fig
