import pandas as pd

from jalas_app.config import TIMING_LOG_ADDRESS

logs = pd.read_csv(TIMING_LOG_ADDRESS, header=None)


print('average response time: {}'.format(logs[4].mean()))
