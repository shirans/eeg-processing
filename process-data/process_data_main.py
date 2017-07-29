from load_data import describe_data
from glob import glob

if __name__ == "__main__":
    files = glob('/Users/shiran/workspace/muse-lsl/data/visual/P300/shiran/muse_monitor_dogs/data_2017-07-29-13.21.06.csv')
    describe_data(files)
