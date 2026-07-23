## CBLT `[ALIAS]`
_ARM A64 Instruction_ (Alias of cbcc_imm.xml)

**Title**: CBLE (immediate) -- A64 | **Class**: `general` | **XML ID**: `CBLE_imm`

**Architecture**: `FEAT_CMPBR` (ARMv9.6)

**Summary**: Compare signed less than or equal immediate and branch

**Description**:
This instruction compares the signed value in a register with an
immediate, and conditionally branches to a label at a PC-relative offset
if the register value is less than or equal to the immediate. It
provides a hint that this is not a subroutine call or return. This
instruction does not affect the condition flags.

### Variant: `Branch (CBLE_CBLT_32_imm)` (32-bit less than)
- **Condition**: `sf == 0`
- **Assembly**: `CBLE  <Wt>, #<imms1>, <label>`
- **Fixed bits**: `sf`=`0`
- **Bit Pattern**: `???????????????????????????????0`
- **Alias of**: `CBLT  <Wt>, #<imm>, <label>`
  Condition: Never
**Encoding Diagram (32-bit)**:

```text
| 31 30  23  20  14 13   4  |
|-----------------------|
| sf  1110101 001 imm6 0   imm9 Rt  |
```

### Variant: `Branch (CBLE_CBLT_64_imm)` (64-bit less than)
- **Condition**: `sf == 1`
- **Assembly**: `CBLE  <Xt>, #<imms1>, <label>`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
- **Alias of**: `CBLT  <Xt>, #<imm>, <label>`
  Condition: Never
**Encoding Diagram (32-bit)**:

```text
| 31 30  23  20  14 13   4  |
|-----------------------|
| sf  1110101 001 imm6 0   imm9 Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wt>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the general-purpose register to be tested, encoded in the "Rt" field. |
| `<imms1>` | `immediate` | `imm6` | Is a signed immediate, in the range -1 to 62, encoded as "imm6" minus 1. |
| `<label>` | `label` | `imm9` | Is the program label to be conditionally branched to. Its offset from the address of this instruction, in the range -1024 to 1020, is encoded as "imm9 |
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose register to be tested, encoded in the "Rt" field. |

---
<details><summary>Metadata</summary>

- alias_mnemonic: `CBLE`
- isa: `A64`
- sve-compare-type: `lt`
- source: `cble_imm.xml`
</details>