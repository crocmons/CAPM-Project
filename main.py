import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_datareader.data as web
import datetime
import capm_functions

st.set_page_config(page_title="CAPM", page_icon="chart_with_upwards_trend", layout="wide")

st.title("Capital Assets Pricing modal")

# getting input from users

col1, col2 = st.columns([1, 1])

with col1:
    stocks_list = st.multiselect("Choose 4 stocks", ("TSLA", "AAPL", "NFLX", "MSFT", "MGM", "AMZN", "GOOGL", "NVDA"), ["TSLA", "MSFT", "GOOGL", "AAPL"])

with col2:
    years = st.number_input("Number of Years", 1 , 10)


    # download data for Sp500
try:        
    start = datetime.date(datetime.date.today().year - years, datetime.date.today().month, datetime.date.today().day)

    end = datetime.date.today()    

    SP500 = web.DataReader(["sp500"], 'fred', start, end)

    # print(SP500.head())
    # print(SP500.tail())


    stocks_df = pd.DataFrame()

    for stock in stocks_list:
        data = yf.download(stock, period= f'{years}y')
        # print(data.head())
        stocks_df[f'{stock}'] = data['Close']
    # print(stocks_df.head(12))    
    stocks_df.reset_index(inplace=True)  
    SP500.reset_index(inplace = True) 
    print(stocks_df.dtypes)
    print(SP500.dtypes)

    SP500.columns = ["Date", "sp500"]

    stocks_df["Date"] = stocks_df["Date"].astype('datetime64[ns]')

    stocks_df["Date"] = stocks_df["Date"].apply(lambda x:str(x)[:10])

    stocks_df["Date"] = pd.to_datetime(stocks_df["Date"])

    stocks_df = pd.merge(stocks_df, SP500, on="Date", how="inner")

    col1, col2 = st.columns([1,1])

    with col1:
        st.markdown("### DataFrame Head Data")
        st.dataframe(stocks_df.head(), use_container_width=True)

    with col2:
        st.markdown("### DataFrame Tail Data")
        st.dataframe(stocks_df.tail(), use_container_width=True)



    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### Price of all the stocks above")
        st.plotly_chart(capm_functions.interactive_plot(stocks_df))

    with col2:
        # print(capm_functions.normalize(stocks_df))
        st.markdown("### After Normalization Price")
        # st.plotly_chart(capm_functions.normalize(stocks_df))
        st.dataframe(capm_functions.normalize(stocks_df), use_container_width=True)


    stocks_daily_return = capm_functions.daily_returns(stocks_df)

    print(stocks_daily_return.head())

    # alpha and beta value:
    beta = {}
    alpha = {}

    for i in stocks_daily_return.columns:
        if i != "Date" and i != "sp500":
            b, a = capm_functions.calculate_beta(stocks_daily_return, i)
            beta[i] = b
            alpha[i] = a

    print(beta, alpha)     

    beta_df = pd.DataFrame(columns=["Stock","Beta Value"])

    beta_df["Stock"] = beta.keys()
    beta_df["Beta Value"] = [str(round(i, 2)) for i in beta.values()]


    with col1:
        st.markdown("### Stocks Beta Value")
        st.dataframe(beta_df, use_container_width=True)

    # calculate the return

        rf = 0
        rm = stocks_daily_return['sp500'].mean() * 252

        return_values_df = pd.DataFrame()

        return_value = []

        for stock, values in beta.items():
            return_value.append(str(round(rf + (values * (rm - rf)), 2)))
        return_values_df["Stock"] = stocks_list

        return_values_df["Return Values"] = return_value  


    with col2:
        st.markdown("### Stocks Return CAPM")
        st.dataframe(return_values_df, use_container_width=True)

except:
    st.write("Please select valid input")






