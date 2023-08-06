# Introduction

**logmonitor** is a console application written in python that follows an actively written Common Log Format log file
for HTTP traffic and displays useful statistics at a specific time interval defined by the user. In addition, it
displays alerts when web traffic derived from the log exceeds *on average* a user defined threshold at a user defined
interval. **logmonitor** is build with ease of installation, ease of use and flexibility in mind.
Effort is therefore concentrated on packaging, interfacing, a scalable design and documentation.

# Requirements

Some of the requirements were directly communicated to the author of this work (in **bold**). Others are the author's
own assumptions (left in plain text): 

 * **Ability to follow a Common Log Format log written in real time.**
   * **https://en.wikipedia.org/wiki/Common_Log_Format**
   * If the logfile is not present, exit.
   * **Follow the log file from the end of the last entry.**
 * Be able to work with the following log entry traffic characteristics:
   * Log entries can be written asynchronously and potentially out of order.
   * Log entries with timestamps indicating a future time beyond the application's current time will be discarded.
   * Log entries with timestamps indicating a past time below the monitoring and alert threshold time windows will be
     discarded.
   * Log entries that do not conform to the Common Log Format will be discarded.
 * **For a user defined interval, display statistics derived from the log.**
   * **The three website sections with the most hits and their number of hits.**.
     * If there are less than three sections, all sections are printed.
     * Sections can be added or removed arbitrarily.
       * They are parsed from the log.
   * Moving average of the number of hits per second.
   * Moving variance of the number of hits per second.
 * **Generate alerts when average web traffic, measured in website hits per second, over a user-defined interval
     exceeds a user defined threshold.**
   * **The user defined threshold can be changed at runtime.**
   * **A timestamp is displayed, indicating when the alert activated.**
 * **Display a message indicating when the alert deactivates due to normalization of traffic**
   * **A timestamp is displayed, indicating when the alert deactivated.**
 * Must be easy to install, build, interact with basic knowledge on how to install python packages.
 * **Ability to work for both low and high loads of log traffic (scalability).**

# Interface

Users will interface to the application through a command line. Users will be able to set the parameters to the
application at start time. Users will be able to change some of the parameters of the application during runtime, as per
the requirements. A *--help* command line option should result in the display of all options and arguments. A
 *--version* command line option should result in the display of the version of the application. A typical *--help*
output should look like this:
  
````
usage: __init__.py [-h] [-l LOGFILE] [-u UPDATE_INTERVAL]
                   [-a ALERT_REQUEST_THRESHOLD] [-o ALERT_SWITCH_ON_THRESHOLD]
                   [-v]

Log monitoring application. Press 'q' followed by 'Enter' to quit.

optional arguments:
  -h, --help            show this help message and exit
  -l LOGFILE, --logfile LOGFILE
                        Logfile to monitor. Application will exit if it
                        doesn't exist Default: /tmp/access.log
  -u UPDATE_INTERVAL, --update-interval UPDATE_INTERVAL
                        Monitor update interval in seconds. Default: 10 Min: 1
                        Max: None
  -a ALERT_REQUEST_THRESHOLD, --alert-request-threshold ALERT_REQUEST_THRESHOLD
                        Average number of requests per second that will cause
                        alert if sustained for more than the alert switch-on
                        threshold. Overrideable. To override it, press 'a'
                        followed by the new threshold in seconds and then hit
                        enter during runtime. Default: 10 Min: 1 Max: None
  -o ALERT_SWITCH_ON_THRESHOLD, --alert-switch-on-threshold ALERT_SWITCH_ON_THRESHOLD
                        Alert switch-on threshold in seconds. Alert will turn
                        on if the average number of requests surpasses the
                        average request threshold for the duration of the
                        switch-on threshold. Otherwise, alert will be turned
                        off Default: 120 Min: 1 Max: None
  -v, --version         Version number
````  

A display of statistics during a monitoring interval looks like this:

