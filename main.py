from flask import Flask, render_template
import requests
import datetime
import pandas as pd
import plotly
import plotly.express as px
import json
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v3/get-chart"
headers = {
    "X-RapidAPI-Key": os.environ['API_KEY'],
    "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
}

symbols = ["ACC.BO", "VOLTAS.NS", "RELIANCE.BO", "SBIN.NS", "MRF.NS"]
names = ["ACC LTD", "Voltas LTD", "Reliance Industries LTD", "State Bank Of India", "MRF LTD"]
ticker_symbol = ["ACC", "VOLTAS", "RELIANCE", "SBIN", "MRF"]

responses = {}
for symbol, name in zip(symbols, names):
    querystring = {"interval": "1mo", "symbol": symbol, "range": "2y", "region": "IN",
                   "includePrePost": "false", "useYfid": "true", "includeAdjustedClose": "true",
                   "events": "capitalGain,div,split"}
    response = requests.get(url, headers=headers, params=querystring)
    # print(response.json())
    result = response.json()['chart']['result'][0]
    responses[name] = [symbol, [datetime.datetime.fromtimestamp(d).strftime("%d/%m/%Y") for d in result['timestamp']],
                       [round(r, 2) for r in result['indicators']['quote'][0]['close']], len(result['timestamp'])]
# print(responses)


# --------------- Test Data(If you do not have API KEY) -------------------------
# responses = {'ACC LTD': ['ACC.BO', ['01/09/2021', '01/10/2021', '01/11/2021', '01/12/2021', '01/01/2022', '01/02/2022', '01/03/2022', '01/04/2022', '01/05/2022', '01/06/2022', '01/07/2022', '01/08/2022', '01/09/2022', '01/10/2022', '01/11/2022', '01/12/2022', '01/01/2023', '01/02/2023', '01/03/2023', '01/04/2023', '01/05/2023', '01/06/2023', '01/07/2023', '01/08/2023', '11/08/2023'], [2254.5, 2333.5, 2288.05, 2217.4, 2281.3, 2088.6, 2151.75, 2333.45, 2198.05, 2122.4, 2225.35, 2299.45, 2408.55, 2390.35, 2563.7, 2441.4, 1969.35, 1732.25, 1666.75, 1762.95, 1783.85, 1813.65, 1950.1, 1954.65, 1954.65]], 'Voltas LTD': ['VOLTAS.NS', ['01/09/2021', '01/10/2021', '01/11/2021', '01/12/2021', '01/01/2022', '01/02/2022', '01/03/2022', '01/04/2022', '01/05/2022', '01/06/2022', '01/07/2022', '01/08/2022', '01/09/2022', '01/10/2022', '01/11/2022', '01/12/2022', '01/01/2023', '01/02/2023', '01/03/2023', '01/04/2023', '01/05/2023', '01/06/2023', '01/07/2023', '01/08/2023', '11/08/2023'], [1218.05, 1204.55, 1201.0, 1219.15, 1183.3, 1263.15, 1245.4, 1261.55, 1018.05, 972.4, 1004.75, 1001.2, 906.45, 876.2, 819.5, 799.85, 802.65, 892.0, 818.25, 799.05, 821.35, 759.75, 780.1, 828.55, 828.55]], 'Reliance Industries LTD': ['RELIANCE.BO', ['01/09/2021', '01/10/2021', '01/11/2021', '01/12/2021', '01/01/2022', '01/02/2022', '01/03/2022', '01/04/2022', '01/05/2022', '01/06/2022', '01/07/2022', '01/08/2022', '01/09/2022', '01/10/2022', '01/11/2022', '01/12/2022', '01/01/2023', '01/02/2023', '01/03/2023', '01/04/2023', '01/05/2023', '01/06/2023', '01/07/2023', '01/08/2023', '11/08/2023'], [2517.0, 2537.6, 2406.75, 2368.15, 2386.35, 2359.1, 2633.95, 2790.8, 2633.9, 2594.05, 2508.75, 2639.1, 2377.7, 2549.55, 2732.4, 2548.2, 2353.9, 2321.95, 2331.05, 2420.2, 2474.7, 2550.7, 2527.6, 2548.0, 2548.0]], 'State Bank Of India': ['SBIN.NS', ['01/09/2021', '01/10/2021', '01/11/2021', '01/12/2021', '01/01/2022', '01/02/2022', '01/03/2022', '01/04/2022', '01/05/2022', '01/06/2022', '01/07/2022', '01/08/2022', '01/09/2022', '01/10/2022', '01/11/2022', '01/12/2022', '01/01/2023', '01/02/2023', '01/03/2023', '01/04/2023', '01/05/2023', '01/06/2023', '01/07/2023', '01/08/2023', '11/08/2023'], [453.0, 502.15, 460.55, 460.45, 538.3, 483.2, 493.55, 496.3, 468.1, 465.9, 528.35, 531.25, 530.6, 573.8, 602.45, 613.7, 553.5, 522.8, 523.75, 578.3, 579.85, 572.85, 620.2, 574.15, 574.15]], 'MRF LTD': ['MRF.NS', ['01/09/2021', '01/10/2021', '01/11/2021', '01/12/2021', '01/01/2022', '01/02/2022', '01/03/2022', '01/04/2022', '01/05/2022', '01/06/2022', '01/07/2022', '01/08/2022', '01/09/2022', '01/10/2022', '01/11/2022', '01/12/2022', '01/01/2023', '01/02/2023', '01/03/2023', '01/04/2023', '01/05/2023', '01/06/2023', '01/07/2023', '01/08/2023', '11/08/2023'], [79375.55, 77308.15, 74630.8, 73338.0, 72148.1, 65740.95, 65022.1, 72729.0, 77649.45, 70800.9, 83818.15, 85364.95, 81654.55, 90767.0, 93557.55, 88535.45, 90869.4, 85256.6, 84047.2, 89006.8, 97211.7, 101260.5, 102956.25, 105989.25, 105989.25]]}

charts = []
for idx, key in enumerate(responses.keys()):
    df = pd.DataFrame(data={'Date': responses[key][1], 'Price': responses[key][2]}, columns=['Date', 'Price'])
    df['Date'] = pd.to_datetime(df['Date'], format="%d/%m/%Y").dt.date
    df.to_csv(f"./data_files/{key}_{ticker_symbol[idx]}_{df.iloc[0]['Date']}_{df.iloc[-1]['Date']}_211080038.csv",
              columns=['Date', 'Price'], header=True)
    fig = px.line(df, x='Date', y='Price', markers=True, width=600, height=500)
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    charts.append(graph_json)


@app.route("/")
def home():
    return render_template("index.html", data=responses, length=len(responses[names[0]][1]), items=len(names),
                           names=names, charts=charts)


if __name__ == "__main__":
    app.run(debug=True)
