## PACM
_ARM A64 Instruction_

**Title**: PACM -- A64 | **Class**: `system` | **XML ID**: `PACM`

**Architecture**: `FEAT_PAuth_LR` (ARMv9.5)

**Summary**: Pointer authentication modifier

**Description**:
This instruction is used to set the value of PSTATE.PACM to 1.

If FEAT_PAuth_LR is not implemented,
this instruction behaves as a NOP.

### Variant: `System`
- **Assembly**: `PACM`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  11   7   4  |
|--------------------|
| 110 101 01000000110010 0100 111 11111 |
```

#### Decode (A64.control.hints.PACM_HI_hints)

```
if !IsFeatureImplemented(FEAT_PAuth_LR) then EndOfDecode(Decode_NOP);
```

#### Execute (A64.control.hints.PACM_HI_hints)

```
PSTATE.PACM = if IsPACMEnabled() then '1' else '0';
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_PAuth_LR)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `pacm.xml`
</details>