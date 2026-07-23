## SVC
_ARM A64 Instruction_

**Title**: SVC -- A64 | **Class**: `system` | **XML ID**: `SVC`

**Summary**: Supervisor call

**Description**:
This instruction causes an exception to be taken to EL1.

On executing an SVC instruction, the PE records the exception
as a Supervisor Call exception in
ESR_ELx, using the EC syndrome value
0x15, and the value of the immediate argument.

### Variant: `System`
- **Assembly**: `SVC  #<imm>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  23  20   4   1  |
|-----------------------|
| 110 101 00  000 imm16 000 01  |
```

#### Decode (A64.control.exception.SVC_EX_exception)

```
constant bits(16) imm = imm16;
```

#### Execute (A64.control.exception.SVC_EX_exception)

```
AArch64.CheckForSVCTrap(imm);
AArch64.CallSupervisor(imm);
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<imm>` | `immediate` | `imm16` | Is a 16-bit unsigned immediate, in the range 0 to 65535, encoded in the "imm16" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `svc.xml`
</details>