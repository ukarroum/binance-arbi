from binance import Client
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from functools import lru_cache


@lru_cache(None)
def get_symbol_sets(client):
    return {d['symbol']: (d['baseAsset'], d['quoteAsset']) for d in client.get_exchange_info()['symbols']}


def get_prices(client):
    symbols = get_symbol_sets(client)

    df = pd.DataFrame(data=client.get_all_tickers())

    df['base'] = df.symbol.map({key: val[0] for key, val in symbols.items()})
    df['quote'] = df.symbol.map({key: val[1] for key, val in symbols.items()})

    df['price'] = -np.log(df['price'].astype(float))

    return df


if __name__ == '__main__':
    client = Client()

    print("Running...")
    while True:

        df = get_prices(client)

        G = nx.from_pandas_edgelist(df, "base", "quote", ["price"], create_using=nx.DiGraph())

        nx.draw(G, with_labels=True, font_weight='bold')

        if nx.negative_edge_cycle(G):
            print("You win")
