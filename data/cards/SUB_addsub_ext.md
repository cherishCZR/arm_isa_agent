## SUB
_ARM A64 Instruction_

**Title**: SUB (extended register) -- A64 | **Class**: `general` | **XML ID**: `SUB_addsub_ext`

**Summary**: Subtract extended and scaled register

**Description**:
This instruction subtracts a sign or zero-extended register
value, followed by an optional left shift amount, from a register value,
and writes the result to the destination register. The argument
that is extended from the <Rm> register can be a byte, halfword,
word, or doubleword.

### Variant: `Not setting the condition flags (SUB_32_addsub_ext)` (32-bit)
- **Condition**: `sf == 0`
- **Assembly**: `SUB  <Wd|WSP>, <Wn|WSP>, <Wm>{, <extend> {#<amount>}}`
- **Fixed bits**: `sf`=`0`
- **Bit Pattern**: `???????????????????????????????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  15  12   9   4  |
|-----------------------------------|
| sf  1   0   01011 00  1   Rm  option imm3 Rn  Rd  |
```

#### Decode (A64.dpreg.addsub_ext.SUB_32_addsub_ext)

```
if imm3 IN {'101', '110', '111'} then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer shift = UInt(imm3);
constant integer datasize = 32 << UInt(sf);
constant ExtendType extend_type = DecodeRegExtend(option);
```

#### Execute (A64.dpreg.addsub_ext.SUB_32_addsub_ext)

```
constant bits(datasize) operand1 = if n == 31 then SP[datasize] else X[n, datasize];
constant bits(datasize) operand2 = NOT(ExtendReg(m, extend_type, shift, datasize));
bits(datasize) result;

(result, -) = AddWithCarry(operand1, operand2, '1');

if d == 31 then
    SP[64] = ZeroExtend(result, 64);
else
    X[d, datasize] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `imm3 IN{'101', '110', '111'}` |

### Variant: `Not setting the condition flags (SUB_64_addsub_ext)` (64-bit)
- **Condition**: `sf == 1`
- **Assembly**: `SUB  <Xd|SP>, <Xn|SP>, <R><m>{, <extend> {#<amount>}}`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  15  12   9   4  |
|-----------------------------------|
| sf  1   0   01011 00  1   Rm  option imm3 Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd\|WSP>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the destination general-purpose register or stack pointer, encoded in the "Rd" field. |
| `<Wn\|WSP>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the first source general-purpose register or stack pointer, encoded in the "Rn" field. |
| `<Wm>` | `register (32-bit)` | `Rm` | Is the 32-bit name of the second general-purpose source register, encoded in the "Rm" field. |
| `<extend>` | `shift` | `option` | For the "32-bit" variant: is the extension to be applied to the second source operand, |
| `<extend>` | `shift` | `option` | For the "64-bit" variant: is the extension to be applied to the second source operand, |
| `<amount>` | `unknown` | `imm3` | Is the left shift amount to be applied after extension in the range 0 to 4, defaulting to 0, encoded in the "imm3" field. It must be absent when <exte |
| `<Xd\|SP>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the destination general-purpose register or stack pointer, encoded in the "Rd" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the first source general-purpose register or stack pointer, encoded in the "Rn" field. |
| `<R>` | `unknown` | `option` | Is a width specifier, |
| `<m>` | `unknown` | `Rm` | Is the number [0-30] of the second general-purpose source register or the name ZR (31), encoded in the "Rm" field. |

**<extend> Value Table**:

| bitfield | symbol |
|---|---|
| 000 | UXTB |
| 001 | UXTH |
| 010 | LSL\|UXTW |
| 011 | UXTX |
| 100 | SXTB |
| 101 | SXTH |
| 110 | SXTW |
| 111 | SXTX |

**<extend> Value Table**:

| bitfield | symbol |
|---|---|
| 000 | UXTB |
| 001 | UXTH |
| 010 | UXTW |
| 011 | LSL\|UXTX |
| 100 | SXTB |
| 101 | SXTH |
| 110 | SXTW |
| 111 | SXTX |

**<R> Value Table**:

| bitfield | symbol |
|---|---|
| 00x | W |
| 010 | W |
| x11 | X |
| 10x | W |
| 110 | W |

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
- source: `sub_addsub_ext.xml`
</details>