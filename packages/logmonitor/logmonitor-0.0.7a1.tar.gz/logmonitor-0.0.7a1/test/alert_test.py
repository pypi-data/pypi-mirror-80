#!/usr/bin/env python3
import os
from subprocess import Popen, PIPE, DEVNULL
from time import sleep
from datetime import datetime


# Tests that alerts are working as intended. We start a slow log-generator and then we start logmonitor. We do not
# expect any alerts. We continue with a fast log-generator and we expect an alert to trigger. Finally we stop the
# log-generator and we expect a warning indicating the alert is deactivated.

def test_func():
    # clean up procedure in case of exception:
    def cleanup():
        if 'gen' in locals() or 'gen' in globals():
            gen.kill()
        if 'log_monitor_process' in locals() or 'log_monitor_process' in globals():
            log_monitor_process.kill()
        if os.path.isfile(access_log_file):
            Popen(["rm", access_log_file], stdout=DEVNULL, stderr=DEVNULL)
        if os.path.isfile(test_output_file):
            Popen(["rm", test_output_file], stdout=DEVNULL, stderr=DEVNULL)

    try:
        test_output_file = "test_output.out"
        access_log_file = "access.log"
        ON_thres = 10

        # start a slow log generator:
        gen = Popen(["log-generator", "log_schema_slow.yaml"])

        # wait a bit until the log-generator creates the access.log file
        sleep(1)

        # start a log_monitor process:
        ofile = open(test_output_file, "w")
        log_monitor_process = Popen(
            ["python", "../src/logmonitor/__init__.py", "-l", access_log_file, "-o", str(ON_thres)], stdout=ofile,
            stdin=PIPE)

        # no alert should be seen for the next 2*on_thres seconds:
        sleep(2 * ON_thres)

        # kill the slow log generator:
        gen.terminate()

        # start the fast log generator:
        gen = Popen(["log-generator", "log_schema_fast.yaml"])

        # alert should turn on within the next on_thres+1 seconds at most:
        ON_start = datetime.now()
        sleep(ON_thres + 1)
        ON_end = datetime.now()

        # kill the fast log generator:
        gen.terminate()

        # alert should turn off within the next on_thres+1 seconds at most:
        OFF_start = datetime.now()
        sleep(ON_thres + 1)
        OFF_end = datetime.now()

        # quit the log_monitor process:
        log_monitor_process.communicate(input=b'q\n')

        # parse output file and get all lines with the alert and their timestamps
        alerts = []
        with open(test_output_file, 'r') as file:
            for line in file:
                tokens = line.split()
                if tokens and tokens[0] == 'ALERT':
                    alerts.append((tokens[1], datetime.strptime(tokens[-2] + " " + tokens[-1], "%Y-%m-%d %H:%M:%S")))

        cleanup()
    except Exception as e:
        print(str(e))
        cleanup()

    # assert there is one alert turn-on and one turn-off
    print(alerts)
    assert (len(alerts) == 2)
    assert (alerts[0][0] == "ON:")
    assert (alerts[1][0] == "OFF:")

    # assert the timestamps are what's expected
    ON_time = alerts[0][1]
    OFF_time = alerts[1][1]
    print(
        "ON low thres: {}, ON time: {}, ON high thres: {}, OFF low thres: {}, OFF time: {}, OFF high thres: {}".format(
            ON_start, ON_time, ON_end, OFF_start, OFF_time, OFF_end))
    assert (ON_time < OFF_time)
    assert (ON_start <= ON_time < ON_end)
    assert (OFF_start <= OFF_time < OFF_end)


if __name__ == '__main__':
    test_func()
