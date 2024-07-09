from case_edits.defaults import WEATHER_FILE

from epw import epw

import seaborn as sns

import pandas as pd
import numpy as np


class JointAnalysis:
    def __init__(self) -> None:
        self.qois = []
        self.retrieve_data()
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

    def filter_to_summer_data(self):
        mask = (self.df["Month"] > 6) & (self.df["Month"] < 9)
        self.summer_df = self.df.loc[mask].reset_index(drop=True)

        self.summer_df["Datetime"] = pd.to_datetime(
            self.summer_df[["Year", "Month", "Day", "Hour"]]
        )

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

    def plot(self):
        return sns.jointplot(
            data=self.summer_df, x=self.qois[0], y=self.qois[1], kind="kde"
        )
