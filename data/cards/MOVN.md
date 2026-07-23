## MOVN
_ARM A64 Instruction_

**Title**: MOVN -- A64 | **Class**: `general` | **XML ID**: `MOVN`

**Summary**: Move wide with NOT

**Description**:
This instruction moves the inverse of an optionally-shifted 16-bit immediate
value to a register.

### Variant: `Immediate packed into 16-bit value and 2-bit shift (MOVN_32_movewide)` (32-bit)
- **Condition**: `sf == 0 && hw == 0x`
- **Assembly**: `MOVN  <Wd>, #<imm>{, LSL #<shift>}`
- **Fixed bits**: `sf`=`0`, `hw`=`0`
- **Bit Pattern**: `??????????????????????0????????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  22  20   4  |
|--------------------|
| sf  00  100101 hw  imm16 Rd  |
```

#### Decode (A64.dpimm.movewide.MOVN_32_movewide)

```
if sf == '0' && hw<1> == '1' then EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer datasize = 32 << UInt(sf);
constant bits(16) imm = imm16;
constant integer pos = UInt(hw) << 4;
```

#### Execute (A64.dpimm.movewide.MOVN_32_movewide)

```
bits(datasize) result = Zeros(datasize);
result<pos+15:pos> = imm;
X[d, datasize] = NOT(result);
```

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `sf != '0' \|\| hw<1> != '1'` |

### Variant: `Immediate packed into 16-bit value and 2-bit shift (MOVN_64_movewide)` (64-bit)
- **Condition**: `sf == 1`
- **Assembly**: `MOVN  <Xd>, #<imm>{, LSL #<shift>}`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  22  20   4  |
|--------------------|
| sf  00  100101 hw  imm16 Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<imm>` | `immediate` | `imm16` | Is the 16-bit unsigned immediate, in the range 0 to 65535, encoded in the "imm16" field. |
| `<shift>` | `shift` | `hw` | For the "32-bit" variant: is the amount by which to shift the immediate left, either 0 (the default) or 16, encoded in the "hw" field as <shift>/16. |
| `<shift>` | `shift` | `hw` | For the "64-bit" variant: is the amount by which to shift the immediate left, either 0 (the default), 16, 32 or 48, encoded in the "hw" field as <shif |
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |

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

- immediate-type: `imm18-packed`
- isa: `A64`
- source: `movn.xml`
</details>