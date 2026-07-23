## STSHH
_ARM A64 Instruction_

**Title**: STSHH -- A64 | **Class**: `system` | **XML ID**: `STSHH`

**Architecture**: `FEAT_PCDPHINT` (ARMv9.6)

**Summary**: Store shared hint

**Description**:
This instruction signals to the memory system that if the next instruction in program order generates an
explicit write effect, then it is to a location that one or more other threads of execution will observe,
and there is a performance benefit to ensuring that the updated value from the write to that location
propagates to those other observers with minimal latency.

The thread of execution on the other observers might be polling the location using load or load-exclusive
instructions, or may have executed a PRFM IR instruction targeting the location.

### Variant: `System`
- **Assembly**: `STSHH  <policy>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  11   7   4  |
|--------------------|
| 110 101 01000000110010 0110 00x 11111 |
```

#### Decode (A64.control.hints.STSHH_HI_hints)

```
if !IsFeatureImplemented(FEAT_PCDPHINT) then EndOfDecode(Decode_NOP);
constant boolean stream = op2<0> == '1';
```

#### Execute (A64.control.hints.STSHH_HI_hints)

```
Hint_StoreShared(stream);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_PCDPHINT)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<policy>` | `unknown` | `op2<0>` | <policy> is one of:                                       KEEP               Signals to the memory system that there may be a performance benefit to r |

**<policy> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | KEEP |
| 1 | STRM |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `stshh.xml`
</details>