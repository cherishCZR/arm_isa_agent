## NOT `[ALIAS]`
_ARM A64 Instruction_ (Alias of not_advsimd.xml)

**Title**: MVN -- A64 | **Class**: `advsimd` | **XML ID**: `MVN_NOT_advsimd`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Bitwise NOT (vector)

**Description**:
This instruction reads each vector element from the source SIMD&FP register,
places the inverse of each value into a vector, and writes the
vector to the destination SIMD&FP register.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Vector`
- **Assembly**: `MVN  <Vd>.<T>, <Vn>.<T>`
- **Alias of**: `NOT  <Vd>.<T>, <Vn>.<T>`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21  16  11   9   4  |
|--------------------------------------|
| 0   Q   1   0   111 0   00  10000 00101 10  Rn  Rd  |
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

- advsimd-type: `simd`
- alias_mnemonic: `MVN`
- isa: `A64`
- source: `mvn_not_advsimd.xml`
</details>