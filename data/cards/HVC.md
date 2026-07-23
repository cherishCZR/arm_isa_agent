## HVC
_ARM A64 Instruction_

**Title**: HVC -- A64 | **Class**: `system` | **XML ID**: `HVC`

**Summary**: Hypervisor call

**Description**:
This instruction causes an exception to EL2. Software executing at EL1
can use this instruction to call the hypervisor to request a
service.

The HVC instruction is UNDEFINED:

On executing an HVC instruction, the PE records the exception
as a Hypervisor Call exception in
ESR_ELx, using the EC syndrome value
0x16, and the value of the immediate argument.

### Variant: `System`
- **Assembly**: `HVC  #<imm>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  23  20   4   1  |
|-----------------------|
| 110 101 00  000 imm16 000 10  |
```

#### Decode (A64.control.exception.HVC_EX_exception)

```
if !HaveEL(EL2) then EndOfDecode(Decode_UNDEF);
constant bits(16) imm = imm16;
```

#### Execute (A64.control.exception.HVC_EX_exception)

```
if PSTATE.EL == EL0 then UNDEFINED;
if PSTATE.EL == EL1 && !EL2Enabled() then UNDEFINED;
if !HaveEL(EL3) && HCR_EL2.HCD == '1' then UNDEFINED;
if HaveEL(EL3) && SCR_EL3.HCE == '0' then UNDEFINED;

AArch64.CallHypervisor(imm);
```

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `!HaveEL(EL2)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<imm>` | `immediate` | `imm16` | Is a 16-bit unsigned immediate, in the range 0 to 65535, encoded in the "imm16" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `hvc.xml`
</details>