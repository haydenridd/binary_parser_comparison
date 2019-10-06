meta:
  id: data_complex
  file-extension: data_complex
  endian: le

seq:
  - id: record
    type: record
    repeat: eos
  
types:
  str_with_len:
    seq:
      - id: len
        type: u1
      - id: value
        type: str
        encoding: UTF-8
        size: len
  sub_table1:
    seq:
      - id: table1_field1
        type: u2
      - id: table1_field2
        type: u1
      - id: table1_field3
        type: str_with_len
      - id: table1_field4
        type: f4
  sub_table2:
    seq:
      - id: table2_field1
        type: str_with_len
      - id: table2_field2
        type: str_with_len
      - id: table2_field3
        type: str_with_len
  sub_table3:
    seq:
      - id: table3_field1
        type: u2
      - id: table3_field2
        type: u4
      - id: table3_field3
        type: u4
      - id: table3_field4
        type: u4
      - id: table3_field5
        type: u4
      - id: table3_field6
        type: u4
      - id: table3_field7
        type: u4
      - id: table3_field8
        type: u4
      - id: table3_field9
        type: str_with_len
      - id: table3_field10
        type: f4
      - id: table3_field11
        type: f4
  record:
    seq:
      - id: record_len
        type: u2
      - id: record_typ
        type: u1
        enum: sub_tables
      - id: body
        size: record_len
        type:
          switch-on: record_typ
          cases:
            sub_tables::sub_table1: sub_table1
            sub_tables::sub_table2: sub_table2
            sub_tables::sub_table3: sub_table3
            
enums:
  sub_tables:
    1: sub_table1
    2: sub_table2
    3: sub_table3