# time_delta.py

Utility script to print two (recent) timestamps with the given delta.

Timestamps are printed in ISO format.

Source: https://github.com/tellezhector/time_delta

## Usage:

```txt
Usage:  ./time_delta.py [-h] [-n] [-v] delta [shift]
Output: <before> - <after>  [# delta]

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

    -h  prints help, -hh, -hhh and -hhhh will print more details increasingly.

Note: `delta` can also be negative, in which case the resulting delta will be 
a time addition instead of a substraction, but this doesn't seem very 
intuitive nor useful.
```


## Examples

Assuming the current time is 2024-09-04 02:59:53-07:00

A delta between now and a day ago:

```shell
$ ./time_delta.py 1d
2024-09-03 02:59:53-07:00 - 2024-09-04 02:59:53-07:00
```

Shifting 7 seconds into the future:

```shell
$ ./time_delta.py 1d 7s
2024-09-03 03:00:00-07:00 - 2024-09-04 03:00:00-07:00
```

Shifting 3 seconds into the past:

```shell
$ ./time_delta.py 1d -3s
2024-09-03 02:59:50-07:00 - 2024-09-04 02:59:50-07:00
```

The same but including the delta:

```shell
$ ./time_delta.py -v 1d -3s
2024-09-03 02:59:50-07:00 - 2024-09-04 02:59:50-07:00  # 1d
```

A delta between now and a day from now:

```shell
$ ./time_delta.py -1d
2024-09-04 02:59:50-07:00 - 2024-09-05 02:59:50-07:00
```
