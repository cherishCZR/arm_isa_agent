## GCSB
_ARM A64 Instruction_

**Title**: GCSB -- A64 | **Class**: `system` | **XML ID**: `GCSB`

**Architecture**: `FEAT_GCS` (ARMv9.4)

**Summary**: Guarded Control Stack barrier

**Description**:
This instruction generates a GCSB effect.

If FEAT_GCS is not implemented,
this instruction executes as a NOP.

### Variant: `System`
- **Assembly**: `GCSB  DSYNC`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  11   7   4  |
|--------------------|
| 110 101 01000000110010 0010 011 11111 |
```

#### Decode (A64.control.hints.GCSB_HD_hints)

```
if !IsFeatureImplemented(FEAT_GCS) then EndOfDecode(Decode_NOP);
```

#### Execute (A64.control.hints.GCSB_HD_hints)

```
GCSSynchronizationBarrier();
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_GCS)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `gcsb.xml`
</details>