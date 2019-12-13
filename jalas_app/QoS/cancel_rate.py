#%%

import pandas as pd

from jalas_app.config import Poll_LOG_ADDRESS

logs = pd.read_csv(Poll_LOG_ADDRESS, header=None)

finalized_Polls = logs[logs[0] == 'Poll_finalized']
cancelled_Polls = logs[logs[0] == 'Poll_cancelled']

print('cancel_rate: {}'.format(len(cancelled_Polls) / (len(finalized_Polls) + len(cancelled_Polls))))
