## CHKFEAT
_ARM A64 Instruction_

**Title**: CHKFEAT -- A64 | **Class**: `system` | **XML ID**: `CHKFEAT`

**Architecture**: `FEAT_CHK` (ARMv9.4)

**Summary**: Check feature status

**Description**:
This instruction indicates the status of features. For more information, see
Check Feature.

If FEAT_CHK is not implemented, this instruction executes as a NOP.

### Variant: `System`
- **Assembly**: `CHKFEAT  X16`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  11   7   4  |
|--------------------|
| 110 101 01000000110010 0101 000 11111 |
```

#### Decode (A64.control.hints.CHKFEAT_HF_hints)

```
if !IsFeatureImplemented(FEAT_CHK) then EndOfDecode(Decode_NOP);
```

#### Execute (A64.control.hints.CHKFEAT_HF_hints)

```
X[16, 64] = AArch64.ChkFeat(X[16, 64]);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_CHK)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `chkfeat.xml`
</details>