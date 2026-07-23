## MSR `[ALIAS]`
_ARM A64 Instruction_ (Alias of msr_imm.xml)

**Title**: SMSTART -- A64 | **Class**: `system` | **XML ID**: `SMSTART_MSR_imm`

**Architecture**: `FEAT_SME` (PROFILE_A)

**Summary**: Enables access to Streaming SVE mode and SME architectural state

**Description**:
This instruction enables access to Streaming SVE mode and SME architectural state.

SMSTART enters Streaming SVE mode, and enables the SME ZA storage.

SMSTART SM enters Streaming SVE mode, but does not enable the SME ZA storage.

SMSTART ZA enables the SME ZA storage, but does not cause an entry to Streaming SVE mode.

### Variant: `System`
- **Assembly**: `SMSTART  {<option>}`
- **Alias of**: `MSR  <pstatefield>,   #1`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  18  15  11   7   4  |
|--------------------------|
| 110 101 0100000 011 0100 0xx1 011 11111 |
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

- alias_mnemonic: `SMSTART`
- isa: `A64`
- msr-sysreg-target: `whole-register`
- source: `smstart_msr_imm.xml`
</details>