from read_and_clean import *
from analyze import *
from basic_stats import *
from model_forecast import *

data = load_data()
data = clean_data(data)
train_data = prepare_for_prophet(data)
setup_visuals()

plot_all_analysis(data)
run_full_analysis()

