# WPS

## Source Code
```
.
├── README.md
├── run.py                  # when you want to run the program, please use this script 
└── src
    ├── __init__.py
    ├── config.py           # define come configurations
    ├── feature.py          # extract features
    ├── reader.py           # read original data
    └── util.py             # define some functions
```

#### API Usage

Please refer to `run.py`.

## How to run

- Ensure that you terminal is in the right directory, i.e. `src`'s parent directory
- Run the following command

```sh
$ python3 run.py --tr_dir=$train_directory --ts_dir=$test_directory  

# Example
$ python3 run.py --tr_dir=./weps2007_data_1.1/traininig --ts_dir=./WePS2_test_data/data/test
```

For help,
```sh
$ python3 run.py -h
```
