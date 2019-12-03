#%%

import pandas as pd

from jalas_app.config import MEETING_LOG_ADDRESS

logs = pd.read_csv(MEETING_LOG_ADDRESS, header=None)

finalized_meetings = logs[logs[0] == 'meeting_finalized']
cancelled_meetings = logs[logs[0] == 'meeting_cancelled']

print('cancel_rate: {}'.format(len(cancelled_meetings) / (len(finalized_meetings) + len(cancelled_meetings))))
