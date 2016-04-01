from datetime import timedelta
from nvidia_gpu_top import config
from nvidia_gpu_top import devicehistory
from nvidia_gpu_top import iteminfo
from nvidia_gpu_top import methods
import pynvml


class Device(object):

    def __init__(self, handle, gpuid, timerng_s=5.):
        """
        :param handle: a device handle
        :param gpuid: the id of the gpu
        :param timerng_s: the time range, in seconds, that we'll keep history
        """
        self.handle = handle
        self.gpuid = gpuid
        self.name = pynvml.nvmlDeviceGetName(self.handle)

        self.timerng = timedelta(seconds=timerng_s)
        self.history = devicehistory.DeviceHistory(self.timerng)

    def update_info(self):
        temp = methods.get_temperature(self.handle)
        fan = methods.get_fan_speed(self.handle)
        mem_used, mem_total, mem_percent = methods.get_memory_information(
            self.handle)
        power_usage, power_max, power_percent = methods.get_power(self.handle)
        gpu_util = methods.get_gpu_util(self.handle)

        self.history.add({
            'temp': iteminfo.ItemInfo('temp', temp),
            'fan': iteminfo.ItemInfo('fan', fan),
            'mem_used': iteminfo.ItemInfo('mem_used', mem_used),
            'mem_total': iteminfo.ItemInfo('mem_total', mem_total),
            'mem_percent': iteminfo.ItemInfo('mem_percent', mem_percent),
            'power_usage': iteminfo.ItemInfo('power_usage', power_usage),
            'power_max': iteminfo.ItemInfo('power_max', power_max),
            'power_percent': iteminfo.ItemInfo('power_percent', power_percent),
            'gpu_util': iteminfo.ItemInfo('gpu_util', gpu_util),
        })

    def print_device_info(self, w):
        """
        Prints information for the current device, like temperature, fan speed,
        and memory usage.
        """
        # print the devices name
        w.addstr(
            '  [{}] {}\n'.format(self.gpuid, self.name),
            w.get_color('bluebold'))

        self.update_info()
        data = self.history[-1]

        # print temperature info
        temp = data['temp']
        temp_color = w.get_status_color(
            temp.value, config.MIN_TEMP, config.MAX_TEMP)
        w.addstr('    {:20}'.format('Temperature'))
        w.addstr('{}C'.format(temp.value), temp_color)
        # temperature stats
        w.addstr(' ({:.1f}C {:.1f}C {:.1f}C)\n'.format(
            temp.min(self.history),
            temp.mean(self.history),
            temp.max(self.history)),
            w.get_color('darkgray'))

        # print fan info
        fan = data['fan']
        fan_color = w.get_status_color(
            fan.value, config.MIN_FAN, config.MAX_FAN)
        w.addstr('    {:20}'.format('Fan Speed'))
        w.addstr('{}%'.format(fan.value), fan_color)
        # fan stats
        w.addstr(' ({:.1f}% {:.1f}% {:.1f}%)\n'.format(
            fan.min(self.history),
            fan.mean(self.history),
            fan.max(self.history)),
            w.get_color('darkgray'))

        # print memory info
        mem_used = data['mem_used']
        mem_total = data['mem_total']
        mem_percent = data['mem_percent']

        mem_color = w.get_status_color(mem_used.value, 0, mem_total.value)
        w.addstr('    {:20}'.format('Memory'))
        w.addstr('{}MB / {}MB'.format(mem_used.value, mem_total.value))
        w.addstr(' ({:.1f}%)'.format(mem_percent.value), mem_color)
        # memory stats
        w.addstr(' ({:.1f}% {:.1f}% {:.1f}%)\n'.format(
            mem_used.min(self.history, mem_total.value),
            mem_used.mean(self.history, mem_total.value),
            mem_used.max(self.history, mem_total.value)),
            w.get_color('darkgray'))

        # print power
        power_usage = data['power_usage']
        power_max = data['power_max']
        power_percent = data['power_percent']

        power_color = w.get_status_color(power_usage.value, 0, power_max.value)
        w.addstr('    {0: <20}'.format('Power Usage'))
        w.addstr('{:.1f}W / {}W'.format(power_usage.value, power_max.value))
        w.addstr(' ({:.1f}%)'.format(power_percent.value), power_color)
        # power stats
        w.addstr(' ({:.1f}W {:.1f}W {:.1f}W)\n'.format(
            power_usage.min(self.history),
            power_usage.mean(self.history),
            power_usage.max(self.history)),
            w.get_color('darkgray'))

        # print utilization
        gpu_util = data['gpu_util']
        gpu_color = w.get_status_color(gpu_util.value, 0, 100)
        w.addstr('    {:20}'.format('GPU-Util'))
        w.addstr('{}%'.format(gpu_util.value), gpu_color)
        # gpu util stats
        w.addstr(' ({:.1f}% {:.1f}% {:.1f}%)\n'.format(
            gpu_util.min(self.history),
            gpu_util.mean(self.history),
            gpu_util.max(self.history)),
            w.get_color('darkgray'))
