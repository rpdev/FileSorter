import time
import sys
for t in range(100):
    sys.stdout.write('\r'+str(t))
    sys.stdout.flush()
    time.sleep(0.10)