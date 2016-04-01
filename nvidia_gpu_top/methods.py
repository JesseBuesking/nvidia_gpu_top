"""
See http://docs.nvidia.com/deploy/nvml-api/group__nvmlDeviceQueries.html#group__nvmlDeviceQueries
for things that can be queried.
"""


import pynvml


def get_gpu_util(handle):
    util = -1
    try:
        util = pynvml.nvmlDeviceGetUtilizationRates(handle)
        util = util.gpu
    except Exception:
        raise
    return util


def get_power(handle):
    power_usage = -1
    power_max = -1
    power_percent = -1
    try:
        # defaults to milliwatts
        power_usage = pynvml.nvmlDeviceGetPowerUsage(handle)
        power_usage = power_usage / 1000.
        # defaults to milliwatts
        power_max = pynvml.nvmlDeviceGetEnforcedPowerLimit(handle)
        power_max = power_max / 1000

        power_percent = (float(power_usage) / power_max) * 100.
    except Exception:
        pass
    return power_usage, power_max, power_percent


def get_temperature(handle):
    temp = -1
    try:
        temp = pynvml.nvmlDeviceGetTemperature(handle,
                                               pynvml.NVML_TEMPERATURE_GPU)
    except Exception:
        pass

    return temp


def get_fan_speed(handle):
    fan = -1
    try:
        fan = pynvml.nvmlDeviceGetFanSpeed(handle)
    except Exception:
        pass

    return fan


def get_memory_information(handle):
    mem_total = -1
    mem_used = -1
    mem_percent = -1
    try:
        memInfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
        mem_total = memInfo.total / 1024 / 1024
        mem_used = memInfo.used / 1024 / 1024
        mem_percent = (float(memInfo.used) / memInfo.total) * 100.
    except Exception:
        pass

    return mem_used, mem_total, mem_percent
