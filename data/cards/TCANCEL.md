## TCANCEL
_ARM A64 Instruction_

**Title**: TCANCEL -- A64 | **Class**: `system` | **XML ID**: `TCANCEL`

**Architecture**: `FEAT_TME` (ARMv9.0)

**Summary**: Cancel current transaction

**Description**:
This instruction exits Transactional state and discards all state
modifications that were performed transactionally. Execution continues at the
instruction that follows the TSTART instruction of the outer transaction. The
destination register of the TSTART instruction of the outer transaction is
written with the immediate operand of TCANCEL.

### Variant: `System`
- **Assembly**: `TCANCEL  #<imm>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  23  20   4   1  |
|-----------------------|
| 110 101 00  011 imm16 000 00  |
```

#### Decode (A64.control.exception.TCANCEL_EX_exception)

```
if !IsFeatureImplemented(FEAT_TME) then EndOfDecode(Decode_UNDEF);
constant boolean  retry  = (imm16<15> == '1');
constant bits(15) reason = imm16<14:0>;
```

#### Execute (A64.control.exception.TCANCEL_EX_exception)

```
if !IsTMEEnabled() then UNDEFINED;

if TSTATE.depth > 0 then
    FailTransaction(TMFailure_CNCL, retry, FALSE, reason);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_TME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<imm>` | `immediate` | `imm16` | Is a 16-bit unsigned immediate, in the range 0 to 65535, encoded in the "imm16" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `tcancel.xml`
</details>