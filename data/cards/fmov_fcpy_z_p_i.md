## FCPY `[ALIAS]`
_ARM A64 Instruction_ (Alias of fcpy_z_p_i.xml)

**Title**: FMOV (immediate, predicated) -- A64 | **Class**: `sve` | **XML ID**: `fmov_fcpy_z_p_i`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Move 8-bit floating-point immediate to vector elements (predicated)

**Description**:
Move a floating-point immediate into each active element
in the destination vector. Inactive elements in the destination vector register remain unmodified.

**Attributes**: Predicated

### Variant: `SVE`
- **Assembly**: `FMOV  <Zd>.<T>, <Pg>/M, #<const>`
- **Alias of**: `FCPY  <Zd>.<T>, <Pg>/M, #<const>`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  19  15  12   4  |
|-----------------------------|
| 000 0010 1   size 01  Pg  110 imm8 Zd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register, encoded in the "Pg" field. |
| `<const>` | `unknown` | `imm8` | Is a floating-point immediate value expressible as ±n÷16×2^r, where n and r are integers such that 16 ≤ n ≤ 31 and -3 ≤ r ≤ 4, i.e. a normalized binar |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | H |
| 10 | S |
| 11 | D |

### Operational Notes

This instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must conform to all of the following requirements, otherwise the behavior of the MOVPRFX and this instruction is CONSTRAINED UNPREDICTABLE:
        
          
            The MOVPRFX can be predicated or unpredicated.
          
          
            A predicated MOVPRFX must use the same governing predicate register as this instruction.
          
          
            A predicated MOVPRFX must use the larger of the destination element size and first source element size in the preferred disassembly of this instruction.
          
          
            The MOVPRFX must specify the same destination register as this instruction.
          
          
            The destination register must not refer to architectural register state referenced by any other source operand register of this instruction.

---
<details><summary>Metadata</summary>

- alias_mnemonic: `FMOV`
- isa: `A64`
- source: `fmov_fcpy_z_p_i.xml`
</details>