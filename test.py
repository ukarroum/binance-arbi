from binance.spot import Spot
import pandas as pd

client = Spot()

print(client.ticker_price("BTCUSDT"))
