## BTI
_ARM A64 Instruction_

**Title**: BTI -- A64 | **Class**: `system` | **XML ID**: `BTI`

**Architecture**: `FEAT_BTI` (ARMv8.5)

**Summary**: Branch target identification

**Description**:
This instruction is used to guard against
the execution of instructions that are not the intended target of a branch.

Outside of a guarded memory region, a BTI instruction executes as a
NOP. Within a guarded memory region, while
PSTATE.BTYPE != 0b00, a BTI
instruction compatible with the current value of PSTATE.BTYPE
will not generate a Branch Target Exception and will allow execution of
subsequent instructions within the memory region. For more information,
see PSTATE.BTYPE.

The operand <targets> passed to a BTI instruction determines
the values of PSTATE.BTYPE that the BTI
instruction is compatible with.

### Variant: `System`
- **Assembly**: `BTI  {<targets>}`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  11   7   4  |
|--------------------|
| 110 101 01000000110010 0100 xx0 11111 |
```

#### Decode (A64.control.hints.BTI_HB_hints)

```
if !IsFeatureImplemented(FEAT_BTI) then EndOfDecode(Decode_NOP);

// Check branch target compatibility between BTI instruction and PSTATE.BTYPE
SetBTypeCompatible(BTypeCompatible_BTI(op2<2:1>));
```

#### Execute (A64.control.hints.BTI_HB_hints)

```
SetBTypeNext('00');
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_BTI)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<targets>` | `unknown` | `op2<2:1>` | Is the type of indirection, |

**<targets> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | [absent] |
| 01 | c |
| 10 | j |
| 11 | jc |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `bti.xml`
</details>