# globalCounter
Have you ever wanted to achieve **complete order** in a distributed system? **GlobalCounter** is a simple solution. It is a server that works as a **global counter**. This gives you an easy way to locally timestamp functions.

# Description
## Basic Concepts
- **Counter**: It is a program that *counts*. It contains a *dict* of *Topic*->*Sum*. *To count* means adding 1 to a topic's sum. 
- **Topic**: It is a string representing a sum. Its main usage is for having logically several *count*s at the same time.
- **Sum**: It is a topic's count. *Count* and *Sum* are synonyms.

## Asynchronous vs Multiprocess
GlobalCounter supports **asynchronous** and **multiprocessing** Client and Server. 

It uses [Trio](https://github.com/python-trio/trio) for asynchronous programming. The server spawns one coroutine for every request.

For multiprocessing, the Server contains a Pool of processes. The maximum amount of Processes in the Pool, it is specified when initializing the Server Class. By default it is equal to system's cpu amount.

```python
from multiprocessing import Pool, Queue, Manager, cpu_count
...
MAX_WORKERS = cpu_count()
...
def __init__(self, ip="0.0.0.0", port=0, max_workers=MAX_WORKERS):
    ...

```


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


global_counter = UDPCounterServer(ip="127.0.0.1", port=9999, max_workers=4)
global_counter.run()
```

#### TCP Server
```python
from globalCounter.server.counter_server import TCPCounterServer


global_counter = TCPCounterServer(ip="127.0.0.1", port=9999, max_workers=4)
global_counter.run()
```

#### Async UDP Server
```python
import trio

from globalCounter.server.async_counter_server import AsyncUDPCounterServer


async def run_global_counter(global_counter):
    await global_counter.run()

global_counter = AsyncUDPCounterServer(ip="127.0.0.1", port=9999)
trio.run(run_global_counter, global_counter)
```

#### Async TCP Server
```python
import trio

from globalCounter.server.async_counter_server import AsyncTCPCounterServer


async def run_global_counter(global_counter):
    await global_counter.run()

global_counter = AsyncTCPCounterServer(ip="127.0.0.1", port=9999)
trio.run(run_global_counter, global_counter)
```

## Client
#### UDP client
```python
from globalCounter.client.counter_client import count, reset


count_num = count(topic="topic", ip="127.0.0.1", port=9999)

reset(topic="topic", ip="127.0.0.1", port=9999)

```
Using decorators:
```python
from globalCounter.client.counter_client import count_deco


@count_deco(topic="topic", ip="127.0.0.1", port=9999)
def do_something():
    return "Something"


count_num, something = do_something()
```
#### TCP client
```python
from globalCounter.client.counter_client import count, reset

count_num = count(topic="topic", ip="127.0.0.1", port=9999, tcp=True)

reset(topic="topic", ip="127.0.0.1", port=9999, tcp=True)

```
Using decorators:
```python
from globalCounter.client.counter_client import count_deco


@count_deco(topic="topic", ip="127.0.0.1", port=9999, tcp=True)
def do_something():
    return "Something"


count_num, something = do_something()
```
#### Async UDP client
```python
import trio

from globalCounter.client.async_counter_client import count, reset

async def run_count_and_reset():
    count_num = await count(topic="topic", ip="127.0.0.1", port=9999)
    
    await reset(topic="topic", ip="127.0.0.1", port=9999)


trio.run(run_count_and_reset)

```
Using decorators:
```python
import trio
from globalCounter.client.async_counter_client import count_deco


@count_deco(topic="topic", ip="127.0.0.1", port=9999)
def do_something():
    return "Something"


@count_deco(topic="topic", ip="127.0.0.1", port=9999)
async def do_something_async():
    return "Something"


count_num, something = trio.run(do_something)

count_num, something = trio.run(do_something_async)
```
#### Async TCP client
```python
import trio

from globalCounter.client.async_counter_client import count, reset

async def run_count_and_reset():
    count_num = await count(topic="topic", ip="127.0.0.1", port=9999, tcp=True)
    
    await reset(topic="topic", ip="127.0.0.1", port=9999, tcp=True)


trio.run(run_count_and_reset)

```
Using decorators:
```python
import trio
from globalCounter.client.async_counter_client import count_deco


@count_deco(topic="topic", ip="127.0.0.1", port=9999, tcp=True)
def do_something():
    return "Something"


@count_deco(topic="topic", ip="127.0.0.1", port=9999, tcp=True)
async def do_something_async():
    return "Something"


count_num, something = trio.run(do_something)

count_num, something = trio.run(do_something_async)