## TSB
_ARM A64 Instruction_

**Title**: TSB -- A64 | **Class**: `system` | **XML ID**: `TSB`

**Architecture**: `FEAT_TRF` (ARMv8.4)

**Summary**: Trace synchronization barrier

**Description**:
This instruction is a barrier that synchronizes the trace operations
of instructions, see
Trace Synchronization Barrier (TSB).

If FEAT_TRF is not implemented, this instruction executes as a
NOP.

### Variant: `System`
- **Assembly**: `TSB  CSYNC`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  11   7   4  |
|--------------------|
| 110 101 01000000110010 0010 010 11111 |
```

#### Decode (A64.control.hints.TSB_HC_hints)

```
if !IsFeatureImplemented(FEAT_TRF) then EndOfDecode(Decode_NOP);
```

#### Execute (A64.control.hints.TSB_HC_hints)

```
if IsFeatureImplemented(FEAT_FGT2) && IsFeatureImplemented(FEAT_TRBEv1p1) then
    constant boolean trap_to_el2 = (PSTATE.EL IN {EL0, EL1} && EL2Enabled() &&
                                    !IsInHost() &&
                                    (!HaveEL(EL3) || SCR_EL3.FGTEn2 == '1') &&
                                    HFGITR2_EL2.TSBCSYNC == '1');
    if trap_to_el2 then
        ExceptionRecord except = ExceptionSyndrome(Exception_LDST64BTrap); // to be renamed
        except.syndrome.iss = 0x4<24:0>;
        constant bits(64) preferred_exception_return = ThisInstrAddr(64);
        constant integer vect_offset = 0x0;
        AArch64.TakeException(EL2, except, preferred_exception_return, vect_offset);

TraceSynchronizationBarrier();
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_TRF)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `tsb.xml`
</details>