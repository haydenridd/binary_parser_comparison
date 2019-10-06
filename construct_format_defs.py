from construct import *

# Simple tabular binary record with fixed fields
data_simple_fmt = Struct(
    "field1" / Int16ul,
    "field2" / Int8ul,
    "field3" / Float32l,
    "field4" / Int32sl
)

# Simple tabular binary record with 2 varying string fields, a record length header is included
data_varying_fmt = Struct(
    "record_len" / Int16ul,
    "field1" / Int16ul,
    "field2" / Int8ul,
    "field3" / Int16ul,
    "field4" / PascalString(Int8ul, "utf8"),
    "field5" / PascalString(Int8ul, "utf8"),
    "field6" / Float32l
)

# Complex binary record with multiple tabular record types that have varying fields indicated by record header
table1_fmt = Struct(
    "table1_field1" / Int16ul,
    "table1_field2" / Int8ul,
    "table1_field3" / PascalString(Int8ul, "utf8"),
    "table1_field4" / Float32l
)
table2_fmt = Struct(
    "table2_field1" / PascalString(Int8ul, "utf8"),
    "table2_field2" / PascalString(Int8ul, "utf8"),
    "table2_field3" / PascalString(Int8ul, "utf8")
)
table3_fmt = Struct(
    "table3_field1" / Int16ul,
    "table3_field2" / Int32ul,
    "table3_field3" / Int32ul,
    "table3_field4" / Int32ul,
    "table3_field5" / Int32ul,
    "table3_field6" / Int32ul,
    "table3_field7" / Int32ul,
    "table3_field8" / Int32ul,
    "table3_field9" / PascalString(Int8ul, "utf8"),
    "table3_field10" / Float32l,
    "table3_field10" / Float32l
)

data_complex_fmt = Struct(
    "record_len" / Int16ul,
    "record_typ" / Int8ul,
    Switch(this.record_typ,
           {
               1: Embedded(table1_fmt),
               2: Embedded(table2_fmt),
               3: Embedded(table3_fmt)
           })
)