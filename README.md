## like linux top, for nvidia gpus

Call as a python script:
```
python nvidia_gpu_top.py
```

or as a shell script:
```
./nvidia-gpu-top.sh
```

```
usage: nvidia_gpu_top.py [-h] [--refresh REFRESH]

GPU monitoring tool

optional arguments:
  -h, --help         show this help message and exit
  --refresh REFRESH  how often values should refresh (default 1.0s)
```

Output contains:
- Temperature in celsius
- Fan speed percentage
- Memory
- Power usage
- GPU utilization

All rows also include the statistics from the past 5 seconds (min mean max).

![example](http://i.imgur.com/i4KfOsu.png)
