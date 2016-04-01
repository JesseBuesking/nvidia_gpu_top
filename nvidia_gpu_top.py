"""Renders valuable GPU information like linux ``top``."""


import argparse
from nvidia_gpu_top import device
from nvidia_gpu_top import window
import os
import pynvml
from time import sleep


def pargs():
    """Parse out the arguments supplied."""
    parser = argparse.ArgumentParser(description='GPU monitoring tool')

    parser.add_argument(
        '--refresh', default=1.0, action='store',
        help='how often values should refresh (default 1.0s)', type=float)

    return parser.parse_args()


def print_driver_info(maxyx):
    """Basic driver versioning information."""
    msg = 'Driver Version: {}'.format(pynvml.nvmlSystemGetDriverVersion())
    w.addstr(0, maxyx[1] - len(msg), msg)


if __name__ == '__main__':
    pynvml.nvmlInit()

    argu = pargs()

    # get devices
    devices = []
    deviceCount = pynvml.nvmlDeviceGetCount()
    for i in range(deviceCount):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        gpuid = i
        devices.append(device.Device(handle, gpuid))

    try:
        # hide the curor -- looks cleaner
        os.system('setterm -cursor off')
        w = window.Window()
        while True:
            # clear the terminal window to start
            w.erase()

            # loop over devices, printing information
            for idx, d in enumerate(devices):
                d.print_device_info(w)

            # print driver version info
            print_driver_info(w.getmaxyx())

            # update the window with the output
            w.refresh()

            # delay
            sleep(argu.refresh)
    except KeyboardInterrupt:
        pass
    finally:
        os.system('setterm -cursor on')
        w.endwin()
