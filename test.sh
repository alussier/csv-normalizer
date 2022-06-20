#!/bin/bash

diff --report-identical-files --unified <(python3 normalizer.py < sample.csv) sample_normalized.csv
diff --report-identical-files --unified <(python3 normalizer.py < sample-with-broken-utf8.csv) sample-with-broken-utf8_normalized.csv
