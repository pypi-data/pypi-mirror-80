# Ping tester

Simple module for ping testing 


## Usage
```bash
pip install dev-ping-tester
```

```python
# For Huawei Device
from dev_ping_tester.Huawei import Huawei


h= Huawei("DeviceName","IP",PORT,"Username","Password","telnet/ssh")
packet_drop, min_latency, avg_latency, max_latency = h.ping("192.168.0.10",10)
# 192.168.0.10 is destination and 10 is count
```

```python
# For Cisco Device
from dev_ping_tester.Cisco import Cisco


h= Cisco("DeviceName","IP",PORT,"Username","Password","telnet/ssh")
packet_drop, min_latency, avg_latency, max_latency = h.ping("192.168.0.10",10)
# 192.168.0.10 is destination and 10 is count

```


```python
# For Auto detect Device Type
from dev_ping_tester.AutoDetectDevice import AutoDetectDevice


a= AutoDetectDevice("DeviceName","IP",PORT,"Username","Password","telnet/ssh")
packet_drop, min_latency, avg_latency, max_latency = a.ping("192.168.0.10",10)
# 192.168.0.10 is destination and 10 is count

```