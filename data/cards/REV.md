## REV
_ARM A64 Instruction_

**Title**: REV -- A64 | **Class**: `general` | **XML ID**: `REV`

**Summary**: Reverse bytes

**Description**:
This instruction reverses the byte order in a register.

### Variant: `Integer (REV_32_dp_1src)` (32-bit)
- **Condition**: `sf == 0 && opc == 10`
- **Assembly**: `REV  <Wd>, <Wn>`
- **Fixed bits**: `sf`=`0`, `opc`=`0`
- **Bit Pattern**: `??????????0????????????????????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15  11   9   4  |
|-----------------------------|
| sf  1   0   11010110 00000 0000 1x  Rn  Rd  |
```

#### Decode (A64.dpreg.dp_1src.REV_32_dp_1src)

```
if opc == '11' && sf == '0' then EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer datasize = 32 << UInt(sf);
constant integer container_size = 8 << UInt(opc);
```

#### Execute (A64.dpreg.dp_1src.REV_32_dp_1src)

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

### Variant: `Integer (REV_64_dp_1src)` (64-bit)
- **Condition**: `sf == 1 && opc == 11`
- **Assembly**: `REV  <Xd>, <Xn>`
- **Fixed bits**: `sf`=`1`, `opc`=`1`
- **Bit Pattern**: `??????????1????????????????????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15  11   9   4  |
|-----------------------------|
| sf  1   0   11010110 00000 0000 1x  Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Wn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the general-purpose source register, encoded in the "Rn" field. |
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

- isa: `A64`
- source: `rev.xml`
</details>