# CSV normalization
Author: Adam Lussier <adam@adamlussier.com>

## Prerequisites:
* Docker image: `ubuntu:20.04`
* Launch Docker container:
    ```sh
    $ docker run -it ubuntu:20.04
    ```
* install `python3`, `pip`, and `pytz` in Docker container:
    ```sh
    # apt-get update
    # apt-get install -y python3 python3-pip
    # pip install pytz
    ```
## Example usage:
* input file and output file:
    ```sh
    $ ./normalizer.py < sample.csv > output.csv
    ```
* outputting to `stdout`:
    ```sh
    $ ./normalizer.py < sample.csv
    ```
* checking output against test files:
    ```sh
    $ ./test.sh
    ```
