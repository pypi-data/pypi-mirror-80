## RPBot

[![Build Status](https://travis-ci.com/doyou89/RPBot.svg?branch=master)](https://travis-ci.com/doyou89/RPBot)

RPBot is a Python script to serialize `Robot Framework`  output files into
a ReportPortal. This way the future `Robot Framework` related tools and
plugins will have a unified storage for the test run results.

RPBot is a fork of DbBot-SQLAlchemy project that is using SQLAlchemy in order
to store test run results in any of the major supported database systems.

### Requirements

RPBot is tested on

-  `Python` 3.5+
-  `Robot Framework` 3.0+

It may (though it is not guaranteed) work with older versions of dependencies.

### How it works

The script takes one or more `output.xml` files as input, and stores
the respective results into a ReportPortal

### Installation

This tool is installed with pip with command:
```sh
$ pip install rpbot
```

Alternatively you can download the `source distribution`, extract it and
install using:

```sh
$ python setup.py install
```

### License

RpBot is released under the `Apache License, Version 2.0`.

See LICENSE.TXT for details.
