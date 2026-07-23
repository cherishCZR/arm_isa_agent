## CLRBHB
_ARM A64 Instruction_

**Title**: CLRBHB -- A64 | **Class**: `system` | **XML ID**: `CLRBHB`

**Architecture**: `FEAT_CLRBHB` (ARMv8.9)

**Summary**: Clear branch history

**Description**:
This instruction clears the branch history for the current context
to the extent that branch history information created before
the CLRBHB instruction cannot be used by code before
the CLRBHB instruction to exploitatively control the execution
of any indirect branches in code in the current context that appear
in program order after the instruction.

### Variant: `System`
- **Assembly**: `CLRBHB`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  11   7   4  |
|--------------------|
| 110 101 01000000110010 0010 110 11111 |
```

#### Decode (A64.control.hints.CLRBHB_HI_hints)

```
if !IsFeatureImplemented(FEAT_CLRBHB) then EndOfDecode(Decode_NOP);
```

#### Execute (A64.control.hints.CLRBHB_HI_hints)

```
Hint_CLRBHB();
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_CLRBHB)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `clrbhb.xml`
</details>