````
***** Statistics for interval: 2020-09-27 16:00:11 to 2020-09-27 16:00:21 *****
three most common section hits: [('users', 22), ('events', 17), ('alerts', 16)]
total hits: 120
average (hits per second): 12.0
variance (hits per second): 96.0
````

A display of an alert warning looks like this:

````
ALERT ON: High traffic generated an alert - average (hits per second over --alert-switch-on-threshold period) = 12.0, triggered at 2020-09-27 16:00:03
````

````
ALERT OFF: Traffic back to normal after an alert, normalized at 2020-09-27 16:01:57
````

# Details
The architecture of this project is designed as follows:

 * This is a threaded application. We use 4 threads and a parallel process which will be explained below.
 * Argument parsing logic parses the command line arguments of the application and checks them for consistency.
 * When arguments are verified, the application initializes the common, thread safe data structures used by all the
   the threads.
 * When those data structures have been initialized, we start 4 threads, one for a specific function of the application
   * A **collector** thread:
     * Runs continuously.
     * Starts a *tail -f* process that follows the logfile for as long as the thread is alive and
       retrieves new entries.
     * Parses the entries and derives values relevant to the statistics and metrics that are counted, as per
       the requirements.
     * Discards stale, future or malformed entries as per the requirements.
     * Pushes the data to the common data structures of the threads where they are being processed to compute the
       relevant statistics (see the *TimeSeriesMovingStats* class)
   * An **alerter** thread:
     * Runs every second.
     * Manages the alerts by retrieving the state of the common data structures.
     * When the alert is off, checks whether the moving average HTTP hit count within the window, as defined by the user
       exceeds the user defined threshold and prints an alert with the current timestamp if that is the case.
     * When the alert is on, checks whether the moving average HTTP hit count within the window, as defined by the user
       is below the user defined threshold, deactivates the alert and prints a message for this event with the current
       timestamp.
   * A **monitor** thread:
     * Runs every monitoring interval as defined by the user.
     * Retrieves the state of the common data structures and prints the statistics defined by the requirements to the
       user.
   * A **user input** thread:
     * Runs every half a second.
     * Monitors user keyboard input and informs the other threads through communication with the common data structures.
     * Stops all threads when the user wants to quit the application.
     
Most of the components required for building this project can be found from other projects. For example, the **sh**
python module can be used to start the *tail -f* process. **apachelog** can be used to parse the log entries for the
Common Log Format. **log-generator** can be used to generate logs for testing. **pytest** can be used for
running the actual tests. And of course in-build python libraries for everything else. 

However, our research failed to find a suitable library for the common data structures of all threads. The
 requirements here are as follows:

 * We know the number of elements we need to keep for a specific time window (the number of seconds in the window) so
   the space has to be allocated once and be static (however, the contents of said space are NOT static).
 * We need to be able to add/remove new elements in O(1) time
   * Since log entries can come out of order, we need to be able to do that for arbitrary positions in the data
     structure (random access).
 * We need to be able to compute the new average/variance in O(1) time when new information arrives.
 * We need to retrieve the new average/variance in O(1) time.
 * Thread safety.
 
We were unable to find a ready made data structure that would fulfill these requirements. **pandas** and **pyspark** 
were considered, however their use cases indicated that they are more suited for static time series, not time series
were new elements are added constantly and old ones removed. If you think such a structure exists, please contact the
author of this application!

Subsequently we decided to build a specialized data structure for the task. The result is the *TimeSeriesMovingStats*
class. This class is essentially a circular buffer implemented with a python *deque* with a *maxlen* argument. Each
entry in the buffer represents the value of a statistic at a specific second of time. Statistics can be added to it
anywhere (not only front and back) in O(1) time. Additionally, when new statistics are entered, we keep a running sum
and a running sum of squares that are computed in O(1) time on statistic entry and which can then be used to compute
the running average and variance in O(1) time as well. We keep the average, variance and sum statistics in memory
for quick retrieval when those are requested. Thread safety is ensured by python thread primitives.

