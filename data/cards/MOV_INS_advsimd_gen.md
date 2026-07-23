## INS `[ALIAS]`
_ARM A64 Instruction_ (Alias of ins_advsimd_gen.xml)

**Title**: MOV (from general) -- A64 | **Class**: `advsimd` | **XML ID**: `MOV_INS_advsimd_gen`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Move general-purpose register to a vector element

**Description**:
This instruction copies the contents of
the source general-purpose register
to the specified vector element in the destination SIMD&FP register.

This instruction can insert data into individual elements within a SIMD&FP
register without clearing the remaining bits to zero.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Advanced SIMD`
- **Assembly**: `MOV  <Vd>.<Ts>[<index>], <R><n>`
- **Alias of**: `INS  <Vd>.<Ts>[<index>], <R><n>`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24  22  20  15 14  10  9   4  |
|-----------------------------------------|
| 0   1   0   0   111 00  00  imm5 0   0011 1   Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Ts>` | `unknown` | `imm5` | Is an element size specifier, |
| `<index>` | `unknown` | `imm5` | Is the element index |
| `<R>` | `unknown` | `imm5` | Is the width specifier for the general-purpose source register, |
| `<n>` | `unknown` | `Rn` | Is the number [0-30] of the general-purpose source register or ZR (31), encoded in the "Rn" field. |

**<Ts> Value Table**:

| bitfield | symbol |
|---|---|
| x0000 | RESERVED |
| xxxx1 | B |
| xxx10 | H |
| xx100 | S |
| x1000 | D |

**<index> Value Table**:

| bitfield | symbol |
|---|---|
| x0000 | RESERVED |
| xxxx1 | UInt(imm5<4:1>) |
| xxx10 | UInt(imm5<4:2>) |
| xx100 | UInt(imm5<4:3>) |
| x1000 | UInt(imm5<4>) |

**<R> Value Table**:

| bitfield | symbol |
|---|---|
| x0000 | RESERVED |
| xxxx1 | W |
| xxx10 | W |
| xx100 | W |
| x1000 | X |

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
- vector-xfer-type: `vector-from-general`
- source: `mov_ins_advsimd_gen.xml`
</details>