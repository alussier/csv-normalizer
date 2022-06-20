#!/usr/bin/env python3

"""
normalizer.py - CSV normalizer

example usage:
$ ./normalizer.py < sample.csv > output.csv

Adam Lussier - adam@adamlussier.com - 2022-06-19
"""

import csv
import datetime
import math
import pytz
import sys

# expected header: "Timestamp,Address,ZIP,FullName,FooDuration,BarDuration,TotalDuration,Notes"
EXPECTED_COLS = 8

def error(*args, **kwargs):
    """ print to stderr """
    print(*args, file=sys.stderr, **kwargs)

def main():
    """ main function for CSV normalization """
    eastern_tz = pytz.timezone('US/Eastern')
    pacific_tz = pytz.timezone('US/Pacific')
    # replace invalid characters with Unicode Replacement Character, and "\r\n" with "\n"
    sys.stdin.reconfigure(encoding='utf-8', errors='replace', newline=None)
    # quote fields with "" when they contain the delimiter ","
    reader = csv.DictReader(sys.stdin, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL)
    writer = csv.writer(sys.stdout)
    writer.writerow(reader.fieldnames)
    # line 1 is header, data starts at line #2
    for linenum,row_string in enumerate(reader, start=2):
        output_row = []
        if len(row_string) != EXPECTED_COLS:
            error(f"line {linenum} skipped: wrong number of columns: {len(row_string)} != {EXPECTED_COLS}")
            continue

        # The sample data we provide contains all date and time format variants you will need to handle.
        try:
            date_object = datetime.datetime.strptime(row_string['Timestamp'], "%m/%d/%y %I:%M:%S %p")
        except ValueError:
            error(f'line {linenum} skipped: could not parse date field "{row_string["Timestamp"]}"')
            continue

        # The Timestamp column should be assumed to be in US/Pacific time; please convert it to US/Eastern.
        date_object = pacific_tz.normalize(pacific_tz.localize(date_object)).astimezone(eastern_tz)
        # The Timestamp column should be formatted in RFC3339 format.
        output_row.append(date_object.isoformat())

        # The Address column should be passed through as is, except for Unicode validation. Please note there are commas in the Address field; your CSV parsing will need to take that into account. Commas will only be present inside a quoted string.
        output_row.append(row_string['Address'])

        # All ZIP codes should be formatted as 5 digits. If there are less than 5 digits, assume 0 as the prefix.
        number = int(row_string['ZIP'])
        output_row.append(f"{number:05d}")

        # The FullName column should be converted to uppercase. There will be non-English names.
        output_row.append(row_string['FullName'].upper())

        # The FooDuration and BarDuration columns are in HH:MM:SS.MS format (where MS is milliseconds); please convert them to the total number of seconds.
        foo_string = row_string['FooDuration'].split(':')
        foo_delta = datetime.timedelta(hours=int(foo_string[0]), minutes=int(foo_string[1]), seconds=float(foo_string[2]))
        # round up to integer seconds
        foo_seconds = math.ceil(foo_delta.total_seconds())
        output_row.append(foo_seconds)
        bar_string = row_string['BarDuration'].split(':')
        bar_delta = datetime.timedelta(hours=int(bar_string[0]), minutes=int(bar_string[1]), seconds=float(bar_string[2]))
        # round up to integer seconds
        bar_seconds = math.ceil(bar_delta.total_seconds())
        output_row.append(bar_seconds)

        # The TotalDuration column is filled with garbage data. For each row, please replace the value of TotalDuration with the sum of FooDuration and BarDuration.
        output_row.append(foo_seconds + bar_seconds)

        # The Notes column is free form text input by end-users; please do not perform any transformations on this column. If there are invalid UTF-8 characters, please replace them with the Unicode Replacement Character.
        output_row.append(row_string['Notes'])

        # emit a normalized CSV formatted file on stdout
        writer.writerow(output_row)

if __name__ == "__main__":
    """ execution from CLI starts here """
    main()
