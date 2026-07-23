## CBGT `[ALIAS]`
_ARM A64 Instruction_ (Alias of cbcc_imm.xml)

**Title**: CBGE (immediate) -- A64 | **Class**: `general` | **XML ID**: `CBGE_imm`

**Architecture**: `FEAT_CMPBR` (ARMv9.6)

**Summary**: Compare signed greater than or equal immediate and branch

**Description**:
This instruction compares the signed value in a register with an
immediate, and conditionally branches to a label at a PC-relative offset
if the register value is greater than or equal to the immediate. It
provides a hint that this is not a subroutine call or return. This
instruction does not affect the condition flags.

### Variant: `Branch (CBGE_CBGT_32_imm)` (32-bit greater than)
- **Condition**: `sf == 0`
- **Assembly**: `CBGE  <Wt>, #<immp1>, <label>`
- **Fixed bits**: `sf`=`0`
- **Bit Pattern**: `???????????????????????????????0`
- **Alias of**: `CBGT  <Wt>, #<imm>, <label>`
  Condition: Never
**Encoding Diagram (32-bit)**:

```text
| 31 30  23  20  14 13   4  |
|-----------------------|
| sf  1110101 000 imm6 0   imm9 Rt  |
```

### Variant: `Branch (CBGE_CBGT_64_imm)` (64-bit greater than)
- **Condition**: `sf == 1`
- **Assembly**: `CBGE  <Xt>, #<immp1>, <label>`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
- **Alias of**: `CBGT  <Xt>, #<imm>, <label>`
  Condition: Never
**Encoding Diagram (32-bit)**:

```text
| 31 30  23  20  14 13   4  |
|-----------------------|
| sf  1110101 000 imm6 0   imm9 Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wt>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the general-purpose register to be tested, encoded in the "Rt" field. |
| `<immp1>` | `immediate` | `imm6` | Is an unsigned immediate, in the range 1 to 64, encoded as "imm6" plus 1. |
| `<label>` | `label` | `imm9` | Is the program label to be conditionally branched to. Its offset from the address of this instruction, in the range -1024 to 1020, is encoded as "imm9 |
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose register to be tested, encoded in the "Rt" field. |

---
<details><summary>Metadata</summary>

- alias_mnemonic: `CBGE`
- isa: `A64`
- sve-compare-type: `gt`
- source: `cbge_imm.xml`
</details>