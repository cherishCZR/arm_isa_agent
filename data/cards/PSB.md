## PSB
_ARM A64 Instruction_

**Title**: PSB -- A64 | **Class**: `system` | **XML ID**: `PSB`

**Architecture**: `FEAT_SPE` (PROFILE_A)

**Summary**: Profiling synchronization barrier

**Description**:
This instruction is a barrier that ensures that all existing
profiling data for the current PE has been formatted, and profiling
buffer addresses have been translated such that all writes to the
profiling buffer have been initiated. A following DSB
instruction completes when the writes to the profiling buffer have
completed.

If FEAT_SPE is not implemented,
this instruction executes as a NOP.

### Variant: `System`
- **Assembly**: `PSB  CSYNC`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  11   7   4  |
|--------------------|
| 110 101 01000000110010 0010 001 11111 |
```

#### Decode (A64.control.hints.PSB_HC_hints)

```
if !IsFeatureImplemented(FEAT_SPE) then EndOfDecode(Decode_NOP);
```

#### Execute (A64.control.hints.PSB_HC_hints)

```
if IsFeatureImplemented(FEAT_FGT) && IsFeatureImplemented(FEAT_SPEv1p5) then
    constant boolean trap_to_el2 = (PSTATE.EL IN {EL0, EL1} && EL2Enabled() &&
                                    !IsInHost() &&
                                    (!HaveEL(EL3) || SCR_EL3.FGTEn == '1') &&
                                    HFGITR_EL2.PSBCSYNC == '1');
    if trap_to_el2 then
        ExceptionRecord except = ExceptionSyndrome(Exception_LDST64BTrap); // to be renamed
        except.syndrome.iss = 0x3<24:0>;
        constant bits(64) preferred_exception_return = ThisInstrAddr(64);
        constant integer vect_offset = 0x0;
        AArch64.TakeException(EL2, except, preferred_exception_return, vect_offset);

ProfilingSynchronizationBarrier();
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SPE)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `psb.xml`
</details>