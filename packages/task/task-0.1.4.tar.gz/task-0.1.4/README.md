# task

[![Build Status](http://drone.matteyeux.com:8080/api/badges/matteyeux/task/status.svg)](http://drone.matteyeux.com:8080/matteyeux/task)

Taskwarrior-like CLI tool

```
Usage: task [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --version  print version
  --help         Show this message and exit.

Commands:
  add   Add task
  done  Finished task.
  ls    List tasks.
  rm    Remove a task.
```

### Installation

Make sure to have [poetry](https://pypi.org/project/poetry)

#### Github repository
```bash
$ git clone https://github.com/matteyeux/task
$ cd task
$ poetry install
```

#### PyPI
- Installation : `pip3 install task`
- Update : `pip3 install --upgrade task`

### Setup

Make sure to have `~/.local/bin` in your `$PATH` (`export PATH=$PATH:~/.local/bin`)

The first time you run `task add` command it will setup the SQLite3 database.


### Examples



### Credits
Powered by [etnawrapper](https://github.com/tbobm/etnawrapper)
