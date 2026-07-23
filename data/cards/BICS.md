## BICS
_ARM A64 Instruction_

**Title**: BICS (shifted register) -- A64 | **Class**: `general` | **XML ID**: `BICS`

**Summary**: Bitwise bit clear (shifted register), setting flags

**Description**:
This instruction performs a bitwise AND of a register
value and the complement of an optionally-shifted register value, and writes the result
to the destination register. It updates the condition flags based on the result.

### Variant: `Setting the condition flags (BICS_32_log_shift)` (32-bit)
- **Condition**: `sf == 0`
- **Assembly**: `BICS  <Wd>, <Wn>, <Wm>{, <shift> #<amount>}`
- **Fixed bits**: `sf`=`0`
- **Bit Pattern**: `???????????????????????????????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  23  21 20  15   9   4  |
|-----------------------------|
| sf  11  01010 shift 1   Rm  imm6 Rn  Rd  |
```

#### Decode (A64.dpreg.log_shift.BICS_32_log_shift)

```
if sf == '0' && imm6<5> == '1' then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer datasize = 32 << UInt(sf);
constant ShiftType shift_type = DecodeShift(shift);
constant integer shift_amount = UInt(imm6);
```

#### Execute (A64.dpreg.log_shift.BICS_32_log_shift)

```
constant bits(datasize) operand1 = X[n, datasize];
constant bits(datasize) operand2 = ShiftReg(m, shift_type, shift_amount, datasize);

constant bits(datasize) result = operand1 AND NOT(operand2);
X[d, datasize] = result;
PSTATE.<N,Z,C,V> = result<datasize-1>:IsZeroBit(result):'00';
```

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `sf != '0' \|\| imm6<5> != '1'` |

### Variant: `Setting the condition flags (BICS_64_log_shift)` (64-bit)
- **Condition**: `sf == 1`
- **Assembly**: `BICS  <Xd>, <Xn>, <Xm>{, <shift> #<amount>}`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  23  21 20  15   9   4  |
|-----------------------------|
| sf  11  01010 shift 1   Rm  imm6 Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Wn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the first general-purpose source register, encoded in the "Rn" field. |
| `<Wm>` | `register (32-bit)` | `Rm` | Is the 32-bit name of the second general-purpose source register, encoded in the "Rm" field. |
| `<shift>` | `shift` | `shift` | Is the optional shift to be applied to the final source, defaulting to LSL and |
| `<amount>` | `unknown` | `imm6` | For the "32-bit" variant: is the shift amount, in the range 0 to 31, defaulting to 0 and encoded in the "imm6" field. |
| `<amount>` | `unknown` | `imm6` | For the "64-bit" variant: is the shift amount, in the range 0 to 63, defaulting to 0 and encoded in the "imm6" field. |
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Xn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the first general-purpose source register, encoded in the "Rn" field. |
| `<Xm>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the second general-purpose source register, encoded in the "Rm" field. |

**<shift> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | LSL |
| 01 | LSR |
| 10 | ASR |
| 11 | ROR |

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

- cond-setting: `S`
- isa: `A64`
- reguse: `shifted-reg`
- source: `bics.xml`
</details>