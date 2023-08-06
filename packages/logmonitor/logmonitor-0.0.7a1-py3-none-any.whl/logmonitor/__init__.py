#!/usr/bin/env python3
import argparse
import pkg_resources
import os.path
from datetime import datetime
from time import sleep
from math import floor
from collections import namedtuple, Counter
from threading import Thread
import errno
from sh import tail
from apachelogs import LogParser, InvalidEntryError
from apachelogs import COMMON as COMMON_LOG_FORMAT
from time_series_moving_stats import TimeSeriesMovingStats


def main():
    version = pkg_resources.get_distribution('logmonitor').version
    description = "Log monitoring application. Press 'q' followed by 'Enter' to quit."

    # Instantiate the argument parser
    arg_parser = argparse.ArgumentParser(description=description)

    # Optional arguments:
    OptArgTuple = namedtuple('OptArg', ['short', 'long', 'type', 'default', 'min', 'max', 'help'])
    opt_args = {"logfile": OptArgTuple('l', 'logfile', str, '/tmp/access.log', None, None,
                                       "Logfile to monitor. Application will exit if it doesn't exist"),
                "update_interval": OptArgTuple('u', 'update-interval', int, 10, 1, None,
                                               'Monitor update interval in seconds.'),
                "alert_request_threshold": OptArgTuple('a', 'alert-request-threshold', int, 10, 1, None,
                                                       "Average number of requests per second that will cause alert if "
                                                       "sustained for more than the alert switch-on threshold. "
                                                       "Overrideable. To override it, press 'a' followed by the new "
                                                       "threshold in seconds and then hit enter during runtime."),
                "alert_switch_on_threshold": OptArgTuple('o', 'alert-switch-on-threshold', int, 120, 1, None,
                                                         'Alert switch-on threshold in seconds. Alert will turn on if '
                                                         'the average number of requests surpasses the average '
                                                         'request threshold for the duration of the switch-on '
                                                         'threshold. Otherwise, alert will be turned off')}

    for arg in opt_args.values():
        allowed_values = ""
        if arg.default:
            allowed_values += " Default: " + str(arg.default)
        if (arg.type is int) or (arg.type is float):
            allowed_values += " Min: " + str(arg.min) + " Max: " + str(arg.max)
        arg_parser.add_argument('-' + arg.short, '--' + arg.long, type=arg.type, default=arg.default,
                                help=arg.help + allowed_values)
    arg_parser.add_argument('-v', '--version', action='version', version=version, help='Version number')

    # Parse arguments:
    args = arg_parser.parse_args()

    # Exit if path is not a file:
    if not os.path.isfile(args.logfile):
        raise ValueError("{} is not a file".format(args.logfile))

    # Check numerical arguments are within bounds:
    for arg_key, arg_tup in opt_args.items():
        if (arg_tup.type is int) or (arg_tup.type is float):
            if arg_tup.min is not None and eval("args.{}".format(arg_key)) < arg_tup.min:
                raise ValueError(
                    "ERROR: value of argument --{} is smaller than its minimum admissible value.".format(arg_tup.long))
            if arg_tup.max is not None and eval("args.{}".format(arg_key)) > arg_tup.max:
                raise ValueError(
                    "ERROR: value of argument --{} is larger than its maximum admissible value.".format(arg_tup.long))

    print(description)

    # Thread stop conditions:
    input_thread_stop = [False]
    monitor_stop = [False]
    alerter_stop = [False]
    collector_stop = [False]

    # Stop all threads:
    def stop_threads():
        input_thread_stop[0] = True
        monitor_stop[0] = True
        alerter_stop[0] = True
        collector_stop[0] = True

    # Instantiate log analyzers:
    now = floor(datetime.now().timestamp())
    alert_log_analyzer = TimeSeriesMovingStats(args.alert_switch_on_threshold, start=now)
    update_interval_log_analyzer = TimeSeriesMovingStats(args.update_interval, start=now)
    section_hit_counter = Counter()

    # Initialize the alert:
    alert = [False]

    # Start a thread that reads the log and inputs data:
    def collector():
        log_parser = LogParser(COMMON_LOG_FORMAT)
        generator = tail("-f", "-n0", args.logfile, _iter_noblock=True, _bg_exc=False)
        for entry in generator:
            if collector_stop[0]:
                generator.kill()
                return

            # When nothing retrieved, add 0 for this timeslot:
            if entry is errno.EWOULDBLOCK:
                current = datetime.now().timestamp()
                alert_log_analyzer.add(floor(current), 0)
                update_interval_log_analyzer.add(floor(current), 0)
                continue

            try:
                parsed_entry = log_parser.parse(entry)
            except InvalidEntryError:

                # discard log entry if you fail to parse it:
                continue

            timestamp = parsed_entry.request_time_fields["timestamp"].timestamp()

            # discard log entry with a timestamp in the future:
            current = datetime.now().timestamp()
            if timestamp > current:
                continue

            # retrieve relevant fields:
            [method, resource, _] = parsed_entry.request_line.split()
            section = resource.split('/')[1]

            # add request to the analyzers:
            # TODO: Consider batched updates.
            alert_log_analyzer.add(floor(timestamp), 1)
            update_interval_log_analyzer.add(floor(timestamp), 1)
            section_hit_counter[section] += 1

    log_collector = Thread(target=collector)
    log_collector.start()

    # Start a thread that detects alerts:
    def alerter():
        alerter_period = 1
        while not alerter_stop[0]:
            hits = alert_log_analyzer.get_average()
            if hits > args.alert_request_threshold:
                if not alert[0]:
                    alert[0] = True
                    print("ALERT ON: High traffic generated an alert - average (hits per second over "
                          "--alert-switch-on-threshold "
                          "period) = {}, triggered at {}".format(hits, datetime.now().isoformat(' ', 'seconds')))
            else:
                if alert[0]:
                    alert[0] = False
                    print("ALERT OFF: Traffic back to normal after an alert, normalized at {}".format(
                        datetime.now().isoformat(' ', 'seconds')))
            sleep(alerter_period)

    log_alerter = Thread(target=alerter)
    log_alerter.start()

    # Start a thread that refreshes the monitor every update-interval seconds:
    def monitor():
        start = datetime.now().isoformat(' ', 'seconds')
        while not monitor_stop[0]:
            stop = datetime.now().isoformat(' ', 'seconds')
            print("***** Statistics for interval: {} to {} *****".format(start, stop))
            print("three most common section hits: {}\ntotal hits: {}\nmoving average (hits per second): {}"
                  "\nmoving variance (hits per second): {}\n".format(section_hit_counter.most_common(3),
                                                                     update_interval_log_analyzer.get_sum(),
                                                                     update_interval_log_analyzer.get_average(),
                                                                     update_interval_log_analyzer.get_variance()))

            section_hit_counter.clear()
            start = stop
            sleep(args.update_interval)

    log_monitor = Thread(target=monitor)
    log_monitor.start()

    # Start a thread that gets input from the terminal:
    def console_input():
        while not input_thread_stop[0]:
            line = input()
            if 'q' == line:
                stop_threads()
                print("quiting...")
            if 'a' == line[0]:
                if line[1:].isdigit():
                    prev = args.alert_request_threshold
                    new = int(line[1:])
                    print("--alert-request-threshold changed from {} to {}.".format(prev, new))
                    args.alert_request_threshold = new
            sleep(.5)

    input_thread = Thread(target=console_input)
    input_thread.start()


if __name__ == '__main__':
    main()
