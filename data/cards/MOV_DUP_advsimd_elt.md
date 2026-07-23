## DUP `[ALIAS]`
_ARM A64 Instruction_ (Alias of dup_advsimd_elt.xml)

**Title**: MOV (scalar) -- A64 | **Class**: `advsimd` | **XML ID**: `MOV_DUP_advsimd_elt`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Move vector element to scalar

**Description**:
This instruction duplicates the specified vector element
in the SIMD&FP source register
into a scalar,
and writes the result to the SIMD&FP destination register.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Scalar`
- **Assembly**: `MOV  <V><d>, <Vn>.<T>[<index>]`
- **Alias of**: `DUP  <V><d>, <Vn>.<T>[<index>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  29 28 27  24  22  20  15 14  10  9   4  |
|--------------------------------------|
| 01  0   1   111 00  00  imm5 0   0000 1   Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<V>` | `register (128-bit)` | `imm5` | Is the destination width specifier, |
| `<d>` | `unknown` | `Rd` | Is the number of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<T>` | `unknown` | `imm5` | Is the element width specifier, |
| `<index>` | `unknown` | `imm5` | Is the element index |

**<V> Value Table**:

| bitfield | symbol |
|---|---|
| x0000 | RESERVED |
| xxxx1 | B |
| xxx10 | H |
| xx100 | S |
| x1000 | D |

**<T> Value Table**:

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
- vector-xfer-type: `scalar-from-element`
- source: `mov_dup_advsimd_elt.xml`
</details>