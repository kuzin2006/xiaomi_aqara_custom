*Known MIIO commands*

### Radio

- `add_channels`
```{«chs»:[{«id»:9999667,»url»:»http://url/live1.m3u8″,»type»:0}]}```

- `remove_channels`
```{«chs»:[{«id»: 9999666,»url»:»http://url/hls/live1.m3u8″,»type»:0}]}```

- `play_specify_fm`
```[9999667,100]```

- `play_fm`
```[«on»]```
[on, off, toggle, next, prev]

- `volume_ctrl_fm`
```[«100»]```

- `add_channels`
```{«chs»:[{«id»:9999667,»url»:»http://url/live1.m3u8″,»type»:0}]}```

- remove_channels
```{«chs»:[{«id»: 9999666,»url»:»http://url/hls/live1.m3u8″,»type»:0}]}```

### Alarm

- Query the status:
```{"id":65005,"method":"get_arming","params":[]}
{"result":["off"],"id":65005}
```

- Query the wait time:
```{"id":65006,"method":"get_arm_wait_time","params":[]}
{"result":[5],"id":65006}
```

- set arming:
```{"id":65013,"method":"set_arming","params":["on"]}
{"result":["ok"],"id":65013}
```

- set arming off:
```{"id":65014,"method":"set_arming","params":["off"]}
{"result":["ok"],"id":65014}
```
