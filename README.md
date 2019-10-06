# Python Binary Parsing Tester

This repository contains a series of simple scripts for testing three different methods of parsing binary files in
Python. The goal of this project was to compare speeds of two libraries for parsing binary files (Kaitai and Construct)
as well as a pure Python method.


### Prerequisites

This project was deveeloped in Python 3.6.9. Please refer to requirements.txt for package information.


## Usage

###Generating Test Data
After cloning the repository, you should run the script [test_data_generator.py](test_data_generator.py) in order to
create binary files for parsing testing. Modify the following lines to change file sizes:

    # desired file sizes
    file_size_small = 100*1024 # 100 kib
    file_size_medium = 100*1024**2 # 100 mib
    file_size_big = 1024**3 # 1 gib

### Testing Parsing
To test parsing, run the script [test_suite.py](test_suite.py). Currently the largest file size is skipped, this can
be modified in the followign lines of code my modifying the list after "for file_size in":

    # benchmark how long it takes to parse each file in various parsing types
        for parse_type in ["construct",  "kaitai", "homebrew"]:
            for file_type in [data_simple_fn, data_varying_fn, data_complex_fn]:
                for file_size in [small_f, med_f]: #[small_f, med_f, big_f]:

### Modifying Structure
If desired, the structure of generated files can be easily modified by changing the format definitions in 
[construct_format_defs.py](construct_format_defs.py). Note that parsers will have to be updated accordingly. Please
refer to [Kaitai documentation](https://kaitai.io/) as well as 
[Construct documentation](https://construct.readthedocs.io/en/latest/) for more information on that.

## Authors

* **Hayden Riddiford** - [haydenridd](https://github.com/haydenridd)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
