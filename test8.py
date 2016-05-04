

import time
SEEDERS_INTERVAL = 300

time1 = time.time()
while True:
    if time.time() - time1 >= float(SEEDERS_INTERVAL):
        print 1
