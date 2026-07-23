## SMC
_ARM A64 Instruction_

**Title**: SMC -- A64 | **Class**: `system` | **XML ID**: `SMC`

**Summary**: Secure monitor call

**Description**:
This instruction causes an exception to EL3.

SMC is available only for software executing at EL1 or
higher. It is UNDEFINED in EL0.

If the values of HCR_EL2.TSC and
SCR_EL3.SMD are both 0, execution of an
SMC instruction at EL1 or higher generates a Secure Monitor
Call exception, recording it in
ESR_ELx, using the EC syndrome value
0x17, that is taken to EL3.

If the value of HCR_EL2.TSC is 1 and EL2 is enabled in the current Security state, execution
of an SMC instruction at EL1 generates an
exception that is taken to EL2, regardless of the value of
SCR_EL3.SMD.

If the value of HCR_EL2.TSC is 0 and the
value of SCR_EL3.SMD is 1, the SMC instruction
is UNDEFINED.

### Variant: `System`
- **Assembly**: `SMC  #<imm>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  23  20   4   1  |
|-----------------------|
| 110 101 00  000 imm16 000 11  |
```

#### Decode (A64.control.exception.SMC_EX_exception)

```
constant bits(16) imm = imm16;
```

#### Execute (A64.control.exception.SMC_EX_exception)

```
if PSTATE.EL == EL0 then UNDEFINED;
AArch64.CheckForSMCUndefOrTrap(imm);
AArch64.CallSecureMonitor(imm);
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<imm>` | `immediate` | `imm16` | Is a 16-bit unsigned immediate, in the range 0 to 65535, encoded in the "imm16" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `smc.xml`
</details>