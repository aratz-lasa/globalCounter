# globalCounter
Have you ever wanted to achieve **complete order** in a distributed system? GlobalCounter is a simple solution. It is a server that works as a **counter**. This gives you an easy way to locally timestamp functions.

# Description
## Basic Concepts
- **Counter**: It is a program that contains a *dict* of *Topic*->*Sum*. *To count* means adding 1 to a topic's sum. 
- **Topic**: It is a string representing a sum. Its main usage is for having logically several *count*s at the same time.
- **Sum**: It is a topic's count. *Count* and *Sum* are synonyms.

## Asynchronous
It supports **asynchronous Client and Server**. 

It uses [Trio](https://github.com/python-trio/trio) for asynchronous programming.

## Transport layer
It supports both **TCP** and **UDP** Client and Server connections.

## Methods
|Method|Description|
|---|----|
|COUNT|Adds 1 to *{topic}*, and returns the value|
|RESET|Sets *{topic}* to 0|

## Protocol
A message is formatted: 
- 1st byte: **OP_CODE**
- Remaining bytes: **Data**
 

|Method|OP_CODE|Data|
|---|---|---|
|COUNT|0|*{topic}*:utf-8 str|
|COUNT response|128|*{sum}*:unsigned number|
|RESET|1|*{topic}*:utf-8 str|
|RESET response|129|_|

# Usage

## Server
#### UDP Server
```python
from globalCounter.server.counter_server import UDPCounterServer


if __name__ == "__main__":
    global_counter = UDPCounterServer(ip="127.0.0.1", port=9999)
    global_counter.run()
```

#### TCP Server
```python
from globalCounter.server.counter_server import TCPCounterServer


if __name__ == "__main__":
    global_counter = TCPCounterServer(ip="127.0.0.1", port=9999)
    global_counter.run()
```

#### Async UDP Server
```python
import trio

from globalCounter.server.async_counter_server import AsyncUDPCounterServer


async def run_global_counter(global_counter):
    await global_counter.run()

if __name__ == "__main__":
    global_counter = AsyncUDPCounterServer(ip="127.0.0.1", port=9999)
    trio.run(run_global_counter, global_counter)
```

#### Async TCP Server
```python
import trio

from globalCounter.server.async_counter_server import AsyncTCPCounterServer


async def run_global_counter(global_counter):
    await global_counter.run()

if __name__ == "__main__":
    global_counter = AsyncTCPCounterServer(ip="127.0.0.1", port=9999)
    trio.run(run_global_counter, global_counter)
```

## Client
#### UDP client

#### TCP client

#### Async UDP client

#### Async TCP client
