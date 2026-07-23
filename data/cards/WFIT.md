## WFIT
_ARM A64 Instruction_

**Title**: WFIT -- A64 | **Class**: `system` | **XML ID**: `WFIT`

**Architecture**: `FEAT_WFxT` (ARMv8.7)

**Summary**: Wait for interrupt with timeout

**Description**:
This instruction is a hint instruction that indicates that the PE
can enter a low-power state and remain there until either a local timeout event
or a wakeup event occurs.
For more information, see Wait For Interrupt.

As described in Wait For Interrupt, the execution
of a WFIT instruction that would otherwise cause entry to a low-power
state can be trapped to a higher Exception level.

### Variant: `System`
- **Assembly**: `WFIT  <Xt>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  11   7   4  |
|--------------------|
| 110 101 01000000110001 0000 001 Rd  |
```

#### Decode (A64.control.systeminstrswithreg.WFIT_only_systeminstrswithreg)

```
if !IsFeatureImplemented(FEAT_WFxT) then EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
```

#### Execute (A64.control.systeminstrswithreg.WFIT_only_systeminstrswithreg)

```
constant integer localtimeout = UInt(X[d, 64]);

if Halted() && ConstrainUnpredictableBool(Unpredictable_WFxTDEBUG) then
    ExecuteAsNOP();

Hint_WFIT(localtimeout);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_WFxT)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xt>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose source register, encoded in the "Rd" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `wfit.xml`
</details>