#!/usr/bin/env python3
#
# https://github.com/tellezhector/time_delta
#
# Utility script to print two (recent) timestamps in iso-format that have the given delta.
# The fist timestamp is always the in the past in respect to the second (or be the same).
#
# Usage:
#
# ./time_delta.py delta [shift]
#
# `delta` can be of the formats: 
#         1day,       1day3minutes,       1d3m,      3h,      1h, 3h2m50s or equivalently
#         1:00:00:00,   1:00:03:00, 1:00:03:00, 3:00:00, 1:00:00, 3:02:50
#
# `shift` can be of any of the same kind of formats.
#         `shift` can be preceeded by a minus sign (-).
#
# Note: `delta` can also be negative, in which case the resulting delta will be a time
# addition instead of a substraction, but this doesn't seem very intuitive nor useful.
#
# Examples:
# Assuming the current time is 2024-09-04 02:59:53-07:00
#
# A delta between now and a day ago:
#
# $ ./time_delta.py 1d
# 2024-09-03 02:59:53-07:00 - 2024-09-04 02:59:53-07:00
#
# Shifting 7 seconds into the future:
#
# $ ./time_delta.py 1d 7s
# 2024-09-03 03:00:00-07:00 - 2024-09-04 03:00:00-07:00
#
# Shifting 3 seconds into the past:
#
# $ ./time_delta.py 1d -3s
# 2024-09-03 02:59:50-07:00 - 2024-09-04 02:59:50-07:00
#
# A delta between now and a day from now:
#
# $ ./time_delta.py -1d
# 2024-09-04 02:59:50-07:00 - 2024-09-05 02:59:50-07:00

import datetime
import re
import sys

DELTA_REGEX = re.compile(r'''^
        [-+]?
        ((?P<days>\d+?)(d|day|days))?
        ((?P<hours>\d+?)(h|hr|hour|hrs|hours))?
        ((?P<minutes>\d+?)(m|min|mins|minutes))?
        ((?P<seconds>\d+?)(s|sec|secs|seconds))?
        $''', flags=re.VERBOSE)
CLOCK_TIME_REGEX = re.compile(r'^[-+]?(?P<clock>(\d+:){0,3}\d+)$', flags=re.VERBOSE)

def clock_format_to_delta(time_str: str) -> datetime.timedelta:
    time_str = time_str.strip()
    match = CLOCK_TIME_REGEX.fullmatch(time_str)
    if not match:
        raise ValueError(f'Bad time string {time_str=}')
    sign = -1 if time_str.startswith('-') else 1
    parts = match.group('clock').split(":")
    secs = 0
    while parts:
        match len(parts):
            case 4:
                # days
                secs += 3600*24*int(parts.pop(0))
            case 3:
                # hours
                secs += 3600*int(parts.pop(0))
            case 2:
                # minutes
                secs += 60*int(parts.pop(0))
            case 1:
                # seconds
                secs += int(parts.pop(0))
    return sign * datetime.timedelta(seconds=secs)

def parse_long_delta(time_str: str) -> datetime.timedelta:
    match = DELTA_REGEX.fullmatch(time_str)
    if not match:
        raise ValueError(f'Bad time string {time_str=}')
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
    raise ValueError(f'Bad time string {time_str=}')

def main(args):
    if len(args) < 1:
        raise ValueError('at least one argument is required')
    if len(args) > 2:
        raise ValueError(f'too many arguments {len(args)} {args}; at most 2 are expected')
    
    if len(args) == 1:
      [delta_string], shift_string = args, None
    elif len(args) == 2:
        delta_string, shift_string = args

    delta = parse_any_delta(delta_string)
    now = datetime.datetime.now().astimezone()
    if shift_string:
        shift = parse_any_delta(shift_string)
        now = now + shift
    then = now - delta
    if then > now:
        now, then = then, now
    now_display = now.astimezone().isoformat(sep=' ',timespec='seconds')
    then_display = then.astimezone().isoformat(sep=' ',timespec='seconds')
    print(f'{then_display} - {now_display}')

if __name__ == '__main__':
   args = sys.argv[1:]
   main(args)
