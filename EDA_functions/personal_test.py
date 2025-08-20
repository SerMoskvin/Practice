from read_and_clean import *
from analyze import *

data = load_data()
data = clean_data(data)
train_data = prepare_for_prophet(data)
setup_visuals()

plot_all_analysis(data)
