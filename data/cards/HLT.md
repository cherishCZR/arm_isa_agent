## HLT
_ARM A64 Instruction_

**Title**: HLT -- A64 | **Class**: `system` | **XML ID**: `HLT`

**Summary**: Halt instruction

**Description**:
This instruction can generate a Halt Instruction debug
event, which causes entry into Debug state.

Within a guarded memory region, while PSTATE.BTYPE
!= 0b00, an HLT instruction that would cause entry into
Debug state will not generate a Branch Target exception and will cause entry
into Debug state as normal. For more information, see
PSTATE.BTYPE.

### Variant: `System`
- **Assembly**: `HLT  #<imm>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  23  20   4   1  |
|-----------------------|
| 110 101 00  010 imm16 000 00  |
```

#### Decode (A64.control.exception.HLT_EX_exception)

```
if EDSCR.HDE == '0' || !HaltingAllowed() then
    EndOfDecode(Decode_UNDEF);
elsif IsFeatureImplemented(FEAT_BTI) then
    SetBTypeCompatible(TRUE);
```

#### Execute (A64.control.exception.HLT_EX_exception)

```
constant boolean is_async = FALSE;
constant FaultRecord fault = NoFault();
Halt(DebugHalt_HaltInstruction, is_async, fault);
```

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `EDSCR.HDE != '0' && !HaltingAllowed()` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<imm>` | `immediate` | `imm16` | Is a 16-bit unsigned immediate, in the range 0 to 65535, encoded in the "imm16" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `hlt.xml`
</details>