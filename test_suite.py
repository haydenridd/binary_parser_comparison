import os
import time
import mmap
import struct

# CONSTRUCT IMPORTS
from construct import GreedyRange
from construct_format_defs import data_simple_fmt, data_varying_fmt, data_complex_fmt

# KAITAI IMPORTS/PARSERS
from kaitai_export_simple import DataSimple
from kaitai_export_varying import DataVarying
from kaitai_export_complex import DataComplex

## CONSTANTS

# test directory
test_dir = "./test_binary_files"

# file names
data_simple_fn = "data_simple"
data_varying_fn = "data_varying"
data_complex_fn = "data_complex"

# sizes
small_f = "_small.bin"
med_f = "_medium.bin"
big_f = "_large.bin"

## MY PARSERS
def parse_simple(bin_fh):


    # Can also use: Array.array or numpy from file read since this is fixed format

    # precompile struct object
    structobj = struct.Struct("<HBfi")

    # intialize return data (in memory for now)
    data_ls = []

    # Get size in bytes
    bin_fh.seek(0, 2)
    bytes_size = bin_fh.tell()

    # Go back to beginning
    bin_fh.seek(0)

    # iteratively get data
    data_ls.extend(structobj.unpack(bin_fh.read(11)) for _ in range(0, bytes_size, 11))

    # output
    return data_ls

def parse_varying(bin_fh):

    # precompile struct objects for fixed read
    structobj_start = struct.Struct("<HHBHB")
    structobj_len = struct.Struct("<B")
    structobj_end = struct.Struct("<f")

    # intialize return data (in memory for now)
    data_ls = []

    # Get size in bytes
    bin_fh.seek(0, 2)
    bytes_size = bin_fh.tell()

    # Go back to beginning
    bin_fh.seek(0)

    # iteratively get data
    curr_bytes = 0
    while curr_bytes < bytes_size:
        tp_start = structobj_start.unpack(bin_fh.read(8))
        curr_bytes += 8 + tp_start[0]

        # read entire rest of record at once instead of multiple reads
        rest_bytes = bin_fh.read(tp_start[0] - 6)
        str1_len = tp_start[4]
        tp_start = tp_start[0:4] + struct.unpack("<" + str(str1_len) + "s", rest_bytes[0:str1_len])
        str2_len = rest_bytes[str1_len]
        tp_start += struct.unpack("<" + str(str2_len) + "s", rest_bytes[str1_len + 1:str1_len + 1 + str2_len])
        data_ls.append(tp_start + structobj_end.unpack(rest_bytes[str1_len + 1 + str2_len:]))

    # output
    return data_ls

def parse_complex(bin_fh):

    # precompile struct objects for fixed read

    # header section
    structobj_header = struct.Struct("<HB")

    # data section
    structobj_subtable1_chunk1 = struct.Struct("<HBB")
    structobj_subtable1_chunk2 = struct.Struct("<f")
    structobj_subtable3_chunk1 = struct.Struct("<HLLLLLLLB")
    structobj_subtable3_chunk2 = struct.Struct("<ff")

    # intialize return data (in memory for now)
    data_ls = []

    # Get size in bytes
    bin_fh.seek(0, 2)
    bytes_size = bin_fh.tell()

    # Go back to beginning
    bin_fh.seek(0)

    # iteratively get data
    curr_bytes = 0
    while curr_bytes < bytes_size:

        # Header section of table
        data_tuple = structobj_header.unpack(bin_fh.read(3))
        curr_bytes += 3 + data_tuple[0]

        # read entire rest of record at once instead of multiple reads
        rest_bytes = bin_fh.read(data_tuple[0])
        bytes_counter = 0

        # sub table section
        if data_tuple[1] == 1:

            data_tuple += structobj_subtable1_chunk1.unpack(rest_bytes[bytes_counter:bytes_counter+4])
            bytes_counter += 4
            str1_len = data_tuple[4]
            data_tuple = data_tuple[0:4] + struct.unpack("<" + str(str1_len) + "s",
                                                         rest_bytes[bytes_counter:bytes_counter + str1_len])
            bytes_counter += str1_len
            data_tuple += structobj_subtable1_chunk2.unpack(rest_bytes[bytes_counter:bytes_counter+4])

        elif data_tuple[1] == 2:

            str1_len = rest_bytes[0]
            bytes_counter += 1
            data_tuple += struct.unpack("<" + str(str1_len) + "s",
                                                         rest_bytes[bytes_counter:bytes_counter + str1_len])
            bytes_counter += str1_len

            str1_len = rest_bytes[bytes_counter]
            bytes_counter += 1
            data_tuple += struct.unpack("<" + str(str1_len) + "s",
                                        rest_bytes[bytes_counter:bytes_counter + str1_len])
            bytes_counter += str1_len

            str1_len = rest_bytes[bytes_counter]
            bytes_counter += 1
            data_tuple += struct.unpack("<" + str(str1_len) + "s",
                                        rest_bytes[bytes_counter:bytes_counter + str1_len])
            bytes_counter += str1_len

        else:

            data_tuple += structobj_subtable3_chunk1.unpack(rest_bytes[bytes_counter:bytes_counter+31])
            bytes_counter += 31
            str1_len = rest_bytes[30]
            data_tuple = data_tuple[0:31] + struct.unpack("<" + str(str1_len) + "s",
                                        rest_bytes[bytes_counter:bytes_counter + str1_len])
            bytes_counter += str1_len
            data_tuple += structobj_subtable3_chunk2.unpack(rest_bytes[bytes_counter:])

        data_ls.append(data_tuple)

    # output
    return data_ls


def benchmark_parsers():
    ## CONSTRUCT PARSERS

    # construct parsers (for pre-compilation)
    construct_parser_simple = GreedyRange(data_simple_fmt)
    construct_parser_simple.compile()
    construct_parser_varying = GreedyRange(data_varying_fmt)
    construct_parser_varying.compile()
    construct_parser_complex = GreedyRange(data_complex_fmt)
    construct_parser_complex.compile()

    # benchmark how long it takes to parse each file in various parsing types
    for parse_type in ["construct",  "kaitai", "homebrew"]:
        for file_type in [data_simple_fn, data_varying_fn, data_complex_fn]:
            for file_size in [small_f, med_f]:#[small_f, med_f, big_f]:
                with open(os.path.join(test_dir, file_type + file_size), "rb") as f:
                    mem_f = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
                    t0 = time.time()
                    if "simple" in file_type:
                        if parse_type in "construct":
                            data = construct_parser_simple.parse_stream(mem_f)
                        elif parse_type in "kaitai":
                            data = DataSimple.from_io(mem_f)
                        else:
                            data = parse_simple(mem_f)
                    elif "varying" in file_type:
                        if parse_type in "construct":
                            data = construct_parser_varying.parse_stream(mem_f)
                        elif parse_type in "kaitai":
                            data = DataVarying.from_io(mem_f)
                        else:
                            data = parse_varying(mem_f)
                    else:
                        if parse_type in "construct":
                            data = construct_parser_complex.parse_stream(mem_f)
                        elif parse_type in "kaitai":
                            data = DataComplex.from_io(mem_f)
                        else:
                            data = parse_complex(mem_f)
                    t = time.time()
                    print(parse_type + ": " + file_type + file_size + ": " + str(t-t0))


if __name__ == "__main__":
    benchmark_parsers()
