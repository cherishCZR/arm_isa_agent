## DCPS1
_ARM A64 Instruction_

**Title**: DCPS1 -- A64 | **Class**: `system` | **XML ID**: `DCPS1`

**Summary**: Debug change PE state to EL1

**Description**:
This instruction, when executed in Debug state:

The target exception level of a DCPS1 instruction is:

When the target Exception level of a DCPS1 instruction is ELx, on executing this instruction:

This instruction is always UNDEFINED in Non-debug state.

This instruction is UNDEFINED at EL0 in Non-secure state if EL2 is implemented and HCR_EL2.TGE == 1.

For more information on the operation of the DCPS<n> instructions, see DCPS.

### Variant: `System`
- **Assembly**: `DCPS1  {#<imm>}`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  23  20   4   1  |
|-----------------------|
| 110 101 00  101 imm16 000 01  |
```

#### Decode (A64.control.exception.DCPS1_DC_exception)

```
// Empty.
```

#### Execute (A64.control.exception.DCPS1_DC_exception)

```
if !Halted() then UNDEFINED;
DCPSInstruction(EL1);
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<imm>` | `immediate` | `imm16` | Is an optional 16-bit unsigned immediate, in the range 0 to 65535, defaulting to 0 and encoded in the "imm16" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `dcps1.xml`
</details>