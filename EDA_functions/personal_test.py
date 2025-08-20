from read_and_clean import *

data = load_data()
clean_data(data)
train_data = prepare_for_prophet(data)
