## REV32
_ARM A64 Instruction_

**Title**: REV32 -- A64 | **Class**: `general` | **XML ID**: `REV32_int`

**Summary**: Reverse bytes in 32-bit words

**Description**:
This instruction reverses the byte order in each 32-bit
word of a register.

### Variant: `64-bit`
- **Assembly**: `REV32  <Xd>, <Xn>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24  20  15  11   9   4  |
|-----------------------------------|
| 1   1   0   1   101 0110 00000 0000 10  Rn  Rd  |
```

#### Decode (A64.dpreg.dp_1src.REV32_64_dp_1src)

```
if opc == '11' && sf == '0' then EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer datasize = 32 << UInt(sf);
constant integer container_size = 8 << UInt(opc);
```

#### Execute (A64.dpreg.dp_1src.REV32_64_dp_1src)

```
constant bits(datasize) operand = X[n, datasize];
bits(datasize) result;

constant integer containers = datasize DIV container_size;
for c = 0 to containers-1
    constant bits(container_size) container = Elem[operand, c, container_size];
    Elem[result, c, container_size] = Reverse(container, 8);

X[d, datasize] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `opc != '11' \|\| sf != '0'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Xn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose source register, encoded in the "Rn" field. |

### Operational Notes

If PSTATE.DIT is 1:
        
          
            The execution time of this instruction is independent of:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.
                
              
            
          
          
            The response of this instruction to asynchronous exceptions does not vary based on:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.

---
<details><summary>Metadata</summary>

- datatype: `64`
- isa: `A64`
- source: `rev32_int.xml`
</details>