import pandas as pd
import numpy as np

from epw import epw

import seaborn as sns

from case_edits.defaults import WEATHER_FILE
from weather.irrelevant_quantities import irrelevant_qois

# y, month, day, hour minute
N_DATETIME_COLS = 5


class JointAnalysis:
    def __init__(self) -> None:
        self.qois = []
        self.retrieve_data()
        sns.set_theme()
        pass

    def retrieve_data(self):
        self.retrieve_climate_data()
        self.filter_to_summer_data()

    def create_histogram_df(self):
        self.create_histogram()
        self.filter_frequencies()
        self.prepare_filtered_bins()
        self.prepare_frequencies_for_df()
        self.create_frequencies_df()

    def retrieve_climate_data(self):
        epobj = epw()
        epobj.read(WEATHER_FILE)
        self.df = epobj.dataframe
        self.filter_irrelevant_columns()
        

    def filter_to_summer_data(self):
        df = self.filtered_df
        mask = (df["Month"] > 6) & (df["Month"] < 9)
        self.summer_df = df.loc[mask].reset_index(drop=True)

        self.summer_df["Datetime"] = pd.to_datetime(
            self.summer_df[["Year", "Month", "Day", "Hour"]]
        )
        self.summer_qoi_df = self.summer_df[self.potential_qois]


    def update_qois(self, qois: list):
        self.qois = qois

    def create_histogram(self):
        if not self.qois:
            self.qois = ["Dry Bulb Temperature", "Wind Speed"]

        nbins = 6

        qoi_df = self.summer_df[self.qois]
        qoi_arr = qoi_df.to_numpy()

        self.freqs, self.bins = np.histogramdd(qoi_arr, bins=nbins)

    def filter_frequencies(self):
        freqs = self.freqs.flatten()
        sorted_freqs = sorted(freqs, reverse=True)
        self.filtered_freqs = [f for f in sorted_freqs if f > 50]

    def prepare_filtered_bins(self):
        self.nfreqs = len(self.filtered_freqs)
        self.bins_holder = np.zeros((self.nfreqs * 2, len(self.qois) + 1))

        for cnt, freq in enumerate(self.filtered_freqs):
            qoi_indices = np.where(self.freqs == freq)
            row = cnt * 2
            for col, index in enumerate(qoi_indices):
                simple_index = index[0]
                self.bins_holder[row, col] = self.bins[col][simple_index]
                self.bins_holder[row + 1, col] = self.bins[col][simple_index + 1]

    def prepare_frequencies_for_df(self):
        entry_freqs = []
        for freq in self.filtered_freqs:
            entry_freqs.extend([freq, None])

        self.bins_holder[:, -1] = entry_freqs

    def create_frequencies_df(self):
        iterables = [list(range(self.nfreqs)), ["min", "max"]]
        multi_index = pd.MultiIndex.from_product(iterables, names=["index", "bins"])

        names = self.qois + ["Occurences"]
        self.freqs_df = pd.DataFrame(self.bins_holder, index=multi_index, columns=names)

    
    def filter_irrelevant_columns(self):
        df = self.df.drop(irrelevant_qois, axis=1)
        df = df.dropna(axis=1, how="all")

        # drop columns with only one unique value, except for the year
        nunique = df.nunique()
        cols_to_drop = list(nunique[nunique == 1].index)
        if "Year" in cols_to_drop:
            cols_to_drop.remove("Year")
        self.filtered_df = df.drop(cols_to_drop, axis=1)

        self.potential_qois = list(self.filtered_df.columns[N_DATETIME_COLS-1:])


    def jointplot(self):
        if not self.qois:
            self.qois = ["Dry Bulb Temperature", "Wind Speed"]
        return sns.jointplot(
            data=self.summer_df, x=self.qois[0], y=self.qois[1], kind="kde"
        )
    
    def corrplot(self, df=None):
        if not df:
            df = self.summer_qoi_df
        mask = np.triu(np.ones_like(df.corr()))
        heatmap = sns.heatmap(df.corr(), mask=mask, vmin=-1, vmax=1, annot=True, cmap='BrBG')
        return heatmap