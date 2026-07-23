## SUBS
_ARM A64 Instruction_

**Title**: SUBS (immediate) -- A64 | **Class**: `general` | **XML ID**: `SUBS_addsub_imm`

**Summary**: Subtract immediate value, setting flags

**Description**:
This instruction subtracts an optionally-shifted immediate value
from a register value, and writes the result to the destination
register. It updates the condition flags based on the result.

### Variant: `Setting the condition flags (SUBS_32S_addsub_imm)` (32-bit)
- **Condition**: `sf == 0`
- **Assembly**: `SUBS  <Wd>, <Wn|WSP>, #<imm>{, <shift>}`
- **Fixed bits**: `sf`=`0`
- **Bit Pattern**: `???????????????????????????????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  22 21   9   4  |
|--------------------------|
| sf  1   1   100010 sh  imm12 Rn  Rd  |
```

#### Decode (A64.dpimm.addsub_imm.SUBS_32S_addsub_imm)

```
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer datasize = 32 << UInt(sf);

constant bits(24) imm = if sh == '0' then Zeros(12):imm12 else imm12:Zeros(12);
```

#### Execute (A64.dpimm.addsub_imm.SUBS_32S_addsub_imm)

```
constant bits(datasize) operand1 = if n == 31 then SP[datasize] else X[n, datasize];
constant bits(datasize) operand2 = ZeroExtend(imm, datasize);
bits(datasize) result;
bits(4) nzcv;

(result, nzcv) = AddWithCarry(operand1, NOT(operand2), '1');

X[d, datasize] = result;
PSTATE.<N,Z,C,V> = nzcv;
```

### Variant: `Setting the condition flags (SUBS_64S_addsub_imm)` (64-bit)
- **Condition**: `sf == 1`
- **Assembly**: `SUBS  <Xd>, <Xn|SP>, #<imm>{, <shift>}`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  22 21   9   4  |
|--------------------------|
| sf  1   1   100010 sh  imm12 Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Wn\|WSP>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the source general-purpose register or stack pointer, encoded in the "Rn" field. |
| `<imm>` | `immediate` | `imm12` | Is an unsigned immediate, in the range 0 to 4095, encoded in the "imm12" field. |
| `<shift>` | `shift` | `sh` | Is the optional left shift to apply to the immediate, defaulting to LSL #0 and |
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the source general-purpose register or stack pointer, encoded in the "Rn" field. |

**<shift> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | LSL #0 |
| 1 | LSL #12 |

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
- immediate-type: `imm12u`
- isa: `A64`
- source: `subs_addsub_imm.xml`
</details>