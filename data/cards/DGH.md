## DGH
_ARM A64 Instruction_

**Title**: DGH -- A64 | **Class**: `system` | **XML ID**: `DGH`

**Architecture**: `FEAT_DGH` (PROFILE_R)

**Summary**: Data gathering hint

**Description**:
This instruction is a hint instruction that indicates that it is not expected to be performance
optimal to merge memory accesses with Normal Non-cacheable or Device-GRE attributes appearing in program
order before the hint instruction with any memory accesses appearing after the hint instruction into a
single memory transaction on an interconnect.

### Variant: `System`
- **Assembly**: `DGH`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  11   7   4  |
|--------------------|
| 110 101 01000000110010 0000 110 11111 |
```

#### Decode (A64.control.hints.DGH_HI_hints)

```
if !IsFeatureImplemented(FEAT_DGH) then EndOfDecode(Decode_NOP);
```

#### Execute (A64.control.hints.DGH_HI_hints)

```
Hint_DGH();
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_DGH)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `dgh.xml`
</details>