## TCOMMIT
_ARM A64 Instruction_

**Title**: TCOMMIT -- A64 | **Class**: `system` | **XML ID**: `TCOMMIT`

**Architecture**: `FEAT_TME` (ARMv9.0)

**Summary**: Commit current transaction

**Description**:
This instruction commits the current transaction. If the current transaction
is an outer transaction, then Transactional state is exited, and all state
modifications performed transactionally are committed to the architectural
state. TCOMMIT takes no inputs and returns no value.

Execution of TCOMMIT is UNDEFINED in Non-transactional state.

### Variant: `System`
- **Assembly**: `TCOMMIT`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  11   7   4  |
|--------------------|
| 110 101 01000000110011 0000 011 11111 |
```

#### Decode (A64.control.barriers.TCOMMIT_only_barriers)

```
if !IsFeatureImplemented(FEAT_TME) then EndOfDecode(Decode_UNDEF);
```

#### Execute (A64.control.barriers.TCOMMIT_only_barriers)

```
if !IsTMEEnabled() then UNDEFINED;

if TSTATE.depth == 0 then
    UNDEFINED;

if TSTATE.depth == 1 then
    CommitTransactionalWrites();
    ClearExclusiveLocal(ProcessorID());

TSTATE.depth = TSTATE.depth - 1;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_TME)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `tcommit.xml`
</details>