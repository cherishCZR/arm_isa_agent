## ERET
_ARM A64 Instruction_

**Title**: ERET -- A64 | **Class**: `system` | **XML ID**: `ERET`

**Summary**: Exception return

**Description**:
This instruction restores PSTATE from the SPSR, and branches to
the address held in the ELR.

The SPSR is checked for the current Exception level for an illegal return event.
See Illegal exception returns from AArch64 state.

ERET is UNDEFINED at EL0.

### Variant: `System`
- **Assembly**: `ERET`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25 24  20  15  11 10  9   4  |
|--------------------------------|
| 110 101 1   0100 11111 0000 0   0   11111 00000 |
```

#### Decode (A64.control.branch_reg.ERET_64E_branch_reg)

```
constant boolean pac = FALSE;
constant boolean use_key_a = TRUE;
```

#### Execute (A64.control.branch_reg.ERET_64E_branch_reg)

```
if PSTATE.EL == EL0 then UNDEFINED;
AArch64.CheckForERetTrap(pac, use_key_a);
constant bits(64) target = ELR_ELx[];

AArch64.ExceptionReturn(target, SPSR_ELx[]);
```

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `eret.xml`
</details>