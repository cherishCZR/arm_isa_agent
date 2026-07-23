## MSUB `[ALIAS]`
_ARM A64 Instruction_ (Alias of msub.xml)

**Title**: MNEG -- A64 | **Class**: `general` | **XML ID**: `MNEG_MSUB`

**Summary**: Multiply-negate

**Description**:
This instruction multiplies two register values, negates the product, and
writes the result to the destination register.

### Variant: `Integer (MNEG_MSUB_32A_dp_3src)` (32-bit)
- **Condition**: `sf == 0`
- **Assembly**: `MNEG  <Wd>, <Wn>, <Wm>`
- **Fixed bits**: `sf`=`0`
- **Bit Pattern**: `???????????????????????????????0`
- **Alias of**: `MSUB  <Wd>, <Wn>, <Wm>, WZR`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  23  20  15 14   9   4  |
|-----------------------------|
| sf  00  11011 000 Rm  1   11111 Rn  Rd  |
```

### Variant: `Integer (MNEG_MSUB_64A_dp_3src)` (64-bit)
- **Condition**: `sf == 1`
- **Assembly**: `MNEG  <Xd>, <Xn>, <Xm>`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
- **Alias of**: `MSUB  <Xd>, <Xn>, <Xm>, XZR`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  23  20  15 14   9   4  |
|-----------------------------|
| sf  00  11011 000 Rm  1   11111 Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Wn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the first general-purpose source register holding the multiplicand, encoded in the "Rn" field. |
| `<Wm>` | `register (32-bit)` | `Rm` | Is the 32-bit name of the second general-purpose source register holding the multiplier, encoded in the "Rm" field. |
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Xn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the first general-purpose source register holding the multiplicand, encoded in the "Rn" field. |
| `<Xm>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the second general-purpose source register holding the multiplier, encoded in the "Rm" field. |

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

- alias_mnemonic: `MNEG`
- isa: `A64`
- source: `mneg_msub.xml`
</details>