*TimeSeriesMovingStats* is the main component of scalability. Do notice that, no matter how fast new entries are
added to the log in a second, their number will be summed into a single integer and stored into the data structure
for that second; a 2 minute window means 120 integer values, even if thousands of log entries arrived during the time.
Additionally, that data structure can process new entries in O(1) time. In this situation, the actual bottleneck is
the speed of tailing the file and parsing its entries. On the other hand, a further optimization we could consider is
batched updates on the data structures every set interval (for example, every second).

# Additional Considerations:
Our object oriented design is kept at a minimum at this point. The only class we have is the *TimeSeriesMovingStats*
whose function and responsibilities are well understood. One could either consider this a design advantage or
disadvantage, however we believe it's early in the project's lifetime to decide on class structure given that the
initial requirements, as were communicated to the author of this project left a lot of room for interpretation. That
means assumptions had to be made on the part of the author; a bad assumption could lead to a bad object oriented
design which would cost a lot in time and effort to change later on. Therefore, the project was designed with
flexibility in mind; once the requirements are more robust, we can decide on a more permanent class structure, class
responsibilities, communication etc. This requires additional communication with the customer.

We have kept new features at a minimum. However we design with adaptability in mind; it should be easy with the
current design to add, for example, a failed requests counter, or monitor multiple windows (another instance of 
*TimeSeriesMovingStats*) or spikes (entries with two times the standard deviation which can be derived from the
variance). Most of the interesting statistics we could need in the future can be derived from the basic ones we have
here (averages, variances, hit counts, sums etc)
 
# Packaging
Python project packaging was used for this project. This is due to its simplicity of usage for an end user; a single
 *pip install logmonitor* command is the only thing required to install the package.
 
For more information, you can check here:

https://packaging.python.org/guides/distributing-packages-using-setuptools/#packaging-and-distributing-projects

# Testing
We consider testing to be a lacking feature of this work; the fact is there was not enough time to write all the tests 
we would like. However, the testing that is there is an extensive integration test, where we test that alerts are
working as intended. For this alone to work, most of the commonly used control flow paths of the application need to
work.

To run the tests, you need to have **pytest** and log-generator installed:

````
pip install pytest, log-generator
````

Afterwards, you can go to the *test/* folder and run:

````
pytest
````

Additional tests we would like to add:

 * Extensive testing for the *TimeSeriesMovingStats* class
 * Extensive testing for graceful exit on faulty inputs
   * Threads terminate safely.
   * Generated files are cleaned.

# Ideas for Future Work:
 * More tests need to be added. Unfortunately, time constraints did not allow for more.
 * The time intervals have a slow imperceptible drift of a few milliseconds due to the threaded
   nature of the application. This can and should be amended.
 * Extend or suppress, or add new monitoring intervals during runtime
 * Design alert as a hysteretic system; currently, the alert has no cool-down and therefore can go ON or OFF within
   seconds. This will be confusing, especially for a log file that is being written to with high variability in hits per
   second (too many hits at a time, too little at the next second). The fact that the alert triggers on the moving
   average of a period doesn't matter because that moving average can change between seconds from above the threshold to
   bellow, depending on the hit values added/evicted. Therefore alerts would need to be triggered with a certain delay.
 * Expand to follow multiple logs.
 * Expand for multiple alerts on multiple statistics (hits per second, failed HTTP requests, traffic spikes/lows etc)
 * Expand to follow multiple time intervals
 * Currently, each moving statistics interval has its own dedicated memory for the traffic samples it follows. Ideally
   , we would like those memories to overlap, since a time window of two minutes shares the traffic samples of a time
   window of one minute
 * Display numbers of successful/unsuccessful HTTP requests
 * Display traffic spikes (for example when hits during a second are above two times the standard deviation)
 * Security: Make sure that log file parsing does not exceed memory/computing resources dues to malevolent entries.
 * Object oriented design needs more sophistication once requirements are more robust.
 * Batch update *TimeSeriesMovingStats* data structures instead of adding new entries one by one.
 