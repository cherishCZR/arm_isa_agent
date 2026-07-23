## ORR
_ARM A64 Instruction_

**Title**: ORR (immediate) -- A64 | **Class**: `general` | **XML ID**: `ORR_log_imm`

**Summary**: Bitwise OR (immediate)

**Description**:
This instruction performs a bitwise (inclusive) OR of a
register value and an immediate value, and writes
the result to the destination register.

### Variant: `Not setting the condition flags (ORR_32_log_imm)` (32-bit)
- **Condition**: `sf == 0 && N == 0`
- **Assembly**: `ORR  <Wd|WSP>, <Wn>, #<imm>`
- **Fixed bits**: `sf`=`0`, `N`=`0`
- **Bit Pattern**: `??????????????????????0????????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  22 21  15   9   4  |
|--------------------------|
| sf  01  100100 N   immr imms Rn  Rd  |
```

#### Decode (A64.dpimm.log_imm.ORR_32_log_imm)

```
if sf == '0' && N != '0' then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer datasize = 32 << UInt(sf);
bits(datasize) imm;
(imm, -) = DecodeBitMasks(N, imms, immr, TRUE, datasize);
```

#### Execute (A64.dpimm.log_imm.ORR_32_log_imm)

```
constant bits(datasize) operand1 = X[n, datasize];
constant bits(datasize) operand2 = imm;

constant bits(datasize) result = operand1 OR operand2;

if d == 31 then
    SP[64] = ZeroExtend(result, 64);
else
    X[d, datasize] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `sf != '0' \|\| N == '0'` |

### Variant: `Not setting the condition flags (ORR_64_log_imm)` (64-bit)
- **Condition**: `sf == 1`
- **Assembly**: `ORR  <Xd|SP>, <Xn>, #<imm>`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  22 21  15   9   4  |
|--------------------------|
| sf  01  100100 N   immr imms Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd\|WSP>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the destination general-purpose register or stack pointer, encoded in the "Rd" field. |
| `<Wn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the general-purpose source register, encoded in the "Rn" field. |
| `<imm>` | `immediate` | `immr:imms` | For the "32-bit" variant: is the bitmask immediate, encoded in "imms:immr". |
| `<imm>` | `immediate` | `N:immr:imms` | For the "64-bit" variant: is the bitmask immediate, encoded in "N:imms:immr". |
| `<Xd\|SP>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the destination general-purpose register or stack pointer, encoded in the "Rd" field. |
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

- cond-setting: `no-s`
- immediate-type: `imm12-bitfield`
- isa: `A64`
- source: `orr_log_imm.xml`
</details>