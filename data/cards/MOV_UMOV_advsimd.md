## UMOV `[ALIAS]`
_ARM A64 Instruction_ (Alias of umov_advsimd.xml)

**Title**: MOV (to general) -- A64 | **Class**: `advsimd` | **XML ID**: `MOV_UMOV_advsimd`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Move vector element to general-purpose register

**Description**:
This instruction reads the unsigned integer from the
source SIMD&FP register,
zero-extends it to form a 32-bit or 64-bit value, and writes the result to
the destination general-purpose register.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Advanced SIMD (MOV_UMOV_asimdins_W_w)` (32-bit)
- **Condition**: `Q == 0 && imm5 == xx100`
- **Assembly**: `MOV  <Wd>, <Vn>.S[<index>]`
- **Fixed bits**: `Q`=`0`, `imm5`=`x1`
- **Bit Pattern**: `??????????????????1???????????0?`
- **Alias of**: `UMOV  <Wd>, <Vn>.S[<index>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15 14  10  9   4  |
|--------------------------------|
| 0   Q   0   01110000 xxx00 0   0111 1   Rn  Rd  |
```

### Variant: `Advanced SIMD (MOV_UMOV_asimdins_X_x)` (64-bit)
- **Condition**: `Q == 1 && imm5 == x1000`
- **Assembly**: `MOV  <Xd>, <Vn>.D[<index>]`
- **Fixed bits**: `Q`=`1`, `imm5`=`10`
- **Bit Pattern**: `??????????????????01??????????1?`
- **Alias of**: `UMOV  <Xd>, <Vn>.D[<index>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15 14  10  9   4  |
|--------------------------------|
| 0   Q   0   01110000 xxx00 0   0111 1   Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<index>` | `unknown` | `imm5` | For the "32-bit" variant: is the element index encoded in "imm5<4:3>". |
| `<index>` | `unknown` | `imm5` | For the "64-bit" variant: is the element index encoded in "imm5<4>". |
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |

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
- vector-xfer-type: `general-from-element`
- source: `mov_umov_advsimd.xml`
</details>