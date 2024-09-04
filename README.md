# time_delta.py

Self link: https://github.com/tellezhector/time_delta

Utility script to print two (recent) timestamps in iso-format that have the given delta.
The fist timestamp is always the in the past in respect to the second (or be the same).

## Usage:

```txt
./time_delta.py delta [shift]

`delta` can be of the formats:
        1:00:00:00, 1:00:03:00,   1:00:03:00, 3:00:00, 1:00:00, 3:02:50 or equivalently
        1day,       1day3minutes, 1d3m,       3h,      1h,      3h2m50s 

`shift` can be of any of the same kind of formats.
        `shift` can be preceeded by a minus sign (-).

   `-n` do not print a new line at the end.

Note: `delta` can also be negative, in which case the resulting delta will be a time
addition instead of a substraction, but this doesn't seem very intuitive nor useful.
```


## Examples:

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

A delta between now and a day from now:

```shell
$ ./time_delta.py -1d
2024-09-04 02:59:50-07:00 - 2024-09-05 02:59:50-07:00
```