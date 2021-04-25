import pandas_datareader.data as web
import pandas as pd
import numpy as np


class FinData:
    def __init__(self):
        self.start = None
        self.end = None
        self.symbol = None
        self.indexes = None

    @staticmethod
    def _build_df(df):
        df["Date"] = pd.to_datetime(df["DATE"])
        df["Day"] = [i.day for i in df["Date"]]
        df["Month"] = [i.month for i in df["Date"]]
        df["Year"] = [i.year for i in df["Date"]]
        df.drop(["DATE"], axis=1, inplace=True)
        return df

    @staticmethod
    def _build_technical_df(df):
        df['8ema'] = df['Adj Close'].ewm(span=8, adjust=False).mean()
        df['21ema'] = df['Adj Close'].ewm(span=21, adjust=False).mean()
        df['20sma'] = df['Adj Close'].rolling(window=20).mean()
        df['50sma'] = df['Adj Close'].rolling(window=50).mean()
        df['100sma'] = df['Adj Close'].rolling(window=100).mean()
        df['200sma'] = df['Adj Close'].rolling(window=200).mean()
        return df

    def get_gdp(self, start, end):
        df = web.DataReader("GDP", "fred", start=start, end=end).reset_index()
        df = self._build_df(df)
        return df

    def get_unemployment(self, start, end):
        df = web.DataReader("UNRATE", "fred", start=start, end=end).reset_index()
        df = self._build_df(df)
        return df

    def get_currencies(self, start, end):
        indexes = ["DEXUSEU", "DEXJPUS", "DEXCHUS"]
        df = (
            web.DataReader(indexes, "fred", start=start, end=end)
                .fillna(method="bfill")
                .reset_index()
        )
        df = self._build_df(df)
        df = df.rename(
            columns={"DEXUSEU": "USD/EU", "DEXJPUS": "USD/YEN", "DEXCHUS": "USD/YUAN"}
        )
        return df

    def get_finance_data(self, start, end):
        indexes = [
            "UNRATE",
            "GDP",
            "FPCPITOTLZGUSA",
            "CPALTT01USM657N",
            "RSAFS",
            "USSTHPI",
            "IEABC",
            "GFDEBTN",
            "FEDFUNDS",
            "PAYEMS",
            "DCOILWTICO",
            "GOLDAMGBD228NLBM",
            "PALLFNFINDEXQ",
        ]
        df = (
            web.DataReader(indexes, "fred", start=start, end=end)
                .fillna(0)
                .reset_index()
        )
        df = self._build_df(df)
        df = df.rename(
            columns={
                "FPCPITOTLZGUSA": "INFLATION",
                "CPALTT01USM657N": "CPI",
                "RSAFS": "AdvanceRetailSales",
                "USSTHPI": "HousePrices",
                "IEABC": "BalanceOnCurrentAccount",
                "GFDEBTN": "TotalPublicDebtInMillion",
                "FEDFUNDS": "EffectiveFederalFundsRate",
                "PAYEMS": "TotalNonfarm",
                "DCOILWTICO": "CrudeOil",
                "GOLDAMGBD228NLBM": "Gold",
                "PALLFNFINDEXQ": "CommoditiesIndex",
            }
        )
        return df

    def get_stock(self, symbol, start, end):
        df = web.DataReader(symbol, "yahoo", start=start, end=end).reset_index()
        df["Day"] = [i.day for i in df["Date"]]
        df["Month"] = [i.month for i in df["Date"]]
        df["Year"] = [i.year for i in df["Date"]]
        df = self._build_technical_df(df)
        return df

    @staticmethod
    def get_war_index(start, end):
        df = web.DataReader("ITA", "yahoo", start=start, end=end).reset_index()
        df["Day"] = [i.day for i in df["Date"]]
        df["Month"] = [i.month for i in df["Date"]]
        df["Year"] = [i.year for i in df["Date"]]
        df["Series"] = np.arange(1, len(df) + 1)
        return df

    @staticmethod
    def get_covid_stat():
        data = "https://api.covidtracking.com/v1/us/daily.csv"
        df = pd.read_csv(data).reset_index(drop=True)
        df["Date"] = pd.to_datetime(df["date"], format="%Y%m%d")
        return df