import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# plot functions for charts

def interactive_plot(df):
    fig = px.line(df, x="Date")
    for i in df.columns[1:]:
        fig.add_scatter(x=df["Date"], y=df[i], name=i)
    fig.update_layout(width=450, margin=dict(l=20, r=20, t=50, b=20), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    
    return fig   

def normalize(df_2):
    df = df_2.copy()
    for i in df.columns[1:]:
        df[i] = df[i] / df[i][0]
    return df   


def daily_returns(df_2):
    df_daily_return = df_2.copy()
    for i in df_daily_return.columns[1:]:
        for j in range(1, len(df_daily_return )):
            df_daily_return [i][j] = ((df_daily_return [i][j] - df_daily_return [i][j - 1]) / df_daily_return [i][j - 1]) * 100
        df_daily_return [i][0] = 0  
    return df_daily_return 

# calculate beta and alpha:
def calculate_beta(stocks_daily_return, stock):
    rm = stocks_daily_return['sp500'].mean() * 252
    b, a = np.polyfit(stocks_daily_return['sp500'], stocks_daily_return[stock], 1)

    return b, a

