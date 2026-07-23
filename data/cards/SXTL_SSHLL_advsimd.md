## SSHLL `[ALIAS]`
_ARM A64 Instruction_ (Alias of sshll_advsimd.xml)

**Title**: SXTL, SXTL2 -- A64 | **Class**: `advsimd` | **XML ID**: `SXTL_SSHLL_advsimd`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Signed extend long

**Description**:
This instruction duplicates each vector element in the
lower or upper half of the source SIMD&FP register into a vector,
and writes the vector to the destination SIMD&FP
register.
The destination vector elements are twice
as long as the source vector elements.
All the values in this instruction are signed integer values.

The SXTL instruction extracts
the source vector from the lower half
of the source register. The SXTL2 instruction extracts
the source vector from the upper half
of the source register.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Vector`
- **Assembly**: `SXTL{2}  <Vd>.<Ta>, <Vn>.<Tb>`
- **Alias of**: `SSHLL{2}  <Vd>.<Ta>, <Vn>.<Tb>, #0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24  22  18  15  10  9   4  |
|--------------------------------------|
| 0   Q   0   0   111 10  ?   000 10100 1   Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `2` | `unknown` | `Q` | Is the second and upper half specifier. If present it causes the operation to be performed on the upper 64 bits of the registers holding the narrower  |
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Ta>` | `unknown` | `immh` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<Tb>` | `unknown` | `immh:Q` | Is an arrangement specifier, |

**2 Value Table**:

| bitfield | symbol |
|---|---|
| 0 | [absent] |
| 1 | [present] |

**<Ta> Value Table**:

| bitfield | symbol |
|---|---|
| 0001 | 8H |
| 001x | 4S |
| 01xx | 2D |
| 1xxx | RESERVED |

**<Tb> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 8B |
| 1 | 16B |
| 0 | 4H |
| 1 | 8H |
| 0 | 2S |
| 1 | 4S |
| x | RESERVED |

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
- alias_mnemonic: `SXTL`
- isa: `A64`
- source: `sxtl_sshll_advsimd.xml`
</details>