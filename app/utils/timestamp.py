import calendar
import time

# Current GMT time in a tuple format
current_GMT = time.gmtime()

# ts stores timestamp
CURRENT_TIMESTAMP = calendar.timegm(current_GMT)
