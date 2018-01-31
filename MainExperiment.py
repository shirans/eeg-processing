from experiment.experiemnt_old import Experiment
from experiment.p300 import P300

if __name__ == "__main__":
    # Experiment(3).start()
    P300(False, "/Users/shiran/workspace/stimulis/cars/*","/Users/shiran/workspace/stimulis/flowers/*").start_experiment()