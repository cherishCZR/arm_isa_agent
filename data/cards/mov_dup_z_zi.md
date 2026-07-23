## DUP `[ALIAS]`
_ARM A64 Instruction_ (Alias of dup_z_zi.xml)

**Title**: MOV (SIMD&FP scalar, unpredicated) -- A64 | **Class**: `sve` | **XML ID**: `mov_dup_z_zi`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Move indexed element or SIMD&FP scalar to vector (unpredicated)

**Description**:
Unconditionally broadcast the SIMD&FP scalar into each element of the
destination vector. This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE (mov_z_v__dup_z_zi_)`
- **Assembly**: `MOV  <Zd>.<T>, <V><n>`
- **Alias of**: `DUP  <Zd>.<T>, <Zn>.<T>[0]`
**Encoding Diagram (32-bit)**:

```text
| 31  23  21 20  15   9   4  |
|-----------------------|
| 00000101 imm2 1   tsz 001000 Zn  Zd  |
```

### Variant: `SVE (mov_z_zi__dup_z_zi_)`
- **Assembly**: `MOV  <Zd>.<T>, <Zn>.<T>[<imm>]`
- **Alias of**: `DUP  <Zd>.<T>, <Zn>.<T>[<imm>]`
**Encoding Diagram (32-bit)**:

```text
| 31  23  21 20  15   9   4  |
|-----------------------|
| 00000101 imm2 1   tsz 001000 Zn  Zd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `tsz` | Is the size specifier, |
| `<V>` | `register (128-bit)` | `tsz` | Is a width specifier, |
| `<n>` | `unknown` | `Zn` | Is the number [0-31] of the source SIMD&FP register, encoded in the "Zn" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |
| `<imm>` | `immediate` | `imm2:tsz` | Is the immediate index, in the range 0 to one less than the number of elements in 512 bits, encoded in "imm2:tsz". |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00000 | RESERVED |
| xxxx1 | B |
| xxx10 | H |
| xx100 | S |
| x1000 | D |
| 10000 | Q |

**<V> Value Table**:

| bitfield | symbol |
|---|---|
| 00000 | RESERVED |
| xxxx1 | B |
| xxx10 | H |
| xx100 | S |
| x1000 | D |
| 10000 | Q |

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
- source: `mov_dup_z_zi.xml`
</details>