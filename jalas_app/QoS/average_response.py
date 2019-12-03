import pandas as pd

from jalas_app.config import TIMING_LOG_ADDRESS

logs = pd.read_csv(TIMING_LOG_ADDRESS, header=None)


print('average response time: {}ms'.format(int(logs[4].mean()/1000)))
