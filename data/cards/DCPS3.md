## DCPS3
_ARM A64 Instruction_

**Title**: DCPS3 -- A64 | **Class**: `system` | **XML ID**: `DCPS3`

**Summary**: Debug change PE state to EL3

**Description**:
This instruction, when executed in Debug state:

The target exception level of a DCPS3 instruction is EL3.

On executing a DCPS3 instruction:

This instruction is always UNDEFINED in Non-debug state.

This instruction is UNDEFINED at all exception levels if either:

For more information on the operation of the DCPS<n> instructions, see DCPS.

### Variant: `System`
- **Assembly**: `DCPS3  {#<imm>}`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  23  20   4   1  |
|-----------------------|
| 110 101 00  101 imm16 000 11  |
```

#### Decode (A64.control.exception.DCPS3_DC_exception)

```
// Empty.
```

#### Execute (A64.control.exception.DCPS3_DC_exception)

```
if !Halted() then UNDEFINED;
DCPSInstruction(EL3);
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<imm>` | `immediate` | `imm16` | Is an optional 16-bit unsigned immediate, in the range 0 to 65535, defaulting to 0 and encoded in the "imm16" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `dcps3.xml`
</details>