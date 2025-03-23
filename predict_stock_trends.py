import yfinance as yf #get imformation from yahoo finance
import pandas as pd #data frame proces
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import streamlit as st
import os

#get information about index
Index = {
    "S&P500": "^GSPC",#ticker symbol
    "Nikkei 225": "^N225",
    "EEM (Emerging Markets)": "EEM",
    "Euro Stoxx 50": "^STOXX50E"
}

#setting start date and finish date
start_date = "2010-01-01"
finish_date = "2025-01-01"

#get data
df_list = []
for name, symbol in Index.items():
    stock_data = yf.download(symbol, start = start_date, end = finish_date, auto_adjust = True)
    stock_data =stock_data.reset_index()
    stock_data.columns = ['_'.join(col).strip().lower() if isinstance(col, tuple) else col.lower() for col in stock_data.columns]
    stock_data["index"] = name
    date_col = [col for col in stock_data.columns if col.startswith("date")]
    close_col = [col for col in stock_data.columns if col.startswith("close")]
    if date_col and close_col:
        stock_data["date"] = stock_data[date_col[0]]
        stock_data["close"] = stock_data[close_col[0]]
        df_list.append(stock_data[["date", "close", "index"]])
    else:
        print(f"{name} is not found...")
#all data gathering to one data frame
df = pd.concat(df_list, ignore_index = True)


#save to CSV
df.to_csv("Stock_data.csv", index = False)

#visualization
os.makedirs("output", exist_ok=True)
plt.figure(figsize = (15, 5))
for name in Index.keys():
    subset = df[df["index"] == name]
    plt.plot(subset["date"], subset["close"], label = name)#make line graph
    plt.xlabel("Year")
    plt.ylabel("Adjusted close price")
    plt.title("Stock market index performance (2000 - 2025)")
    plt.legend()#display label
    plt.grid()#add background line
    plt.show()
    filename = name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("/", "") + ".png"
    plt.savefig(f"output/{filename}")
    plt.close()





#result list
results = []

#get data
for name, symbol in Index.items():
    df = yf.download(symbol, start = start_date, end = finish_date, auto_adjust = True)
    df = df.reset_index()
    df.columns = ["_".join(col).strip().lower() if isinstance(col, tuple) else col.lower() for col in df.columns]


    date_col = [col for col in df.columns if "date" in col][0]
    close_col = [col for col in df.columns if "close" in col][0]

    df = df[[date_col, close_col]]
    df = df.rename(columns={date_col: "date", close_col: "close"})

    #tomorrow label
    df["close_tomorrow"] = df["close"].shift(-1)
    #delet last column
    df = df[:-1]

    X = df[["close"]].values#today's stock value
    Y = df["close_tomorrow"].values#tomorrow's stock value

    #create model and learning
    model = LinearRegression()
    model.fit(X,Y)
 
    #predict stock
    last_close = df["close"].values[-1]
    predicted = model.predict([[last_close]])[0]

    results.append((name, last_close, predicted))

print("Tomorrow's stock prediction:")
for name, last_close, predicted in results:
    print(f"{name}\n current close stock price: {last_close:.2f}\n Tomorrow's stock price: {predicted:.2f}\n")

df_result = pd.DataFrame(results, columns = ["Index", "Current_Close", "Predicted_Tomorrow"])
df_result.to_csv("predicted_results.csv", index = False)
print("Save to CVS!!")

#streamlit app
st.set_page_config(page_title = "Tomorrow's stock prediction", layout = "centered")
st.title("Dashboard")
df = pd.read_csv("predicted_results.csv")

#display
st.subheader("Each Index result")
st.dataframe(df)
st.subheader("Predicted vs Current")
selected = st.selectbox("Please select index", df["Index"])
if selected:
    selected_data = df[df["Index"] == selected][["Current_Close", "Predicted_Tomorrow"]].T
    selected_data.columns = [selected]
    st.bar_chart(selected_data)

