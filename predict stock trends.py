import yfinance as yf #get imformation from yahoo finance
import pandas as pd #data frame proces

#get information about index
index = {
    "S&P500": "^GSPC",#ticker symbol
    "Nikkei 225": "^N225",
    "EEM (Emerging Markets)": "EEM",
    "Euro Stoxx 50": "^STOXX50E"
}

#setting start date and finish date
start_date = "2000-01-01"
finish_date = "2025-01-01"

#get data
df_list = []
for name, symbol in index.item():
    stock_data = yf.download(symbol, start = start_date, end = finish_date)
    stock_data["index"] = name
    df_list.append(stock_data)

#all data gathering to one data frame
df = pd.concat(df_list)

#save to CSV
df.to_CSV("Stock_data.csv")
print("The data can saved!!")

