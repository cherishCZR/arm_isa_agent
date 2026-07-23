## SEL `[ALIAS]`
_ARM A64 Instruction_ (Alias of sel_z_p_zz.xml)

**Title**: MOV (vector, predicated) -- A64 | **Class**: `sve` | **XML ID**: `mov_sel_z_p_zz`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Move vector elements (predicated)

**Description**:
Move elements from the source vector to the
corresponding elements of the destination vector. Inactive elements in the destination vector register remain unmodified.

**Attributes**: Predicated; DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE`
- **Assembly**: `MOV  <Zd>.<T>, <Pv>/M, <Zn>.<T>`
- **Alias of**: `SEL  <Zd>.<T>, <Pv>, <Zn>.<T>, <Zd>.<T>`
  Condition: Zd == Zm
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  13   9   4  |
|--------------------------------|
| 000 0010 1   size 1   Zm  11  Pv  Zn  Zd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Pv>` | `unknown` | `Pv` | Is the name of the vector select predicate register, encoded in the "Pv" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
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

- alias_mnemonic: `MOV`
- isa: `A64`
- source: `mov_sel_z_p_zz.xml`
</details>