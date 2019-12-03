
import pandas as pd
logs = pd.read_csv("time_log.csv", header=None)


#
print('average response time: {}'.format(logs[4].mean()))
