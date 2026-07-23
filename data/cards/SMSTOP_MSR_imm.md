## MSR `[ALIAS]`
_ARM A64 Instruction_ (Alias of msr_imm.xml)

**Title**: SMSTOP -- A64 | **Class**: `system` | **XML ID**: `SMSTOP_MSR_imm`

**Architecture**: `FEAT_SME` (PROFILE_A)

**Summary**: Disables access to Streaming SVE mode and SME architectural state

**Description**:
This instruction disables access to Streaming SVE mode and SME architectural state.

SMSTOP exits Streaming SVE mode, and disables the SME ZA storage.

SMSTOP SM exits Streaming SVE mode, but does not disable the SME ZA storage.

SMSTOP ZA disables the SME ZA storage, but does not cause an exit from Streaming SVE mode.

### Variant: `System`
- **Assembly**: `SMSTOP  {<option>}`
- **Alias of**: `MSR  <pstatefield>,   #0`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  18  15  11   7   4  |
|--------------------------|
| 110 101 0100000 011 0100 0xx0 011 11111 |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<option>` | `unknown` | `CRm<2:1>` | Is an optional mode, |

**<option> Value Table**:

| bitfield | symbol |
|---|---|
| 00 |  |
| 01 |  |
| 10 |  |
| 11 |  |

---
<details><summary>Metadata</summary>

- alias_mnemonic: `SMSTOP`
- isa: `A64`
- msr-sysreg-target: `whole-register`
- source: `smstop_msr_imm.xml`
</details>