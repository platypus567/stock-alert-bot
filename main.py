import os
import requests

from twilio.rest import Client
ACCOUNT_SID = "" #insert your twilio creds, mine are hidden for security
auth_token = "" 

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

#I don't really care about these keys so you can use them
stock_api_key = "7F71K4LRT680RI1E"
news_api_key = "427edcef72344f91a62dcadad30b1d91"




stock_params = {
    "function":"TIME_SERIES_DAILY",
    "symbol":"TSLA", #change TSLA for any ticker and itll work
    "apikey": stock_api_key,
    "outputsize": "compact"
}

response = requests.get("https://www.alphavantage.co/query",params=stock_params)
response.raise_for_status()
stock_data = response.json()
print(stock_data)


last_refresh = stock_data["Meta Data"]["3. Last Refreshed"]
days_data = stock_data["Time Series (Daily)"][last_refresh]
formula = ((float(days_data["4. close"]) - float(days_data["1. open"]))/float(days_data["1. open"]))*100
formula = round(formula,2)
print(formula)
ticker = stock_params["symbol"]
if formula >= 5:
    news_params = {
        "apiKey": news_api_key,
        "q": stock_params["symbol"],
        "from": last_refresh
    }
    news_response = requests.get("https://newsapi.org/v2/everything",params=news_params)
    news_response.raise_for_status()
    news_data = news_response.json()
    news_slice = news_data["articles"][:3]
    print(news_slice)
    #list of title and news that was called
    news_list = [
        [news_slice[0]["title"], news_slice[0]["description"]],
        [news_slice[1]["title"], news_slice[1]["description"]],
        [news_slice[2]["title"], news_slice[2]["description"]]
    ]
    print(news_list)
    client = Client(ACCOUNT_SID, auth_token)
    message = client.messages \
        .create(
        body= f"{ticker} has moved {formula}% \n"
              f"{news_list[0][0]}:\n{news_list[0][1]}"
              f"{news_list[1][0]}:\n{news_list[1][1]}"
              f"{news_list[2][0]:\n{news_list[2][1]}}",
        from_='+19302075053',
        to='' #input your own number to receive message alerts
    )
    print(message.status)

