#%%

import pandas as pd
logs = pd.read_csv("meetings_log.csv", header=None)

finalized_meetings = logs[logs[0] == 'meeting_finalized']
cancelled_meetings = logs[logs[0] == 'meeting_cancelled']
#
print('cancel_rate: {}'.format(len(cancelled_meetings) / (len(finalized_meetings) + len(cancelled_meetings))))
