import curses
from nvidia_gpu_top import config


class Window(object):

    def __init__(self):
        # initialize a curses screen/window
        self.w = curses.initscr()
        # the window is full, so stop writing to it
        self.is_full = False

        # create the curses color palette
        curses.start_color()
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)

        # DEBUG: toggle to print colors as integers
        if False:
            for i in range(1, curses.COLORS):
                self.w.addstr(str(i) + ' ', curses.color_pair(i))
            self.w.refresh()
            raise

    def get_color(self, color):
        return {
            'green': curses.color_pair(83),
            'yellow': curses.color_pair(227),
            'red': curses.color_pair(203),
            'blue': curses.color_pair(118),
            'bluebold': curses.color_pair(118) | curses.A_BOLD,
            'purple': curses.color_pair(142),
            'darkgray': curses.color_pair(244),
        }[color.lower()]

    def get_status_color(self, value, min_value, max_value):
        """
        Gets the color for the value supplied, given an interval of allowed
        values. Used to show green/yellow/red colors indicating that the value
        is good/ok/bad.
        """
        val = float(max(value - min_value, 0)) / (max_value - min_value)
        if val < config.THRESHOLD_LOW:
            return self.get_color('green')
        elif val < config.THRESHOLD_HIGH:
            return self.get_color('yellow')
        else:
            return self.get_color('red')

    def getmaxyx(self):
        return self.w.getmaxyx()

    def getyx(self):
        return self.w.getyx()

    def erase(self):
        self.w.erase()

    def refresh(self):
        self.w.refresh()
        # UDPATE THE ``is_full`` FLAG!
        self.is_full = False

    def endwin(self):
        curses.endwin()

    def addstr(self, *args):
        """
        Wrapper for w.addstr that handles going outside the bounds of the
        window.
        """
        # get the max x and y
        maxy, maxx = self.getmaxyx()
        # get the current x and y
        y, x = self.getyx()
        # get the message
        if isinstance(args[0], int) and len(args) >= 3:
            msgidx = 2
        else:
            msgidx = 0

        # add the length of the message to x
        x += len(args[msgidx])

        already_full = self.is_full
        if y + 1 == maxy and args[msgidx][-1] == '\n':
            args = list(args)
            args[msgidx] = args[msgidx].replace('\n', '')
            args = tuple(args)
            # flag that we're full
            self.is_full = True

        # make sure the bounds are still good in the y-axis
        validy = (not already_full and y <= maxy) or \
                 (isinstance(args[0], int) and args[0] < maxy)

        # make sure the bounds are still good in the x-axis
        validx = (x <= maxx) or \
                 (len(args) >= 2
                  and (isinstance(args[1], int)
                  and args[1] < maxx))

        if validx and validy:
            # make sure if that, if we supply x and y coords, they're positive
            if len(args) < 3 or (args[0] >= 0 and args[1] >= 0):
                self.w.addstr(*args)
        elif validy:
            # if the line is too long but the current message has a newline,
            # keep the newline character
            if args[msgidx][-1] == '\n':
                self.w.addstr('\n')
