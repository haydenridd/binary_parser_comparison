import os
import random
import string

from construct_format_defs import data_simple_fmt, data_varying_fmt, data_complex_fmt

# generation switches
gen_simple = False
gen_varying = True
gen_complex = False

# output directory
output_dir = "./test_binary_files"

# create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# file names
data_simple_fn = "data_simple"
data_varying_fn = "data_varying"
data_complex_fn = "data_complex"

# desired file sizes
file_size_small = 100*1024 # 100 kib
file_size_medium = 100*1024**2 # 100 mib
file_size_big = 1024**3 # 1 gib

for fname in [data_simple_fn, data_varying_fn, data_complex_fn]:

    if (fname in data_simple_fn and gen_simple) or (fname in data_varying_fn and gen_varying) or \
            (fname in data_complex_fn and gen_complex):

        # build each file type
        with open(os.path.join(output_dir, fname + "_small.bin"), "wb") as f_small, \
             open(os.path.join(output_dir, fname + "_medium.bin"), "wb") as f_medium, \
             open(os.path.join(output_dir, fname + "_large.bin"), "wb") as f_large:

            # initialize file size in bytes
            file_size = 0
            while file_size < file_size_big:

                # Create randomized dictionary
                if fname in data_simple_fn:
                    d_write = {
                        "field1": random.randint(0, 2**16-1),
                        "field2": random.randint(0, 2**8-1),
                        "field3": random.randint(0, 25 * 10000) / 10000,
                        "field4": random.randint(-(2**31), 2**31-1)
                    }
                    # write byte stream to files
                    bytes_data = data_simple_fmt.build(d_write)

                elif fname in data_varying_fn:
                    d_write = {
                        "field1": random.randint(0, 2**16-1),
                        "field2": random.randint(0, 2**8-1),
                        "field3": random.randint(0, 2**16-1),
                        "field4": ''.join(str(chr(random.choice(range(0, 128)))) for x in range(random.randint(1, 20))),
                        "field5": ''.join(random.choice(string.ascii_letters) for x in range(random.randint(1, 20))),
                        "field6":  random.randint(-(2**31), 2**31-1)
                    }
                    # calculate what record length is with varying fields
                    d_write["record_len"] = 9 + len(d_write["field4"]) + len(d_write["field5"]) + 2
                    # write byte stream to files
                    bytes_data = data_varying_fmt.build(d_write)

                else:
                    d_write = {
                        "record_typ": random.randint(1, 3)
                    }
                    d_sub_write = {}
                    if d_write["record_typ"] == 1:
                        d_sub_write["table1_field1"] = random.randint(0, 2**16-1)
                        d_sub_write["table1_field2"] = random.randint(0, 2**8-1)
                        d_sub_write["table1_field3"] = ''.join(
                            str(chr(random.choice(range(0, 128)))) for x in range(random.randint(1, 20)))
                        d_sub_write["table1_field4"] = random.randint(-(2**31), 2**31-1)
                        d_write["record_len"] = len(d_sub_write["table1_field3"]) + 7 + 1

                    elif d_write["record_typ"] == 2:
                        d_sub_write["table2_field1"] = ''.join(
                            random.choice(string.ascii_letters) for x in range(random.randint(1, 20)))
                        d_sub_write["table2_field2"] = ''.join(
                            str(chr(random.choice(range(0, 128)))) for x in range(random.randint(1, 20)))
                        d_sub_write["table2_field3"] = ''.join(
                            str(chr(random.choice(range(0, 128)))) for x in range(random.randint(1, 20)))
                        d_write["record_len"] = len(d_sub_write["table2_field1"]) + len(d_sub_write["table2_field2"]) + len(
                            d_sub_write["table2_field3"]) + 3

                    else:
                        d_sub_write["table3_field1"] = random.randint(0, 2**16-1)
                        d_sub_write["table3_field2"] = random.randint(0, 2**32-1)
                        d_sub_write["table3_field3"] = random.randint(0, 2**32-1)
                        d_sub_write["table3_field4"] = random.randint(0, 2**32-1)
                        d_sub_write["table3_field5"] = random.randint(0, 2**32-1)
                        d_sub_write["table3_field6"] = random.randint(0, 2**32-1)
                        d_sub_write["table3_field7"] = random.randint(0, 2**32-1)
                        d_sub_write["table3_field8"] = random.randint(0, 2**32-1)
                        d_sub_write["table3_field9"] = ''.join(
                            random.choice(string.ascii_letters) for x in range(random.randint(1, 20)))
                        d_sub_write["table3_field10"] = random.randint(-(2**31), 2**31-1)
                        d_sub_write["table3_field11"] = random.randint(-(2**31), 2**31-1)
                        d_write["record_len"] = 38 + len(d_sub_write["table3_field9"]) + 1

                    d_write["sub_table"] = d_sub_write
                    # write byte stream to files
                    bytes_data = data_complex_fmt.build(d_write)

                # gate writing if we have surpassed desired file size
                if file_size < file_size_small:
                    f_small.write(bytes_data)
                if file_size < file_size_medium:
                    f_medium.write(bytes_data)
                f_large.write(bytes_data)

                # add bytes data to determine file size
                file_size += len(bytes_data)
