import time

INTERVAL = 5
start_t1 = 0

while True:

    start = time.time()

    if start - start_t1 > INTERVAL:
        meas_time_start = time.time()

        time.sleep(2)
        print(f'Messung all {INTERVAL} Sekunden')

        meas_time_end = time.time()
        meas_time = meas_time_end - meas_time_start

        # reset time
        start_t1 = start + meas_time


        time.sleep(0.5)