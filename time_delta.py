#!/usr/bin/env python3
"""Utility script to print two (recent) timestamps with the given delta.

Timestamps are printed in ISO format.

Usage:  `./time_delta.py [-h] [-n] [-v] delta [shift]`
Output: `<before> - <after>  [# delta]`

Source: https://github.com/tellezhector/time_delta
"""

_ARGS="""\
The fist timestamp is always the in the past in respect to the second (or be 
the same).

 delta  can be of the formats: 
        1day,       1day3minutes,       1d3m,      3h,      1h, 3h2m50s 
        (or equivalently)
        1:00:00:00,   1:00:03:00, 1:00:03:00, 3:00:00, 1:00:00, 3:02:50

 shift  optional. Can be of any of the same kind of formats as `delta`. 
        If undefined, <after> will be 'now'; if defined, the dates will be 
        shifted by the time specified, `shift` can be preceeded by a
        minus (-) or plus (+) sign, a minus sign shifts "to the past", a plus
        sign shifts "to the future", plus sign is the same as no sign.

    -n  do not print a new line at the end.

    -v  print the original delta after the timestamps in format:
        <before> - <after>  #  delta
        this is verifying the delta length easier visually.

    -h  prints help, -hh and -hhh will print more details increasingly.

Note: `delta` can also be negative, in which case the resulting delta will be 
a time addition instead of a substraction, but this doesn't seem very 
intuitive nor useful.
"""

_EXAMPLES="""\
Examples:

Assuming the current time is 2024-09-04 02:59:53-07:00

A delta between now and a day ago:

$ ./time_delta.py 1d
2024-09-03 02:59:53-07:00 - 2024-09-04 02:59:53-07:00

Shifting 7 seconds into the future:

$ ./time_delta.py 1d 7s
2024-09-03 03:00:00-07:00 - 2024-09-04 03:00:00-07:00

Shifting 3 seconds into the past:

$ ./time_delta.py 1d -3s
2024-09-03 02:59:50-07:00 - 2024-09-04 02:59:50-07:00

The same but including the delta:

$ ./time_delta.py -v 1d -3s
2024-09-03 02:59:50-07:00 - 2024-09-04 02:59:50-07:00  # 1d

A delta between now and a day from now:

$ ./time_delta.py -1d
2024-09-04 02:59:50-07:00 - 2024-09-05 02:59:50-07:00
"""

import argparse
import datetime
import re
import textwrap
import sys

DELTA_REGEX = re.compile(
    r'''^
        [-+]?
        ((?P<days>\d+?)(d|day|days))?
        ((?P<hours>\d+?)(h|hr|hour|hrs|hours))?
        ((?P<minutes>\d+?)(m|min|mins|minutes))?
        ((?P<seconds>\d+?)(s|sec|secs|seconds))?
        $''',
    flags=re.VERBOSE,
)
CLOCK_TIME_REGEX = re.compile(r'^[-+]?(?P<clock>(\d+:){0,3}\d+)$', flags=re.VERBOSE)


class TimeDeltaError(Exception):
    def __init__(self, message: str, *args: object) -> None:
        super().__init__(*[message, args])
        self.message = message


def clock_format_to_delta(time_str: str) -> datetime.timedelta:
    time_str = time_str.strip()
    match = CLOCK_TIME_REGEX.fullmatch(time_str)
    if not match:
        raise TimeDeltaError(f"bad time '{time_str}'")
    sign = -1 if time_str.startswith('-') else 1
    parts = match.group('clock').split(":")
    secs = 0
    while parts:
        match len(parts):
            case 4:
                # days
                secs += 3600 * 24 * int(parts.pop(0))
            case 3:
                # hours
                secs += 3600 * int(parts.pop(0))
            case 2:
                # minutes
                secs += 60 * int(parts.pop(0))
            case 1:
                # seconds
                secs += int(parts.pop(0))
    return sign * datetime.timedelta(seconds=secs)


def parse_long_delta(time_str: str) -> datetime.timedelta:
    match = DELTA_REGEX.fullmatch(time_str)
    if not match:
        raise TimeDeltaError(f"bad time '{time_str}'")
    sign = -1 if time_str.startswith('-') else 1
    parts = match.groupdict()
    time_params = {k: int(v) for k, v in parts.items() if v}
    delta = datetime.timedelta(**time_params)
    return sign * delta


def parse_any_delta(time_str: str) -> datetime.timedelta:
    if DELTA_REGEX.fullmatch(time_str):
        return parse_long_delta(time_str)
    if CLOCK_TIME_REGEX.fullmatch(time_str):
        return clock_format_to_delta(time_str)
    raise TimeDeltaError(f"bad time '{time_str}'")


def main(args: list[str], print_end: str, print_delta: bool):
    try:
        if len(args) < 1:
            raise TimeDeltaError('too few arguments')
        if len(args) > 2:
            raise TimeDeltaError(f'too many arguments')
        
        if len(args) == 1:
            [delta_string], shift_string = args, None
        elif len(args) == 2:
            delta_string, shift_string = args

        delta = parse_any_delta(delta_string)
        now = datetime.datetime.now().astimezone()
        shift = datetime.timedelta(seconds=0)
        if shift_string:
            shift = parse_any_delta(shift_string)
        now = now + shift
        then = now - delta
        if then > now:
            now, then = then, now
        now_display = now.astimezone().isoformat(sep=' ', timespec='seconds')
        then_display = then.astimezone().isoformat(sep=' ', timespec='seconds')
        res = f'{then_display} - {now_display}'
        if print_delta:
            res = f'{res}  # {delta_string}'
        print(res, end=print_end)
    except TimeDeltaError as e:
        print(f'[{e.message}] args: {args}', file=sys.stderr, end=print_end)
        exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('time_delta.py', add_help=False)
    parser.add_argument('-n', dest='no_new_line', action='store_true')
    parser.add_argument('-h', dest='help', action='count', default=0)
    parser.add_argument('-v', dest='print_delta', action='store_true')


    known_args, args = parser.parse_known_args()

    if known_args.help:
        if known_args.help >= 1:
            print(textwrap.dedent(__doc__), file=sys.stderr)
        if known_args.help >= 2:
            print(textwrap.dedent(_ARGS), file=sys.stderr)
        if known_args.help >= 3:
            print(textwrap.dedent(_EXAMPLES), file=sys.stderr)
        exit(0)

    print_end='' if known_args.no_new_line else None
    main(args, print_end=print_end, print_delta=known_args.print_delta)
