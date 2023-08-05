# multiport

multiport is a basic [TCP](https://en.wikipedia.org/wiki/Transmission_Control_Protocol) [port scanner](https://en.wikipedia.org/wiki/Port_scanner) written in Python.

## How to install

multiport is available on PyPI and can be installed via

```shell
$ pip install multiport
```

It is recommended to use it in a [virtual environment](https://docs.python.org/3/tutorial/venv.html).

## How to use

multiport has to ways of defining ports, via `--ports` or via a combination of `--min-port` and `--max-port`.


### `--ports`

This option allows a user to enter one or more ports that will be scanned, e.g.

```shell
$ multiport --host localhost --ports 80
$ multiport --host localhost --ports 80 --ports 443
```

This option will take precedence over the other options, they are mutually exclusive.

### `--min-port` and `--max-port`

These options allow a user to define a range of ports between `--min-port` and `--max-port` instead of a discrete list. If only one is set, the other defaults to 1 (in case of `--min-port`) or 65535 (in case of `--max-port`).

```shell
$ multiport --host localhost --min-port 1024                # will scan all ports in the range 1024 to 65535 
$ multiport --host localhost --max-port 1024                # will scan all ports in the range 1 to 1024
$ multiport --host localhost --min-port 512 --max-port 1024 # will scan all ports in the range 512 to 1024
```

If `--ports` is used, neither `--min-port` nor `--max-port` will have an effect.

## Performance

The [`multiport.scanner.Scanner`](./multiport/scanner.py) class implements port scanning based on the [socket](https://docs.python.org/3/library/socket.html) library. This is written synchronously and therefore blocks on each port, until the scan is done. To improve this, the scanning could be implement using e.g. asyncio or threads to speed things up.