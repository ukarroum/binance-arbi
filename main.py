from binance.spot import Spot
import pandas as pd


def get_symbol_sets(client):
    return {d['symbol']: (d['baseAsset'], d['quoteAsset']) for d in client.exchange_info()['symbols']}


def get_prices(client):
    symbols = get_symbol_sets(client)

    df = pd.DataFrame(data=client.ticker_price())

    df['base'] = df.symbol.map({key: val[0] for key, val in symbols.items()})
    df['quote'] = df.symbol.map({key: val[1] for key, val in symbols.items()})

    return df


if __name__ == '__main__':
    client = Spot()

    df = get_prices(client)

    print(df)