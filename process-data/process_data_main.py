from load_data import describe_data
import glob

if __name__ == "__main__":
    describe_data(glob('/Users/shiran/workspace/muse-lsl/data/visual/P300/shiran/*/data_*.csv'))
