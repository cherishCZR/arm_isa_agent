## DRPS
_ARM A64 Instruction_

**Title**: DRPS -- A64 | **Class**: `system` | **XML ID**: `DRPS`

**Summary**: Debug restore PE state

**Description**:
This instruction restores PSTATE from the SPSR.

The SPSR is checked for the current Exception level for an illegal return event.
See Illegal exception returns from AArch64 state.

This instruction is UNDEFINED in Non-debug state.

This instruction is UNDEFINED at EL0.

For more information on the operation of DRPS,
see DRPS.

### Variant: `System`
- **Assembly**: `DRPS`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25 24  20  15   9   4  |
|--------------------------|
| 110 101 1   0101 11111 000000 11111 00000 |
```

#### Decode (A64.control.branch_reg.DRPS_64E_branch_reg)

```
// Empty.
```

#### Execute (A64.control.branch_reg.DRPS_64E_branch_reg)

```
if !Halted() || PSTATE.EL == EL0 then UNDEFINED;
DRPSInstruction();
```

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `drps.xml`
</details>