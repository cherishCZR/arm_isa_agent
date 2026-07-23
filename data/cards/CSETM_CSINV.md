## CSINV `[ALIAS]`
_ARM A64 Instruction_ (Alias of csinv.xml)

**Title**: CSETM -- A64 | **Class**: `general` | **XML ID**: `CSETM_CSINV`

**Summary**: Conditional set mask

**Description**:
This instruction sets all bits of the destination register
to 1 if the condition is TRUE, and otherwise sets all bits to 0.

### Variant: `Integer (CSETM_CSINV_32_condsel)` (32-bit)
- **Condition**: `sf == 0`
- **Assembly**: `CSETM  <Wd>, <invcond>`
- **Fixed bits**: `sf`=`0`
- **Bit Pattern**: `???????????????????????????????0`
- **Alias of**: `CSINV  <Wd>, WZR, WZR, <cond>`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15  11 10  9   4  |
|--------------------------------|
| sf  1   0   11010100 11111 ?   0   0   11111 Rd  |
```

### Variant: `Integer (CSETM_CSINV_64_condsel)` (64-bit)
- **Condition**: `sf == 1`
- **Assembly**: `CSETM  <Xd>, <invcond>`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
- **Alias of**: `CSINV  <Xd>, XZR, XZR, <cond>`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15  11 10  9   4  |
|--------------------------------|
| sf  1   0   11010100 11111 ?   0   0   11111 Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<invcond>` | `unknown` | `cond` | Is one of the standard conditions, excluding AL and NV, encoded with its least significant bit inverted, and |
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |

**<invcond> Value Table**:

| bitfield | symbol |
|---|---|
| 0000 |  |
| 0001 |  |
| 0010 |  |
| 0011 |  |
| 0100 |  |
| 0101 |  |
| 0110 |  |
| 0111 |  |
| 1000 |  |
| 1001 |  |
| 1010 |  |
| 1011 |  |
| 1100 |  |
| 1101 |  |

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

- alias_mnemonic: `CSETM`
- isa: `A64`
- source: `csetm_csinv.xml`
</details>