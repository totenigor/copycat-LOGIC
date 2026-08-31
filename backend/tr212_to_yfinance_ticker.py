def convert_tr212_to_yfinance(tr212Ticker: str) -> str:

    if tr212Ticker.endswith("_US_EQ"):

        shortName = tr212Ticker.removesuffix("_US_EQ")
        return shortName

    elif tr212Ticker.endswith("l_EQ"):

        shortName = tr212Ticker.removesuffix("l_EQ")
        return f"{shortName}.L"

    elif tr212Ticker.endswith("_DE_EQ"):

        shortName = tr212Ticker.removesuffix("_DE_EQ")
        return f"{shortName}.DE"

    elif tr212Ticker.endswith("_FR_EQ"):

        shortName = tr212Ticker.removesuffix("_FR_EQ")
        return f"{shortName}.PA"

    else:

        shortName = tr212Ticker.partition("_")[0]
        return shortName


