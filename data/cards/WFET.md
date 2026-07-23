## WFET
_ARM A64 Instruction_

**Title**: WFET -- A64 | **Class**: `system` | **XML ID**: `WFET`

**Architecture**: `FEAT_WFxT` (ARMv8.7)

**Summary**: Wait for event with timeout

**Description**:
This instruction is a hint instruction that indicates that the PE
can enter a low-power state and remain there until either a local timeout event
or a wakeup event occurs. Wakeup events include the event signaled as a result
of executing the SEV instruction on any PE in the multiprocessor system.
For more information, see Wait For Event
mechanism and Send event.

As described in Wait For Event mechanism and Send event, the
execution of a WFET instruction that would otherwise cause entry to a low-power
state can be trapped to a higher Exception level.

### Variant: `System`
- **Assembly**: `WFET  <Xt>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  11   7   4  |
|--------------------|
| 110 101 01000000110001 0000 000 Rd  |
```

#### Decode (A64.control.systeminstrswithreg.WFET_only_systeminstrswithreg)

```
if !IsFeatureImplemented(FEAT_WFxT) then EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
```

#### Execute (A64.control.systeminstrswithreg.WFET_only_systeminstrswithreg)

```
constant integer localtimeout = UInt(X[d, 64]);

if Halted() && ConstrainUnpredictableBool(Unpredictable_WFxTDEBUG) then
    ExecuteAsNOP();

Hint_WFET(localtimeout);
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
- source: `wfet.xml`
</details>