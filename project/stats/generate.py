from create_dataframe import default_frame
from plotting import generate_plots
from tex import generate_figures
import matplotlib.pyplot as plt
from matplotlib import rc

rc('text', usetex=True)
frame = default_frame()
generate_plots(plt, frame)