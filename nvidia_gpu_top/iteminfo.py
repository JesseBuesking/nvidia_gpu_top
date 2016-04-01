

class ItemInfo(object):
    """
    Information for a metric we're tracking. Has methods for getting
    min/mean/max for the metric from the current history.
    """

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def min(self, history, maximum=None):
        value = min([i[self.name].value for i in history])
        if maximum is not None:
            value = value / float(maximum)
        return value

    def mean(self, history, maximum=None):
        value = sum([i[self.name].value for i in history]) / float(len(history))
        if maximum is not None:
            value = value / float(maximum)
        return value

    def max(self, history, maximum=None):
        value = max([i[self.name].value for i in history])
        if maximum is not None:
            value = value / float(maximum)
        return value
