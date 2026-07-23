## ESB
_ARM A64 Instruction_

**Title**: ESB -- A64 | **Class**: `system` | **XML ID**: `ESB`

**Architecture**: `FEAT_RAS` (ARMv8.2)

**Summary**: Error synchronization barrier

**Description**:
This instruction is an error synchronization event that might also update DISR_EL1 and VDISR_EL2.

This instruction can be used at all Exception levels and in Debug state.

In Debug state, this instruction behaves as if SError interrupts are masked at all Exception levels.
For more information, see RAS PE architecture
and Arm® Reliability, Availability, and Serviceability (RAS) System Architecture, for A-profile architecture (ARM IHI 0100).

If FEAT_RAS is not implemented, this instruction executes as a NOP.

### Variant: `System`
- **Assembly**: `ESB`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  11   7   4  |
|--------------------|
| 110 101 01000000110010 0010 000 11111 |
```

#### Decode (A64.control.hints.ESB_HI_hints)

```
if !IsFeatureImplemented(FEAT_RAS) then EndOfDecode(Decode_NOP);
```

#### Execute (A64.control.hints.ESB_HI_hints)

```
if IsFeatureImplemented(FEAT_TME) && TSTATE.depth > 0 then
    FailTransaction(TMFailure_ERR, FALSE);
SynchronizeErrors();
AArch64.ESBOperation();
if PSTATE.EL IN {EL0, EL1} && EL2Enabled() then AArch64.vESBOperation();
TakeUnmaskedSErrorInterrupts();
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_RAS)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `esb.xml`
</details>