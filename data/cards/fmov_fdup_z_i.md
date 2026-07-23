## FDUP `[ALIAS]`
_ARM A64 Instruction_ (Alias of fdup_z_i.xml)

**Title**: FMOV (immediate, unpredicated) -- A64 | **Class**: `sve` | **XML ID**: `fmov_fdup_z_i`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Move 8-bit floating-point immediate to vector elements (unpredicated)

**Description**:
Unconditionally broadcast the floating-point immediate into each element of the
destination vector. This instruction is unpredicated.

### Variant: `SVE`
- **Assembly**: `FMOV  <Zd>.<T>, #<const>`
- **Alias of**: `FDUP  <Zd>.<T>, #<const>`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18  16 15  13 12   4  |
|--------------------------------------|
| 001 0010 1   size 1   11  00  1   11  0   imm8 Zd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<const>` | `unknown` | `imm8` | Is a floating-point immediate value expressible as ±n÷16×2^r, where n and r are integers such that 16 ≤ n ≤ 31 and -3 ≤ r ≤ 4, i.e. a normalized binar |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | H |
| 10 | S |
| 11 | D |

---
<details><summary>Metadata</summary>

- alias_mnemonic: `FMOV`
- isa: `A64`
- source: `fmov_fdup_z_i.xml`
</details>