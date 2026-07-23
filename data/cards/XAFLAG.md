## XAFLAG
_ARM A64 Instruction_

**Title**: XAFLAG -- A64 | **Class**: `system` | **XML ID**: `XAFLAG`

**Architecture**: `FEAT_FlagM2` (ARMv8.5)

**Summary**: Convert floating-point condition flags from external format to Arm format

**Description**:
This instruction converts the state of the PSTATE.{N,Z,C,V} flags from an
alternative representation required by some software to a form representing
the result of an Arm floating-point scalar compare instruction.

### Variant: `System`
- **Assembly**: `XAFLAG`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  18  15  11   7   4  |
|--------------------------|
| 110 101 0100000 000 0100 (0)(0)(0)(0) 001 11111 |
```

#### Decode (A64.control.pstate.XAFLAG_M_pstate)

```
if !IsFeatureImplemented(FEAT_FlagM2) then EndOfDecode(Decode_UNDEF);
```

#### Execute (A64.control.pstate.XAFLAG_M_pstate)

```
constant bit n = NOT(PSTATE.C) AND NOT(PSTATE.Z);
constant bit z = PSTATE.Z AND PSTATE.C;
constant bit c = PSTATE.C OR PSTATE.Z;
constant bit v = NOT(PSTATE.C) AND PSTATE.Z;

PSTATE.N = n;
PSTATE.Z = z;
PSTATE.C = c;
PSTATE.V = v;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FlagM2)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `xaflag.xml`
</details>