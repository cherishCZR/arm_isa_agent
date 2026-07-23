## CBGT `[ALIAS]`
_ARM A64 Instruction_ (Alias of cbcc_regs.xml)

**Title**: CBLT (register) -- A64 | **Class**: `general` | **XML ID**: `CBLT_regs`

**Architecture**: `FEAT_CMPBR` (ARMv9.6)

**Summary**: Compare signed less than register and branch

**Description**:
This instruction compares the signed values in two registers, and conditionally
branches to a label at a PC-relative offset if the second value is less than the first.
It provides a hint that this is not a subroutine call or return.
This instruction does not affect the condition flags.

### Variant: `Branch (CBLT_CBGT_32_regs)` (32-bit greater than)
- **Condition**: `sf == 0`
- **Assembly**: `CBLT  <Wm>, <Wt>, <label>`
- **Fixed bits**: `sf`=`0`
- **Bit Pattern**: `???????????????????????????????0`
- **Alias of**: `CBGT  <Wt>, <Wm>, <label>`
  Condition: Never
**Encoding Diagram (32-bit)**:

```text
| 31 30  23  20  15  13   4  |
|-----------------------|
| sf  1110100 000 Rm  00  imm9 Rt  |
```

### Variant: `Branch (CBLT_CBGT_64_regs)` (64-bit greater than)
- **Condition**: `sf == 1`
- **Assembly**: `CBLT  <Xm>, <Xt>, <label>`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
- **Alias of**: `CBGT  <Xt>, <Xm>, <label>`
  Condition: Never
**Encoding Diagram (32-bit)**:

```text
| 31 30  23  20  15  13   4  |
|-----------------------|
| sf  1110100 000 Rm  00  imm9 Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wm>` | `register (32-bit)` | `Rm` | Is the 32-bit name of the second general-purpose source register, encoded in the "Rm" field. |
| `<Wt>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the general-purpose register to be tested, encoded in the "Rt" field. |
| `<label>` | `label` | `imm9` | Is the program label to be conditionally branched to. Its offset from the address of this instruction, in the range -1024 to 1020, is encoded as "imm9 |
| `<Xm>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the second general-purpose source register, encoded in the "Rm" field. |
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose register to be tested, encoded in the "Rt" field. |

---
<details><summary>Metadata</summary>

- alias_mnemonic: `CBLT`
- isa: `A64`
- sve-compare-type: `gt`
- source: `cblt_regs.xml`
</details>