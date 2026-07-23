## SUB
_ARM A64 Instruction_

**Title**: SUB (shifted register) -- A64 | **Class**: `general` | **XML ID**: `SUB_addsub_shift`

**Summary**: Subtract optionally-shifted register

**Description**:
This instruction subtracts an optionally-shifted register value
from a register value, and writes the result to the destination
register.

### Variant: `Not setting the condition flags (SUB_32_addsub_shift)` (32-bit)
- **Condition**: `sf == 0`
- **Assembly**: `SUB  <Wd>, <Wn>, <Wm>{, <shift> #<amount>}`
- **Fixed bits**: `sf`=`0`
- **Bit Pattern**: `???????????????????????????????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  15   9   4  |
|--------------------------------|
| sf  1   0   01011 shift 0   Rm  imm6 Rn  Rd  |
```

#### Decode (A64.dpreg.addsub_shift.SUB_32_addsub_shift)

```
if shift == '11' then EndOfDecode(Decode_UNDEF);
if sf == '0' && imm6<5> == '1' then EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer datasize = 32 << UInt(sf);
constant ShiftType shift_type = DecodeShift(shift);
constant integer shift_amount = UInt(imm6);
```

#### Execute (A64.dpreg.addsub_shift.SUB_32_addsub_shift)

```
constant bits(datasize) operand1 = X[n, datasize];
constant bits(datasize) operand2 = NOT(ShiftReg(m, shift_type, shift_amount, datasize));
bits(datasize) result;

(result, -) = AddWithCarry(operand1, operand2, '1');

X[d, datasize] = result;
```

#### Constraints
_2× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `shift != '11'` |
| 🚫 ENCODING_UNDEF | `sf != '0' \|\| imm6<5> != '1'` |

### Variant: `Not setting the condition flags (SUB_64_addsub_shift)` (64-bit)
- **Condition**: `sf == 1`
- **Assembly**: `SUB  <Xd>, <Xn>, <Xm>{, <shift> #<amount>}`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  15   9   4  |
|--------------------------------|
| sf  1   0   01011 shift 0   Rm  imm6 Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Wn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the first general-purpose source register, encoded in the "Rn" field. |
| `<Wm>` | `register (32-bit)` | `Rm` | Is the 32-bit name of the second general-purpose source register, encoded in the "Rm" field. |
| `<shift>` | `shift` | `shift` | Is the optional shift type to be applied to the second source operand, defaulting to LSL and |
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
| 11 | RESERVED |

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
- isa: `A64`
- source: `sub_addsub_shift.xml`
</details>