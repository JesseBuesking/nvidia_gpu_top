from datetime import datetime


class DeviceHistory(object):
    """
    Keeps track of a device's information, keeping a limited amount depending
    on the value of ``time_range``.
    """

    def __init__(self, time_range):
        self.history = []
        self.time_range = time_range

    def add(self, value):
        if 'timestamp' not in value:
            value['timestamp'] = datetime.utcnow()
        self.history.append(value)
        self.trim_history_()

    def trim_history_(self):
        while True:
            now = datetime.utcnow()
            has_history = len(self.history) > 0
            last_now = self.history[0]['timestamp']
            history_overflows = last_now < (now - self.time_range)
            if not (has_history and history_overflows):
                break
            self.history.pop(0)

    def __len__(self):
        return len(self.history)

    def __getitem__(self, index):
        return self.history[index]
