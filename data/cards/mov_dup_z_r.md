## DUP `[ALIAS]`
_ARM A64 Instruction_ (Alias of dup_z_r.xml)

**Title**: MOV (scalar, unpredicated) -- A64 | **Class**: `sve` | **XML ID**: `mov_dup_z_r`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Move general-purpose register to vector elements (unpredicated)

**Description**:
Unconditionally broadcast the general-purpose scalar source register into each element of the
destination vector. This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE`
- **Assembly**: `MOV  <Zd>.<T>, <R><n|SP>`
- **Alias of**: `DUP  <Zd>.<T>, <R><n|SP>`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18  15   9   4  |
|--------------------------------|
| 000 0010 1   size 1   00  000 001110 Rn  Zd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<R>` | `unknown` | `size` | Is a width specifier, |
| `<n\|SP>` | `unknown` | `Rn` | Is the number [0-30] of the general-purpose source register or the name SP (31), encoded in the "Rn" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

**<R> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | W |
| 01 | W |
| 10 | W |
| 11 | X |

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

- alias_mnemonic: `MOV`
- isa: `A64`
- source: `mov_dup_z_r.xml`
</details>