## AXFLAG
_ARM A64 Instruction_

**Title**: AXFLAG -- A64 | **Class**: `system` | **XML ID**: `AXFLAG`

**Architecture**: `FEAT_FlagM2` (ARMv8.5)

**Summary**: Convert floating-point condition flags from Arm to external format

**Description**:
This instruction converts the state of the PSTATE.{N,Z,C,V} flags from
a form representing the result of an Arm floating-point scalar compare
instruction to an alternative representation required by some software.

### Variant: `System`
- **Assembly**: `AXFLAG`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  18  15  11   7   4  |
|--------------------------|
| 110 101 0100000 000 0100 (0)(0)(0)(0) 010 11111 |
```

#### Decode (A64.control.pstate.AXFLAG_M_pstate)

```
if !IsFeatureImplemented(FEAT_FlagM2) then EndOfDecode(Decode_UNDEF);
```

#### Execute (A64.control.pstate.AXFLAG_M_pstate)

```
constant bit z = PSTATE.Z OR PSTATE.V;
constant bit c = PSTATE.C AND NOT(PSTATE.V);

PSTATE.<N,Z,C,V> = '0' : z : c : '0';
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FlagM2)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `axflag.xml`
</details>