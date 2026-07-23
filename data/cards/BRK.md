## BRK
_ARM A64 Instruction_

**Title**: BRK -- A64 | **Class**: `system` | **XML ID**: `BRK`

**Summary**: Breakpoint instruction

**Description**:
This instruction generates a Breakpoint
Instruction exception. The PE records the exception in
ESR_ELx, using the EC value 0x3C, and
captures the value of the immediate argument in
ESR_ELx.ISS.

Within a guarded memory region, while PSTATE.BTYPE
!= 0b00, a BRK instruction will not generate a Branch
Target exception and will generate a Breakpoint Instruction exception as
normal. For more information, see PSTATE.BTYPE.

### Variant: `System`
- **Assembly**: `BRK  #<imm>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  23  20   4   1  |
|-----------------------|
| 110 101 00  001 imm16 000 00  |
```

#### Decode (A64.control.exception.BRK_EX_exception)

```
constant bits(16) comment = imm16;
if IsFeatureImplemented(FEAT_BTI) then
    SetBTypeCompatible(TRUE);
```

#### Execute (A64.control.exception.BRK_EX_exception)

```
AArch64.SoftwareBreakpoint(comment);
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<imm>` | `immediate` | `imm16` | Is a 16-bit unsigned immediate, in the range 0 to 65535, encoded in the "imm16" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `brk.xml`
</details>