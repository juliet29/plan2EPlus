from plan2eplus.studies.analysis.plot_helpers import plot_zone_domains
import matplotlib.pyplot as plt
from geomeppy import IDF

def plot_case(idf: IDF):
    fig, ax = plt.subplots()
    plot_zone_domains(idf, ax)
    plt.show()
    