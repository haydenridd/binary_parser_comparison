meta:
  id: data_varying
  file-extension: data_varying
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
  body:
    seq:
      - id: field1
        type: u2
      - id: field2
        type: u1
      - id: field3
        type: u2
      - id: field4
        type: str_with_len
      - id: field5
        type: str_with_len
      - id: field6
        type: f4
  
  record:
    seq:
      - id: record_len
        type: u2
      - id: body
        type: body
        size: record_len
  