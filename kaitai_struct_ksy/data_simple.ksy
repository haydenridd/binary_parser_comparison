meta:
  id: data_simple
  file-extension: data_simple
  endian: le

seq:
  - id: record
    type: record
    repeat: eos

types:
  record:
    seq:
      - id: field1
        type: u2
      - id: field2
        type: u1
      - id: field3
        type: f4
      - id: field4
        type: s4
      
      
