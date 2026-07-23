## DUP `[ALIAS]`
_ARM A64 Instruction_ (Alias of dup_z_i.xml)

**Title**: FMOV (zero, unpredicated) -- A64 | **Class**: `sve` | **XML ID**: `fmov_dup_z_i`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Move floating-point +0.0 to vector elements (unpredicated)

**Description**:
Unconditionally broadcast the floating-point constant +0.0 into each element of the
destination vector. This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE`
- **Assembly**: `FMOV  <Zd>.<T>, #0.0`
- **Alias of**: `DUP  <Zd>.<T>, #0`
  Condition: Never
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18  16 15  13 12   4  |
|--------------------------------------|
| 001 0010 1   size 1   11  00  0   11  0   00000000 Zd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | H |
| 10 | S |
| 11 | D |

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

- alias_mnemonic: `FMOV`
- isa: `A64`
- source: `fmov_dup_z_i.xml`
</details>