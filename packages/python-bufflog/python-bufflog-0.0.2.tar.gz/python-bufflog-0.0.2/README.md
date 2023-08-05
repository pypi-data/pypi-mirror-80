# Python Bufflog

Python logger for Buffer services.

## Installation

You can use `pip` to install `bufflog`:

```python
pip install bufflog
```

## Usage

```python

from bufflog import bufflog

bufflog.debug('Hello debug', context={"some":"stuff"});
bufflog.info('Hello info');
bufflog.error('Hello error');
bufflog.critical('Hello critical');
```

## Log verbosity levels

If you wish to see more logs, simply set the `LOG_LEVEL` to the desired level. Here a list with some use case:

|  Levels  | Use case                                                                                                                               | Examples                                                                                                          |
| :------: | -------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
|  DEBUG   | Information used for interactive investigation, with no long-term value. Activate it with `LOG_LEVEL=DEBUG`                            | Printing function names, steps inside a function.                                                                 |
|   INFO   | Interesting events. Track the general flow of the application.  Activate it with `LOG_LEVEL=INFO`                                      | User logs in, SQL logs, worker process/delete a message...                                                        |
|  NOTICE  | Uncommon events. **This is the default verbosity level**.                                                                              | Missing environment variables, page redirection, pod starting/restarting/terminating, retrying to query an API... |
| WARNING  | Exceptional occurrences that are not errors. Undesirable things that are not necessarily wrong.                                        | Use of deprecated APIs,  poor use of an API, unauthorized access, pod restart because of memory limit ...         |
|  ERROR   | Runtime errors. Highlight when the current flow of execution is stopped due to a failure.                                              | Exceptions messages, incorect credentials or permissions...                                                       |
| CRITICAL | Critical conditions. Describe an unrecoverable application, system crash, or a catastrophic failure that requires immediate attention. | Application component unavailable, unexpected exception. entire website down, database unavailable ...            |

## Development

For local development, create a new virtual environment and activate it. That can be done with Python `venv` module.

```bash
$ python -m venv venv
$ source venv/bin/activate
```

Once the virtual environment is activated, install `python-bufflog` locally:

```bash
$ pip install -e .
```
