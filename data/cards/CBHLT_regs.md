## CBHGT `[ALIAS]`
_ARM A64 Instruction_ (Alias of cbhcc_regs.xml)

**Title**: CBHLT -- A64 | **Class**: `general` | **XML ID**: `CBHLT_regs`

**Architecture**: `FEAT_CMPBR` (ARMv9.6)

**Summary**: Compare signed less than halfwords and branch

**Description**:
This instruction compares the signed halfword values in two registers, and conditionally
branches to a label at a PC-relative offset if the second value is less than the first.
It provides a hint that this is not a subroutine call or return.
This instruction does not affect the condition flags.

### Variant: `Branch` (Greater than)
- **Assembly**: `CBHLT  <Wm>, <Wt>, <label>`
- **Alias of**: `CBHGT  <Wt>, <Wm>, <label>`
  Condition: Never
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  23  20  15 14 13   4  |
|-----------------------------|
| 011 101 00  000 Rm  1   1   imm9 Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wm>` | `register (32-bit)` | `Rm` | Is the 32-bit name of the second general-purpose source register, encoded in the "Rm" field. |
| `<Wt>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the general-purpose register to be tested, encoded in the "Rt" field. |
| `<label>` | `label` | `imm9` | Is the program label to be conditionally branched to. Its offset from the address of this instruction, in the range -1024 to 1020, is encoded as "imm9 |

---
<details><summary>Metadata</summary>

- alias_mnemonic: `CBHLT`
- datatype: `16`
- isa: `A64`
- sve-compare-type: `gt`
- source: `cbhlt_regs.xml`
</details>