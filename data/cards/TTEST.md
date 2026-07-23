## TTEST
_ARM A64 Instruction_

**Title**: TTEST -- A64 | **Class**: `system` | **XML ID**: `TTEST`

**Architecture**: `FEAT_TME` (ARMv9.0)

**Summary**: Test transaction state

**Description**:
This instruction writes the depth of the transaction to the destination register,
or the value 0 otherwise.

### Variant: `System`
- **Assembly**: `TTEST  <Xt>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  18  15  11   7   4  |
|--------------------------|
| 110 101 0100100 011 0011 0001 011 Rt  |
```

#### Decode (A64.control.systemresult.TTEST_BR_systemresult)

```
if !IsFeatureImplemented(FEAT_TME) then EndOfDecode(Decode_UNDEF);
constant integer t = UInt(Rt);
```

#### Execute (A64.control.systemresult.TTEST_BR_systemresult)

```
if !IsTMEEnabled() then UNDEFINED;

X[t, 64] = (TSTATE.depth)<63:0>;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_TME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rt" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `ttest.xml`
</details>