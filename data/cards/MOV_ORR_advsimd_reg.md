## ORR `[ALIAS]`
_ARM A64 Instruction_ (Alias of orr_advsimd_reg.xml)

**Title**: MOV (vector) -- A64 | **Class**: `advsimd` | **XML ID**: `MOV_ORR_advsimd_reg`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Move vector

**Description**:
This instruction copies the vector in the source SIMD&FP register
into the destination SIMD&FP register.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Three registers of the same type`
- **Assembly**: `MOV  <Vd>.<T>, <Vn>.<T>`
- **Alias of**: `ORR  <Vd>.<T>, <Vn>.<T>, <Vn>.<T>`
  Condition: Rm == Rn
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21 20  15  10  9   4  |
|-----------------------------------------|
| 0   Q   0   0   111 0   10  1   Rm  00011 1   Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<T>` | `unknown` | `Q` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP source register, encoded in the "Rn" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 8B |
| 1 | 16B |

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

- advsimd-reguse: `3reg-same`
- advsimd-type: `simd`
- alias_mnemonic: `MOV`
- isa: `A64`
- source: `mov_orr_advsimd_reg.xml`
</details>