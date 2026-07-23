## SB
_ARM A64 Instruction_

**Title**: SB -- A64 | **Class**: `system` | **XML ID**: `SB`

**Architecture**: `FEAT_SB` (PROFILE_R)

**Summary**: Speculation barrier

**Description**:
This instruction is a barrier that controls speculation.
For more information and details of the semantics, see
Speculation Barrier (SB).

### Variant: `System`
- **Assembly**: `SB`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  11   7  6   4  |
|-----------------------|
| 110 101 01000000110011 (0)(0)(0)(0) 1   11  11111 |
```

#### Decode (A64.control.barriers.SB_only_barriers)

```
if !IsFeatureImplemented(FEAT_SB) then EndOfDecode(Decode_UNDEF);
```

#### Execute (A64.control.barriers.SB_only_barriers)

```
SpeculationBarrier();
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SB)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `sb.xml`
</details>