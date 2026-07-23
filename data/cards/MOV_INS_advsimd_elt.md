## INS `[ALIAS]`
_ARM A64 Instruction_ (Alias of ins_advsimd_elt.xml)

**Title**: MOV (element) -- A64 | **Class**: `advsimd` | **XML ID**: `MOV_INS_advsimd_elt`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Move vector element to another vector element

**Description**:
This instruction copies the vector element
of the source SIMD&FP register
to the specified vector element
of the destination SIMD&FP register.

This instruction can insert data into individual elements within a SIMD&FP
register without clearing
the remaining bits to zero.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Advanced SIMD`
- **Assembly**: `MOV  <Vd>.<Ts>[<index1>], <Vn>.<Ts>[<index2>]`
- **Alias of**: `INS  <Vd>.<Ts>[<index1>], <Vn>.<Ts>[<index2>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24  22  20  15 14  10  9   4  |
|-----------------------------------------|
| 0   1   1   0   111 00  00  imm5 0   imm4 1   Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Ts>` | `unknown` | `imm5` | Is an element size specifier, |
| `<index1>` | `unknown` | `imm5` | Is the destination element index |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<index2>` | `unknown` | `imm5:imm4` | Is the source element index |

**<Ts> Value Table**:

| bitfield | symbol |
|---|---|
| x0000 | RESERVED |
| xxxx1 | B |
| xxx10 | H |
| xx100 | S |
| x1000 | D |

**<index1> Value Table**:

| bitfield | symbol |
|---|---|
| x0000 | RESERVED |
| xxxx1 | UInt(imm5<4:1>) |
| xxx10 | UInt(imm5<4:2>) |
| xx100 | UInt(imm5<4:3>) |
| x1000 | UInt(imm5<4>) |

**<index2> Value Table**:

| bitfield | symbol |
|---|---|
| x0000 | RESERVED |
| xxxx1 | UInt(imm4) |
| xxx10 | UInt(imm4<3:1>) |
| xx100 | UInt(imm4<3:2>) |
| x1000 | UInt(imm4<3>) |

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
- vector-xfer-type: `vector-from-element`
- source: `mov_ins_advsimd_elt.xml`
</details>