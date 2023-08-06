from collections import deque
from threading import Lock


class TimeSeriesMovingStats:
    def __init__(self, window: int, start: int):
        self.lock = Lock()
        self.window = window
        self.start = start
        self.buffer = deque(maxlen=self.window)
        self.sum = 0
        self.avg = 0
        self.square_sum = 0
        self.var = 0

    def add(self, timeslot: int, data: float):
        with self.lock:

            # ignore if timeslot is less than the start of the window:
            if timeslot < self.start:
                return

            # compute position of the circular buffer relative to the start:
            relative_pos = timeslot - self.start

            # previous data point:
            prev = 0

            # if relative_pos is within the current buffer, simply insert the data:
            if relative_pos < len(self.buffer):
                prev = self.buffer[relative_pos]
                self.buffer[relative_pos] += data

            # if relative_pos is between the end of current buffer and the window, pad zeros:
            elif (relative_pos >= len(self.buffer)) and (relative_pos < self.window):
                for _ in range(len(self.buffer), relative_pos + 1):
                    self.buffer.append(0)
                self.buffer[-1] += data

            # if relative_pos is above the window, we need to resize the window
            else:

                # if the length of the circular buffer is less than the length of the window, pad with 0s:
                for _ in range(len(self.buffer), self.window):
                    self.buffer.append(0)

                # evict items from the circular buffer until the start of the new window:
                diff = relative_pos + 1 - self.window
                for _ in range(diff):
                    self.sum -= self.buffer[0]
                    self.square_sum -= (self.buffer[0] ** 2)
                    self.buffer.append(0)
                self.buffer[-1] += data
                self.start += diff

            # compute the statistics:
            self.sum += data

            # solving this for y: x^2 + y == (x+d)^2 => y == d^2 + 2xd
            # gives what we need to add to update the square sum:
            self.square_sum += (data ** 2) + 2 * data * prev
            self.avg = self.sum / len(self.buffer)
            self.var = self.square_sum / len(self.buffer) - (self.avg ** 2)

    def get_value(self, timeslot: int) -> float:
        with self.lock:
            buffer_pos = timeslot - self.start
            if buffer_pos < 0 or buffer_pos >= len(self.buffer):
                return 0
            return self.buffer[buffer_pos]

    def get_sum(self) -> float:
        with self.lock:
            return self.sum

    def get_average(self) -> float:
        with self.lock:
            return self.avg

    def get_variance(self) -> float:
        with self.lock:
            return self.var
