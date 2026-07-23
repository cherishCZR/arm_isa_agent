## DCPS2
_ARM A64 Instruction_

**Title**: DCPS2 -- A64 | **Class**: `system` | **XML ID**: `DCPS2`

**Summary**: Debug change PE state to EL2

**Description**:
This instruction, when executed in Debug state:

The target exception level of a DCPS2 instruction is:

When the target Exception level of a DCPS2 instruction is ELx, on executing this instruction:

This instruction is always UNDEFINED in Non-debug state.

This instruction is UNDEFINED at the following exception levels:

For more information on the operation of the DCPS<n> instructions, see DCPS.

### Variant: `System`
- **Assembly**: `DCPS2  {#<imm>}`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  23  20   4   1  |
|-----------------------|
| 110 101 00  101 imm16 000 10  |
```

#### Decode (A64.control.exception.DCPS2_DC_exception)

```
// Empty.
```

#### Execute (A64.control.exception.DCPS2_DC_exception)

```
if !Halted() then UNDEFINED;
DCPSInstruction(EL2);
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<imm>` | `immediate` | `imm16` | Is an optional 16-bit unsigned immediate, in the range 0 to 65535, defaulting to 0 and encoded in the "imm16" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `dcps2.xml`
</details>