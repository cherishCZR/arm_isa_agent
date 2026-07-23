## EXTR
_ARM A64 Instruction_

**Title**: EXTR -- A64 | **Class**: `general` | **XML ID**: `EXTR`

**Summary**: Extract register

**Description**:
This instruction extracts a register from a pair of registers.

### Variant: `Integer (EXTR_32_extract)` (32-bit)
- **Condition**: `sf == 0 && N == 0 && imms == 0xxxxx`
- **Assembly**: `EXTR  <Wd>, <Wn>, <Wm>, #<lsb>`
- **Fixed bits**: `sf`=`0`, `N`=`0`, `imms`=`0`
- **Bit Pattern**: `???????????????0??????0????????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  22 21 20  15   9   4  |
|-----------------------------|
| sf  00  100111 N   0   Rm  imms Rn  Rd  |
```

#### Decode (A64.dpimm.extract.EXTR_32_extract)

```
if N != sf then EndOfDecode(Decode_UNDEF);
if sf == '0' && imms<5> == '1' then EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer datasize = 32 << UInt(sf);
constant integer lsb = UInt(imms);
```

#### Execute (A64.dpimm.extract.EXTR_32_extract)

```
bits(datasize) result;
constant bits(datasize) operand1 = X[n, datasize];
constant bits(datasize) operand2 = X[m, datasize];
constant bits(2*datasize) concat = operand1:operand2;

result = concat<(lsb+datasize)-1:lsb>;

X[d, datasize] = result;
```

#### Constraints
_2× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `N == sf` |
| 🚫 ENCODING_UNDEF | `sf != '0' \|\| imms<5> != '1'` |

### Variant: `Integer (EXTR_64_extract)` (64-bit)
- **Condition**: `sf == 1 && N == 1`
- **Assembly**: `EXTR  <Xd>, <Xn>, <Xm>, #<lsb>`
- **Fixed bits**: `sf`=`1`, `N`=`1`
- **Bit Pattern**: `??????????????????????1????????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  22 21 20  15   9   4  |
|-----------------------------|
| sf  00  100111 N   0   Rm  imms Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Wn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the first general-purpose source register, encoded in the "Rn" field. |
| `<Wm>` | `register (32-bit)` | `Rm` | Is the 32-bit name of the second general-purpose source register, encoded in the "Rm" field. |
| `<lsb>` | `unknown` | `imms` | For the "32-bit" variant: is the least significant bit position from which to extract, in the range 0 to 31, encoded in the "imms" field. |
| `<lsb>` | `unknown` | `imms` | For the "64-bit" variant: is the least significant bit position from which to extract, in the range 0 to 63, encoded in the "imms" field. |
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Xn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the first general-purpose source register, encoded in the "Rn" field. |
| `<Xm>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the second general-purpose source register, encoded in the "Rm" field. |

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
- source: `extr.xml`
</details>